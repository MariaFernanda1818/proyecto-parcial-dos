"""
Este módulo proporciona funciones para registrar mensajes de log.

Incluye funciones para registrar mensajes informativos y mensajes de error
usando la biblioteca estándar `logging` de Python.
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def log_info(message: str):
    """
    Función para registrar un mensaje informativo.

    Args:
        message (str): El mensaje informativo a registrar.
    """
    logger.info(message)

def log_error(message: str):
    """
    Función para registrar un mensaje de error.

    Args:
        message (str): El mensaje de error a registrar.
    """
    logger.error(message)
