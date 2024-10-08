"""
Este módulo define el esquema de arrendatario utilizando Pydantic.

Proporciona validaciones para los campos de arrendatarios, como el documento de identificación,
nombre completo, email y teléfono, para garantizar la consistencia de los datos.
"""
import re
from pydantic import BaseModel, Field, EmailStr, field_validator
from app.core.constants import (
    DOCUMENT_REGEX, NAME_MIN_LENGTH, PHONE_REGEX,
    PHONE_MAX_LENGTH, EXAMPLE_DATA_ARRENDATARIO
)


class ArrendatarioSchema(BaseModel):
    """
    Esquema Pydantic para representar un arrendatario.

    Incluye validaciones para los campos de documento de identificación, nombre completo,
    email y teléfono.
    """
    documento_identificacion_arrendatario: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description=(
            "El documento de identificación del arrendatario, solo números permitidos."
        )
    )
    nombre_completo: str = Field(
        ...,
        min_length=NAME_MIN_LENGTH,
        max_length=100,
        description="Nombre completo del arrendatario. Debe contener solo letras y espacios."
    )
    email: EmailStr = Field(
        ...,
        description="Email del arrendatario. Debe ser un formato de email válido."
    )
    telefono: str = Field(
        ...,
        max_length=PHONE_MAX_LENGTH,
        description=(
            "Número de teléfono del arrendatario. Debe cumplir con el formato correcto "
            "y tener una longitud máxima de 15 caracteres."
        )
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
                "El documento de identificación debe contener solo números y tener "
                "entre 1 y 20 caracteres."
            )
        return v

    @field_validator('telefono')
    @classmethod
    def validate_telefono(cls, v):
        """
        Valida el número de teléfono del arrendatario.

        Args:
            v (str): El número de teléfono a validar.

        Returns:
            str: El número de teléfono validado.

        Raises:
            ValueError: Si el número de teléfono no cumple con las validaciones.
        """
        if not re.fullmatch(PHONE_REGEX, v):
            raise ValueError(
                "El teléfono debe contener solo números y tener un formato válido."
            )
        return v

    @classmethod
    def from_model(cls, arrendatario_model: "ArrendatarioModel") -> "ArrendatarioSchema":
        """
        Crea una instancia de ArrendatarioSchema a partir del modelo SQLAlchemy.

        Args:
            arrendatario_model (ArrendatarioModel): El modelo de arrendatario de SQLAlchemy.

        Returns:
            ArrendatarioSchema: El esquema con los datos del arrendatario.
        """
        return cls(
            documento_identificacion_arrendatario=(
                arrendatario_model.documento_identificacion_arrendatario
            ),
            nombre_completo=arrendatario_model.nombre_completo,
            email=arrendatario_model.email,
            telefono=arrendatario_model.telefono
        )

    class Config(BaseModel.Config):  # pylint: disable=too-few-public-methods
        """
        Configuración para habilitar la conversión desde el modelo SQLAlchemy y añadir un ejemplo.
        """
        orm_mode = True
        schema_extra = {
            "example": EXAMPLE_DATA_ARRENDATARIO
        }
