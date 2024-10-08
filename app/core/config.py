from pydantic_settings  import BaseSettings
from pydantic import Field, PostgresDsn, field_validator
from dotenv import load_dotenv


load_dotenv()

class Config(BaseSettings):
    """
    Clase de configuración utilizando Pydantic para manejar variables de entorno.
    """
    APP_NAME: str = Field("My FastAPI App", env="APP_NAME")
    DEBUG: bool = Field(False, env="DEBUG")
    
    # Configuración de base de datos
    SQLALCHEMY_DATABASE_URL: PostgresDsn = Field(..., env="DATABASE_URL")
    MAX_CONNECTIONS_COUNT: int = Field(10, env="MAX_CONNECTIONS_COUNT")
    MIN_CONNECTIONS_COUNT: int = Field(10, env="MIN_CONNECTIONS_COUNT")
    
    RUTA_BASE: str = Field("/api", env="RUTA_BASE")

    # Validación para convertir el valor de DEBUG correctamente
    @field_validator("DEBUG", mode="before")
    def parse_debug(cls, value):
        if isinstance(value, str):
            return value.lower() in ("true", "1")
        return value

    class Config:
        env_file = ".env"  # Define el archivo de entorno a usar

# Instanciar la configuración
config = Config()
