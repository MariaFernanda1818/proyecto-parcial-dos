from sqlalchemy.orm import Session

from app.core.constants import MESSAGE_PRODUCTS_LISTED, STATUS_SUCCESS
from app.db.pago_repository import PagoRepository
from app.schemas.pago_schema import PagoSchema
from app.schemas.response_general import ResponseGeneral


class ConsultaPagoService:
    def __init__(self, db: Session):
        self.repository = PagoRepository(db)

    def get_all_pagos(self) -> ResponseGeneral:
        response = ResponseGeneral()
        response.mensaje = MESSAGE_PRODUCTS_LISTED
        response.status = STATUS_SUCCESS

        # Obtener todos los productos del repositorio
        dataAll = self.repository.get_all_pagos()

        # Convertir los productos a ProductSchema
        data = [PagoSchema.from_model(item) for item in dataAll]

        response.data = data
        return response
