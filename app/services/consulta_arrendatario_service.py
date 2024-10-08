from sqlalchemy.orm import Session

from app.core.constants import MESSAGE_PRODUCTS_LISTED, STATUS_SUCCESS
from app.db.arrendatario_repository import ArrendatarioRepository
from app.schemas.arrendatario_schema import ArrendatarioSchema
from app.schemas.response_general import ResponseGeneral


class ConsultaArrendatarioService:
    def __init__(self, db: Session):
        self.repository = ArrendatarioRepository(db)

    def get_all_arrendatarios(self) -> ResponseGeneral:
        response = ResponseGeneral()
        response.mensaje = MESSAGE_PRODUCTS_LISTED
        response.status = STATUS_SUCCESS

        # Obtener todos los productos del repositorio
        dataAll = self.repository.get_all_arrendatario()

        # Convertir los productos a ProductSchema
        data = [ArrendatarioSchema.from_model(item) for item in dataAll]

        response.data = data
        return response
