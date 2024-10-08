"""
Este módulo define el esquema de la respuesta general utilizando Pydantic.

Proporciona un esquema para representar respuestas generales, incluyendo un mensaje, un estado
y datos opcionales.
"""
from typing import Optional, Union, List
from pydantic import BaseModel, Field, PositiveInt
from app.core.constants import MENSAJE_DESCRIPTION, STATUS_DESCRIPTION


class ResponseGeneral(BaseModel):
    """
    Esquema Pydantic para representar una respuesta general.

    Incluye un mensaje, un estado, y datos opcionales que pueden ser un 
    diccionario o una lista de diccionarios.
    """
    mensaje: str = Field(None, min_length=1, description=MENSAJE_DESCRIPTION)
    status: PositiveInt = Field(None, description=STATUS_DESCRIPTION)
    data: Optional[Union[dict, List[dict]]] = Field(
        None,
        description="Datos adicionales proporcionados en la respuesta."
    )
