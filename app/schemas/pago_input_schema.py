from decimal import Decimal
import re
from pydantic import BaseModel, Field, constr, condecimal, field_validator, model_validator
from datetime import date,datetime
from typing import Optional
from app.core.constants import (
    DATE_FORMAT_ERROR,
    DOCUMENT_REGEX,
    EXAMPLE_DATA_PAGO
)

class PagoInputSchema(BaseModel):
    documento_identificacion_arrendatario: str =  Field(..., description="Documento de identificación del arrendatario, solo números permitidos.")
    codigo_inmueble: str = Field(..., description="Código del inmueble, debe ser alfanumérico.")
    valor_pagado: Decimal = Field(...)
    fecha_pago: date = Field(..., description="Fecha del pago en formato dd/mm/yyyy.")

    @field_validator('documento_identificacion_arrendatario')
    def validate_documento_identificacion(cls, v):
        if not re.fullmatch(DOCUMENT_REGEX, v):
            raise ValueError("El documento de identificación debe contener solo números y tener entre 1 y 20 caracteres.")
        return v
    
    @field_validator('valor_pagado', mode='before')
    def check_valor_pagado(cls, v):
        if v <= 0:
            raise ValueError("El valor pagado debe ser mayor que 0.")
        elif v > 1000000:
            raise ValueError("El valor pagado debe ser menor o igual a 1000000.")
        return v
            
    @field_validator('codigo_inmueble')
    def validate_codigo_inmueble(cls, v):
        if not re.fullmatch(r'^[a-zA-Z0-9]+$', v):
            raise ValueError("El codigo del inmueble debe ser alfanumerico")
        return v

    @field_validator("fecha_pago", mode="before")
    def parse_fecha_pago(cls, v):
        # Si el valor ya es un objeto de tipo date, lo retornamos tal cual
        if isinstance(v, date):
            return v
        # Si es una cadena, intentamos parsearla
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%d/%m/%Y").date()
            except ValueError:
                raise ValueError("Formato de fecha incorrecto")
        # Si no es ninguno de los tipos esperados, lanzamos un error
        raise ValueError("Formato de fecha incorrecto")

  

    @classmethod
    def from_model(cls, pago_model: "PagoModel") -> "PagoInputSchema":
        return cls(
            documento_identificacion_arrendatario=pago_model.documento_identificacion_arrendatario,
            codigo_inmueble=pago_model.codigo_inmueble,
            valor_pagado=pago_model.valor_pagado,
            fecha_pago=pago_model.fecha_pago
        )

    class Config:
        orm_mode = True  # Configuración para habilitar la conversión desde el modelo SQLAlchemy
        schema_extra = {
            "example": EXAMPLE_DATA_PAGO
        }
