from sqlalchemy.orm import Session

from datetime import datetime
from app.core.constants import  MESSAGE_PAGO_CREATED_ERROR, MESSAGE_PAGO_CREATED_SUCCESS,  STATUS_INTERNAL_SERVER_ERROR, STATUS_SUCCESS
from app.core.logger import log_error, log_info
from app.db.pago_repository import PagoRepository
from app.models.pago_model import PagoModel
from app.schemas.pago_input_schema import PagoInputSchema
from app.schemas.pago_schema import PagoSchema
from app.schemas.response_general import ResponseGeneral


class CreatePagoService:
    def __init__(self, db:Session):
        self.repository = PagoRepository(db)
    
    def create_pago(self, pago: PagoInputSchema) -> ResponseGeneral:
        """
        Llama al repositorio para crear un nuevo pago.
        """
        response = ResponseGeneral()
        fecha_actual = datetime.now()
        dia_actual = fecha_actual.day
        if dia_actual % 2 != 0:
            response.mensaje = "Lo siento, pero no se puede recibir el pago por decreto de administración"
            response.status = 400
            return response
        try:
            if not self.repository.exist_arrendatario_by_documento(pago.documento_identificacion_arrendatario):
                response.mensaje = "El arrendador del pago no existe"
                response.status = 400
                return response
            # Convertimos el schema de entrada a PagoSchema
            pago_schem = PagoSchema.from_input_schema(pago)
            pago_arriendo = 1000000
            pago_acumulado = sum(p.valor_pagado for p in self.repository.get_all_by_codigo_email_and_month_pay(pago_schem.codigo_inmueble))

            # Calcular el pago restante y sobrante
            pago_restante = pago_arriendo - (pago_acumulado + pago_schem.valor_pagado)
            pago_sobrante = max(0, -pago_restante)  # Si pago_restante es negativo, este será el pago sobrante
            pago_restante = max(0, pago_restante)   # Si pago_restante es negativo, lo ajustamos a 0

            # Generar el mensaje de respuesta basado en el cálculo
            if 0 < pago_restante < pago_arriendo:
                response.mensaje = f"Gracias por tu abono, sin embargo, recuerda que te hace falta pagar ${pago_restante}"
            elif pago_restante == 0:
                response.mensaje = "Gracias por pagar todo tu arriendo"
            
            log_info(str(pago_sobrante))
            response.status = 200

            # Guardar el nuevo pago en la base de datos
            pago_model = PagoModel(**pago_schem.dict())  # Convertimos el schema a un modelo de base de datos
            self.repository.create_pago(pago_model)
            return response
        except Exception as e:
            log_error(e)
            response.mensaje = self.create_error_message(e.args)
            response.status = STATUS_INTERNAL_SERVER_ERROR
            return response


    def create_error_message(self,args):
        mensajes = []
        for numero, elemento in enumerate(args, start=1):
            mensajes.append(f"{numero}. {elemento} ")
        return ', '.join(mensajes)
    
    
    