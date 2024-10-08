
from sqlalchemy import text
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.constants import ERROR_CREATE_ARRENDATARIO, ERROR_EXIST_ARRENDATARIO_BY_NAME
from app.core.logger import log_info, log_error
from app.models.arrendatario_model import ArrendatarioModel
from sqlalchemy.exc import SQLAlchemyError


class ArrendatarioRepository:
    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de la base de datos.
        """
        self.db = db
    
    def get_all_arrendatario(self) -> List[ArrendatarioModel]:
        """
        Obtiene todos los arrendatarios.
        """
        try:
            return self.db.query(ArrendatarioModel).all()
        except SQLAlchemyError as e:
            #log_error(ERROR_GET_ALL_ARRENDATARIO.format(e))
            return []
        
    def exist_arrendatario_by_email(self, email: str) -> bool:
        """
        Verifica la existencia de un producto por su nombre.
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
    
    def create_pago(self, arrendatario:ArrendatarioModel):
        """
        Crea un nuevo arrendatario.
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