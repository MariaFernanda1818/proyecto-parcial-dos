"""
Este módulo define la configuración de la base de datos y la conexión usando SQLAlchemy.

Proporciona un motor de base de datos, una fábrica de sesiones, y un gestor para
obtener una sesión de base de datos de manera segura.
"""
from pydantic import BaseModel, PostgresDsn, ValidationError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import config
from app.core.logger import log_error
from app.core.constants import (
    ERROR_INVALID_DATABASE_URL,
    ERROR_DATABASE_URL_VALIDATION_FAILED,
    ERROR_SQLALCHEMY,
    ERROR_UNEXPECTED_DB_SESSION
)

# Modelo Pydantic para validar la URL de la base de datos
class Settings(BaseModel):
    """Clase para validar la configuración de la base de datos"""
    database_url: PostgresDsn

DATABASE_URL = config.SQLALCHEMY_DATABASE_URL

try:
    settings = Settings(database_url=DATABASE_URL)
    DATABASE_URL_STR = str(settings.database_url)  # Convertir a cadena
except ValidationError as e:
    log_error(ERROR_INVALID_DATABASE_URL.format(e))
    raise ValueError(ERROR_DATABASE_URL_VALIDATION_FAILED) from e

# Crear el motor de la base de datos con la URL proporcionada
# Cambia echo a True solo para depuración
engine = create_engine(DATABASE_URL_STR, echo=False)

# Crear una fábrica de sesiones para manejar la conexión con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base declarativa para definir los modelos de la base de datos
Base = declarative_base()

def get_db() -> Session:
    """
    Proporciona una sesión de base de datos utilizando un context manager.

    Yields:
        Session: Una sesión de base de datos SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        log_error(ERROR_SQLALCHEMY.format(e))
        raise
    except Exception as e:
        log_error(ERROR_UNEXPECTED_DB_SESSION.format(e))
        raise
    finally:
        db.close()
