"""
Este módulo define el modelo de arrendatario utilizado por SQLAlchemy.

Proporciona validaciones para los campos de arrendatarios, como teléfono, nombre, email
y documento de identificación, para garantizar la consistencia de los datos.
"""
import re
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, validates
from app.core.constants import (
    DOCUMENT_FORMAT_ERROR, DOCUMENT_REGEX, EMAIL_FORMAT_ERROR, EMAIL_REGEX,
    NAME_FORMAT_ERROR, NAME_LENGTH_ERROR, NAME_MIN_LENGTH, PHONE_FORMAT_ERROR,
    PHONE_LENGTH_ERROR, PHONE_MAX_LENGTH, PHONE_REGEX
)
from app.core.database import Base


class ArrendatarioModel(Base):
    """
    Modelo para representar un arrendatario en la base de datos.
    """
    __tablename__ = "arrendatarios"

    documento_identificacion_arrendatario = Column(String, primary_key=True, index=True)
    nombre_completo = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    telefono = Column(String(15), nullable=False)

    # Relación con pagos
    pagos = relationship("PagoModel", back_populates="arrendatario")

    @validates("telefono")
    def validate_phone(self, _, phone):
        """
        Valida el número de teléfono del arrendatario.

        Args:
            phone (str): El número de teléfono a validar.

        Returns:
            str: El número de teléfono validado.

        Raises:
            ValueError: Si el número de teléfono no cumple con las validaciones.
        """
        if len(phone) > PHONE_MAX_LENGTH:
            raise ValueError(PHONE_LENGTH_ERROR)
        if not re.match(PHONE_REGEX, phone):
            raise ValueError(PHONE_FORMAT_ERROR)
        return phone

    @validates("nombre_completo")
    def validate_name(self, _, name):
        """
        Valida el nombre completo del arrendatario.

        Args:
            name (str): El nombre a validar.

        Returns:
            str: El nombre validado.

        Raises:
            ValueError: Si el nombre no cumple con las validaciones.
        """
        if not name or len(name) < NAME_MIN_LENGTH:
            raise ValueError(
                NAME_LENGTH_ERROR.format(key="nombre completo", min_length=NAME_MIN_LENGTH)
            )
        if not re.match(r"^[A-Za-z\s]+$", name):
            raise ValueError(NAME_FORMAT_ERROR.format(key="nombre completo"))
        return name

    @validates("email")
    def validate_email(self, _, email):
        """
        Valida el email del arrendatario.

        Args:
            email (str): El email a validar.

        Returns:
            str: El email validado.

        Raises:
            ValueError: Si el email no cumple con las validaciones.
        """
        if not re.match(EMAIL_REGEX, email):
            raise ValueError(EMAIL_FORMAT_ERROR)
        return email

    @validates("documento_identificacion_arrendatario")
    def validate_document(self, _, document):
        """
        Valida el documento de identificación del arrendatario.

        Args:
            document (str): El documento a validar.

        Returns:
            str: El documento validado.

        Raises:
            ValueError: Si el documento no cumple con las validaciones.
        """
        if not re.match(DOCUMENT_REGEX, document):
            raise ValueError(DOCUMENT_FORMAT_ERROR)
        return document
