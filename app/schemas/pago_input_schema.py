"""
Este módulo define el esquema de pago utilizando Pydantic.

Proporciona validaciones para los campos de pago, como el documento de identificación,
código del inmueble, valor pagado y fecha de pago, para garantizar la consistencia de los datos.
"""
import re
from decimal import Decimal
from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator
from app.core.constants import DOCUMENT_REGEX


class PagoInputSchema(BaseModel):
    """
    Esquema Pydantic para representar un pago.

    Incluye validaciones para los campos de documento de identificación del arrendatario,
    código del inmueble, valor pagado y fecha de pago.
    """
    documento_identificacion_arrendatario: str = Field(
        ...,
        description="Documento de identificación del arrendatario, solo números permitidos."
    )
    codigo_inmueble: str = Field(
        ...,
        description="Código del inmueble, debe ser alfanumérico."
    )
    valor_pagado: Decimal = Field(...)
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
                "El documento de identificación debe contener"
                + " solo números y tener entre 1 y 20 caracteres."
            )
        return v

    @field_validator('valor_pagado', mode='before')
    @classmethod
    def check_valor_pagado(cls, v):
        """
        Verifica que el valor pagado sea mayor que 0 y menor o igual a 1000000.

        Args:
            v (Decimal): El valor pagado a validar.

        Returns:
            Decimal: El valor pagado validado.

        Raises:
            ValueError: Si el valor pagado no cumple con las validaciones.
        """
        if v <= 0:
            raise ValueError("El valor pagado debe ser mayor que 0.")
        if v > 1000000:
            raise ValueError("El valor pagado debe ser menor o igual a 1000000.")
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

    @field_validator("fecha_pago", mode="before")
    @classmethod
    def parse_fecha_pago(cls, v):
        """
        Valida y convierte el valor de la fecha de pago.

        Args:
            v (str | date): La fecha de pago a validar y convertir.

        Returns:
            date: La fecha de pago validada.

        Raises:
            ValueError: Si la fecha de pago no cumple con las validaciones.
        """
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%d/%m/%Y").date()
            except ValueError as exc:
                raise ValueError("Formato de fecha incorrecto") from exc
        raise ValueError("Formato de fecha incorrecto")

    @classmethod
    def from_model(cls, pago_model: "PagoModel") -> "PagoInputSchema":
        """
        Crea una instancia de PagoInputSchema a partir del modelo SQLAlchemy.

        Args:
            pago_model (PagoModel): El modelo de pago de SQLAlchemy.

        Returns:
            PagoInputSchema: El esquema con los datos del pago.
        """
        return cls(
            documento_identificacion_arrendatario=(
                pago_model.documento_identificacion_arrendatario
            ),
            codigo_inmueble=pago_model.codigo_inmueble,
            valor_pagado=pago_model.valor_pagado,
            fecha_pago=pago_model.fecha_pago
        )

    class Config:  # pylint: disable=too-few-public-methods
        """
        Configuración para habilitar la conversión desde el modelo SQLAlchemy y añadir un ejemplo.
        """
        orm_mode = True
