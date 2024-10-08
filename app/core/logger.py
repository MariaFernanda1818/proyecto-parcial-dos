import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def log_info(message: str):
    """
    Función para registrar un mensaje informativo.
    """
    logger.info(message)

def log_error(message: str):
    """
    Función para registrar un mensaje de error.
    """
    logger.error(message)