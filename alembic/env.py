from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os

# Import absoluto para evitar problemas con rutas relativas
from app.core.database import Base, engine
from app.models.arrendatario_model import ArrendatarioModel
from app.models.pago_model import PagoModel


# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de Alembic
config = context.config

# Interpretar el archivo de configuración de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Sobrescribir la URL de SQLAlchemy con la URL del .env
config.set_main_option("sqlalchemy.url", os.environ.get("SQLALCHEMY_DATABASE_URL"))

# Definir los metadatos de los modelos
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Ejecutar migraciones en modo 'online'."""
    connectable = engine

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
