"""
Este módulo define el esquema de pago utilizando Pydantic.

Proporciona validaciones para los campos de pago, como el documento de identificación,
código del inmueble, valor pagado y fecha de pago, para garantizar la consistencia de los datos.
"""
from decimal import Decimal
import re
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.core.constants import DOCUMENT_REGEX, EXAMPLE_DATA_PAGO


class PagoSchema(BaseModel):
    """
    Esquema Pydantic para representar un pago.

    Incluye validaciones para los campos de documento de identificación del arrendatario,
    código del inmueble, valor pagado y fecha de pago.
    """
    id: Optional[int] = Field(None, description="ID del pago (autogenerado).")
    documento_identificacion_arrendatario: str = Field(
        ...,
        description="Documento de identificación del arrendatario, solo números permitidos."
    )
    codigo_inmueble: str = Field(
        ...,
        description="Código del inmueble, debe ser alfanumérico."
    )
    valor_pagado: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    fecha_pago: date = Field(
        ...,
        description="Fecha del pago en formato dd/mm/yyyy."
    )

    @field_validator('documento_identificacion_arrendatario')
    @classmethod
    def validate_documento_identificacion(cls, v):
        """
        Valida el documento de identificación del arrendatario.

        Args:
            v (str): El documento de identificación a validar.

        Returns:
            str: El documento de identificación validado.

        Raises:
            ValueError: Si el documento no cumple con las validaciones.
        """
        if not re.fullmatch(DOCUMENT_REGEX, v):
            raise ValueError(
                "El documento de identificación debe contener solo números y tener entre 1 y 20 caracteres."
            )
        return v

    @field_validator('codigo_inmueble')
    @classmethod
    def validate_codigo_inmueble(cls, v):
        """
        Valida el código del inmueble.

        Args:
            v (str): El código del inmueble a validar.

        Returns:
            str: El código del inmueble validado.

        Raises:
            ValueError: Si el código no cumple con las validaciones.
        """
        if not re.fullmatch(r'^[a-zA-Z0-9]+$', v):
            raise ValueError("El código del inmueble debe ser alfanumérico.")
        return v

    @classmethod
    def from_model(cls, pago_model: "PagoModel") -> "PagoSchema":
        """
        Crea una instancia de PagoSchema a partir del modelo SQLAlchemy.

        Args:
            pago_model (PagoModel): El modelo de pago de SQLAlchemy.

        Returns:
            PagoSchema: El esquema con los datos del pago.
        """
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

        Args:
            input_schema (PagoInputSchema): El esquema de entrada del pago.

        Returns:
            PagoSchema: El esquema con los datos del pago.
        """
        return cls(
            documento_identificacion_arrendatario=input_schema.documento_identificacion_arrendatario,
            codigo_inmueble=input_schema.codigo_inmueble,
            valor_pagado=input_schema.valor_pagado,
            fecha_pago=input_schema.fecha_pago
        )

    class Config:
        """
        Configuración para habilitar la conversión desde el modelo SQLAlchemy y añadir un ejemplo.
        """
        orm_mode = True
        schema_extra = {
            "example": EXAMPLE_DATA_PAGO
        }
