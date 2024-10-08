"""
Este módulo define el repositorio de arrendatarios para interactuar con la base de datos.

Proporciona métodos para obtener todos los arrendatarios, verificar la existencia de un
arrendatario por correo electrónico y crear un nuevo arrendatario.
"""
from typing import List
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.constants import (
    ERROR_CREATE_ARRENDATARIO,
    ERROR_EXIST_ARRENDATARIO_BY_NAME
)
from app.core.logger import log_error
from app.models.arrendatario_model import ArrendatarioModel


class ArrendatarioRepository:
    """
    Repositorio para realizar operaciones relacionadas con arrendatarios en la base de datos.
    """
    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de la base de datos.

        Args:
            db (Session): Sesión de base de datos proporcionada por SQLAlchemy.
        """
        self.db = db

    def get_all_arrendatario(self) -> List[ArrendatarioModel]:
        """
        Obtiene todos los arrendatarios.

        Returns:
            List[ArrendatarioModel]: Lista de todos los arrendatarios registrados.
        """
        try:
            return self.db.query(ArrendatarioModel).all()
        except SQLAlchemyError as e:
            log_error(f"Error al obtener todos los arrendatarios: {e}")
            return []

    def exist_arrendatario_by_email(self, email: str) -> bool:
        """
        Verifica la existencia de un arrendatario por su email.

        Args:
            email (str): El correo electrónico del arrendatario.

        Returns:
            bool: True si el arrendatario existe, False en caso contrario.
        """
        try:
            query = text("""
                SELECT * FROM arrendatarios WHERE email = :emailArrendatario
            """)
            result = self.db.execute(query, {"emailArrendatario": email}).fetchone()
            return result is not None
        except SQLAlchemyError as e:
            log_error(ERROR_EXIST_ARRENDATARIO_BY_NAME.format(e))
            return False

    def create_pago(self, arrendatario: ArrendatarioModel) -> ArrendatarioModel:
        """
        Crea un nuevo arrendatario.

        Args:
            arrendatario (ArrendatarioModel): El arrendatario a registrar.

        Returns:
            ArrendatarioModel: El arrendatario registrado con sus datos actualizados.
        """
        try:
            self.db.add(arrendatario)
            self.db.commit()
            self.db.refresh(arrendatario)
            return arrendatario
        except SQLAlchemyError as e:
            self.db.rollback()
            log_error(ERROR_CREATE_ARRENDATARIO.format(e))
            raise
