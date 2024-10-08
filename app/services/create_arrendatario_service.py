from sqlalchemy.orm import Session

from app.core.constants import MESSAGE_ARRENDATARIO_CREATED_ERROR, MESSAGE_ARRENDATARIO_CREATED_SUCCESS,  STATUS_INTERNAL_SERVER_ERROR, STATUS_SUCCESS
from app.core.logger import log_error, log_info
from app.db.arrendatario_repository import ArrendatarioRepository
from app.models.arrendatario_model import ArrendatarioModel
from app.schemas.arrendatario_schema import ArrendatarioSchema
from app.schemas.response_general import ResponseGeneral


class CreateArrendatarioService:
    def __init__(self, db: Session):
        self.repository = ArrendatarioRepository(db)

    def create_arrendatario(self, arrendatario: ArrendatarioSchema) -> ResponseGeneral:
        """
        Llama al repositorio para crear un nuevo arrendatario.
        """
        response = ResponseGeneral()
        try:
            if self.repository.exist_arrendatario_by_email(arrendatario.email):
                response.mensaje = 'El correo ya existe'
                response.status = STATUS_INTERNAL_SERVER_ERROR
                return response

            # Convertir ProductSchema a ProductModel
            pago_model = ArrendatarioModel(**arrendatario.dict())
            new_pago = self.repository.create_pago(pago_model)
            if new_pago:
                response.mensaje = MESSAGE_ARRENDATARIO_CREATED_SUCCESS
                response.status = STATUS_SUCCESS
                return response
            else:
                response.mensaje = MESSAGE_ARRENDATARIO_CREATED_ERROR
                response.status = STATUS_INTERNAL_SERVER_ERROR
                return response
        except Exception as e:
            log_error(e)
            response.mensaje = self.create_error_message(e.args)
            response.status = STATUS_INTERNAL_SERVER_ERROR
            return response

    def create_error_message(self, args):
        mensajes = []
        for numero, elemento in enumerate(args, start=1):
            mensajes.append(f"{numero}. {elemento} ")
        return ', '.join(mensajes)
