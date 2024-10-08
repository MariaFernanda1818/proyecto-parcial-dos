import re
from pydantic import BaseModel, Field, constr, EmailStr, field_validator
from app.core.constants import (
    DOCUMENT_REGEX, NAME_MIN_LENGTH,  PHONE_REGEX, 
     PHONE_MAX_LENGTH, EXAMPLE_DATA_ARRENDATARIO
)

class ArrendatarioSchema(BaseModel):
    documento_identificacion_arrendatario: str = Field(...,  min_length=1,
        max_length=20, 
        description="El documento de identificación del arrendatario, solo números permitidos.")
    
    nombre_completo: str = Field(...,min_length=NAME_MIN_LENGTH, max_length=100,description="Nombre completo del arrendatario. Debe contener solo letras y espacios.")
    
    email: EmailStr = Field(..., description="Email del arrendatario. Debe ser un formato de email válido.")
    
    telefono: str = Field(..., max_length=PHONE_MAX_LENGTH,description="Número de teléfono del arrendatario. Debe cumplir con el formato correcto y tener una longitud máxima de 15 caracteres.")
    
    @field_validator('documento_identificacion_arrendatario')
    def validate_documento_identificacion(cls, v):
        if not re.fullmatch(DOCUMENT_REGEX, v):
            raise ValueError("El documento de identificación debe contener solo números y tener entre 1 y 20 caracteres.")
        return v
    
    @field_validator('telefono')
    def validate_documento_identificacion(cls, v):
        if not re.fullmatch(PHONE_REGEX, v):
            raise ValueError("El telefono debe ser solo numeros")
        return v
    
    @classmethod
    def from_model(cls, arrendatario_model: "ArrendatarioModel") -> "ArrendatarioSchema":
        return cls(
            documento_identificacion_arrendatario=arrendatario_model.documento_identificacion_arrendatario,
            nombre_completo=arrendatario_model.nombre_completo,
            email=arrendatario_model.email,
            telefono=arrendatario_model.telefono
        )

    class Config:
        orm_mode = True  # Configuración para habilitar la conversión desde el modelo SQLAlchemy
        schema_extra = {
            "example": EXAMPLE_DATA_ARRENDATARIO
        }
