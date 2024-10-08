from typing import List, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.constants import ERROR_CREATE_PAGO, ERROR_EXIST_ARRENDATARIO_BY_NAME, ERROR_GET_ALL_PAGO, ERROR_GET_PAGO
from app.models.pago_model import PagoModel
from app.core.logger import log_info, log_error
from sqlalchemy.exc import SQLAlchemyError
from app.models.pago_model import PagoModel

class PagoRepository:
    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de la base de datos.
        """
        self.db = db

    def exist_arrendatario_by_documento(self, documento: str) -> bool:
        """
        Verifica la existencia de un producto por su nombre.
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
    
    def get_all_by_codigo_email_and_month_pay(self, codigoInmueble: str) -> bool:
        """
        Verifica la existencia de un producto por su nombre.
        """
        try:
            query = text("""
                SELECT * 
                FROM pagos
                WHERE EXTRACT(MONTH FROM fecha_pago) = 10 
                AND EXTRACT(YEAR FROM fecha_pago) = 2024 
                AND codigo_inmueble = :codigoInmueble
            """)
            return self.db.execute(query, {"codigoInmueble": codigoInmueble}).all()
        except SQLAlchemyError as e:
            log_error(ERROR_EXIST_ARRENDATARIO_BY_NAME.format(e))
            return False
    
    def get_pago_by_id(self, pago_id: int) -> Optional[PagoModel]:
        """
        Obtiene un proveedor por su ID.
        """
        try:
            return self.db.query(PagoModel).filter(PagoModel.id == pago_id).first()
        except SQLAlchemyError as e:
            log_error(ERROR_GET_PAGO.format(e))
            return None

    def get_all_pagos(self) -> List[PagoModel]:
        """
        Obtiene todos los pagos.
        """
        try:
            return self.db.query(PagoModel).all()
        except SQLAlchemyError as e:
            log_error(ERROR_GET_ALL_PAGO.format(e))
            return []
    
    def create_pago(self, pago:PagoModel):
        """
        Crea un nuevo pago.
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