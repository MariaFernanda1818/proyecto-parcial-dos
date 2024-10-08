import re
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship, validates
from app.core.constants import DOCUMENT_FORMAT_ERROR, DOCUMENT_REGEX, EMAIL_FORMAT_ERROR, EMAIL_REGEX, NAME_FORMAT_ERROR, NAME_LENGTH_ERROR, NAME_MIN_LENGTH, PHONE_FORMAT_ERROR, PHONE_LENGTH_ERROR, PHONE_MAX_LENGTH, PHONE_REGEX
from app.core.database import Base

class ArrendatarioModel(Base):
    __tablename__ = "arrendatarios"

    documento_identificacion_arrendatario = Column(String, primary_key=True, index=True)
    nombre_completo = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    telefono = Column(String(15), nullable=False)

    # Relación con pagos
    pagos = relationship("PagoModel", back_populates="arrendatario")

    @validates("telefono")
    def validate_phone(self, key, phone):
        if len(phone) > PHONE_MAX_LENGTH:
            raise ValueError(PHONE_LENGTH_ERROR)
        if not re.match(PHONE_REGEX, phone):
            raise ValueError(PHONE_FORMAT_ERROR)
        return phone

    @validates("nombre_completo")
    def validate_name(self, key, name):
        if not name or len(name) < NAME_MIN_LENGTH:
            raise ValueError(NAME_LENGTH_ERROR.format(key=key.replace('_', ' '), min_length=NAME_MIN_LENGTH))
        if not re.match("^[A-Za-z\s]+$", name):
            raise ValueError(NAME_FORMAT_ERROR.format(key=key.replace('_', ' ')))
        return name
    
    @validates("email")
    def validate_email(self, key, email):
        if not re.match(EMAIL_REGEX, email):
            raise ValueError(EMAIL_FORMAT_ERROR)
        return email
    
    @validates("documento_identificacion_arrendatario")
    def validate_document(self, key, document):
        if not re.match(DOCUMENT_REGEX, document):
            raise ValueError(DOCUMENT_FORMAT_ERROR)
        return document