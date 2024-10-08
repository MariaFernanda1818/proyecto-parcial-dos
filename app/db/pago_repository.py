"""
Este módulo define el repositorio de pagos para interactuar con la base de datos.

Proporciona métodos para obtener, crear y verificar pagos y arrendatarios,
así como para realizar consultas específicas relacionadas con los pagos.
"""
from typing import List, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.constants import (
    ERROR_CREATE_PAGO,
    ERROR_EXIST_ARRENDATARIO_BY_NAME,
    ERROR_GET_ALL_PAGO,
    ERROR_GET_PAGO
)
from app.models.pago_model import PagoModel
from app.core.logger import log_error


class PagoRepository:
    """
    Repositorio para realizar operaciones relacionadas con pagos en la base de datos.
    """
    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de la base de datos.

        Args:
            db (Session): Sesión de base de datos proporcionada por SQLAlchemy.
        """
        self.db = db

    def exist_arrendatario_by_documento(self, documento: str) -> bool:
        """
        Verifica la existencia de un arrendatario por su documento de identificación.

        Args:
            documento (str): Documento de identificación del arrendatario.

        Returns:
            bool: True si el arrendatario existe, False en caso contrario.
        """
        try:
            query = text("""
                SELECT * FROM arrendatarios WHERE documento_identificacion_arrendatario = :documento
            """)
            result = self.db.execute(query, {"documento": documento}).fetchone()
            return result is not None
        except SQLAlchemyError as e:
            log_error(ERROR_EXIST_ARRENDATARIO_BY_NAME.format(e))
            return False

    def get_all_by_codigo_email_and_month_pay(self, codigo_inmueble: str) -> bool:
        """
        Obtiene todos los pagos realizados para un inmueble en un mes y año específicos.

        Args:
            codigo_inmueble (str): Código del inmueble.

        Returns:
            bool: Lista de pagos que coinciden con los criterios.
        """
        try:
            query = text("""
                SELECT * 
                FROM pagos
                WHERE EXTRACT(MONTH FROM fecha_pago) = 10 
                AND EXTRACT(YEAR FROM fecha_pago) = 2024 
                AND codigo_inmueble = :codigoInmueble
            """)
            return self.db.execute(query, {"codigoInmueble": codigo_inmueble}).all()
        except SQLAlchemyError as e:
            log_error(ERROR_EXIST_ARRENDATARIO_BY_NAME.format(e))
            return False

    def get_pago_by_id(self, pago_id: int) -> Optional[PagoModel]:
        """
        Obtiene un pago por su ID.

        Args:
            pago_id (int): ID del pago.

        Returns:
            Optional[PagoModel]: Pago correspondiente al ID, o None si no se encuentra.
        """
        try:
            return self.db.query(PagoModel).filter(PagoModel.id == pago_id).first()
        except SQLAlchemyError as e:
            log_error(ERROR_GET_PAGO.format(e))
            return None

    def get_all_pagos(self) -> List[PagoModel]:
        """
        Obtiene todos los pagos registrados.

        Returns:
            List[PagoModel]: Lista de todos los pagos registrados.
        """
        try:
            return self.db.query(PagoModel).all()
        except SQLAlchemyError as e:
            log_error(ERROR_GET_ALL_PAGO.format(e))
            return []

    def create_pago(self, pago: PagoModel) -> PagoModel:
        """
        Crea un nuevo pago.

        Args:
            pago (PagoModel): El pago a registrar.

        Returns:
            PagoModel: El pago registrado con sus datos actualizados.
        """
        try:
            self.db.add(pago)
            self.db.commit()
            self.db.refresh(pago)
            return pago
        except SQLAlchemyError as e:
            self.db.rollback()
            log_error(ERROR_CREATE_PAGO.format(e))
            raise
