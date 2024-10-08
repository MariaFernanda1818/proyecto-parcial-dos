from decimal import Decimal
import re
from pydantic import BaseModel, Field, constr, condecimal, field_validator, model_validator
from datetime import date,datetime
from typing import Optional
from app.core.constants import (
    DOCUMENT_REGEX,
    EXAMPLE_DATA_PAGO
)

class PagoSchema(BaseModel):
    id: Optional[int] = Field(None, description="ID del pago (autogenerado).")
    documento_identificacion_arrendatario: str =  Field(..., description="Documento de identificación del arrendatario, solo números permitidos.")
    codigo_inmueble: str = Field(..., description="Código del inmueble, debe ser alfanumérico.")
    valor_pagado: Decimal = Field(..., gt=0,
        max_digits=10,
        decimal_places=2)
    fecha_pago: date = Field(..., description="Fecha del pago en formato dd/mm/yyyy.")

    @field_validator('documento_identificacion_arrendatario')
    def validate_documento_identificacion(cls, v):
        if not re.fullmatch(DOCUMENT_REGEX, v):
            raise ValueError("El documento de identificación debe contener solo números y tener entre 1 y 20 caracteres.")
        return v

    @field_validator('codigo_inmueble')
    def validate_codigo_inmueble(cls, v):
        if not re.fullmatch(r'^[a-zA-Z0-9]+$', v):
            raise ValueError("El codigo del inmueble debe ser alfanumerico")
        return v

    @classmethod
    def from_model(cls, pago_model: "PagoModel") -> "PagoSchema":
        return cls(
            id=pago_model.id,
            documento_identificacion_arrendatario=pago_model.documento_identificacion_arrendatario,
            codigo_inmueble=pago_model.codigo_inmueble,
            valor_pagado=pago_model.valor_pagado,
            fecha_pago=pago_model.fecha_pago
        )
        
    
    @classmethod
    def from_input_schema(cls, input_schema: "PagoInputSchema") -> "PagoSchema":
        """
        Crea una instancia de PagoSchema a partir de una instancia de PagoInputSchema.
        """
        return cls(
            documento_identificacion_arrendatario=input_schema.documento_identificacion_arrendatario,
            codigo_inmueble=input_schema.codigo_inmueble,
            valor_pagado=input_schema.valor_pagado,
            fecha_pago=input_schema.fecha_pago
        )
    
    class Config:
        orm_mode = True  # Configuración para habilitar la conversión desde el modelo SQLAlchemy
        schema_extra = {
            "example": EXAMPLE_DATA_PAGO
        }
