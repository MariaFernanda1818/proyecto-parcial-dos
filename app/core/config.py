"""
Este módulo define la configuración de la aplicación utilizando Pydantic y variables de entorno.

Maneja la carga de variables de entorno y su validación para proporcionar
una configuración centralizada a la aplicación.
"""
from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn, field_validator
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()


class Config(BaseSettings):
    """
    Clase de configuración utilizando Pydantic para manejar variables de entorno.
    """
    env_file = ".env"  # Define el archivo de entorno a usar

    APP_NAME: str = Field("My FastAPI App", env="APP_NAME")
    DEBUG: bool = Field(False, env="DEBUG")

    # Configuración de base de datos
    SQLALCHEMY_DATABASE_URL: PostgresDsn = Field(..., env="DATABASE_URL")
    MAX_CONNECTIONS_COUNT: int = Field(10, env="MAX_CONNECTIONS_COUNT")
    MIN_CONNECTIONS_COUNT: int = Field(10, env="MIN_CONNECTIONS_COUNT")

    RUTA_BASE: str = Field("/api", env="RUTA_BASE")

    # Validación para convertir el valor de DEBUG correctamente
    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value):
        """
        Valida y convierte el valor de la variable DEBUG.

        Args:
            value: El valor de la variable DEBUG desde el entorno.

        Returns:
            bool: True si el valor es "true" o "1", de lo contrario False.
        """
        if isinstance(value, str):
            return value.lower() in ("true", "1")
        return value


# Instanciar la configuración
config = Config()
