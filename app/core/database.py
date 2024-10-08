import logging
from contextlib import contextmanager
from typing import Generator
from pydantic_core import MultiHostUrl
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import config
from pydantic import BaseModel, PostgresDsn, ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.core.logger import log_info, log_error
from app.core.constants import *

# Modelo Pydantic para validar la URL de la base de datos
class Settings(BaseModel):
    database_url: PostgresDsn

DATABASE_URL = config.SQLALCHEMY_DATABASE_URL

try:
    settings = Settings(database_url=DATABASE_URL)
    database_url_str = str(settings.database_url)  # Convertir a cadena
except ValidationError as e:
    log_error(ERROR_INVALID_DATABASE_URL.format(e))
    raise ValueError(ERROR_DATABASE_URL_VALIDATION_FAILED)

# Crear el motor de la base de datos con la URL proporcionada
engine = create_engine(database_url_str, echo=False)  # Cambia echo a True solo para depuración

# Crear una fábrica de sesiones para manejar la conexión con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base declarativa para definir los modelos de la base de datos
Base = declarative_base()

# Función para obtener una sesión de base de datos usando un context manager
def get_db() -> Session:
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