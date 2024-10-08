from pydantic import BaseModel, Field, constr, PositiveInt
from typing import Optional, Union, List
from app.core.constants import *


class ResponseGeneral(BaseModel):
    mensaje: str = Field(None, min_length=1, description=MENSAJE_DESCRIPTION)
    status: PositiveInt = Field(None, description=STATUS_DESCRIPTION)
    data: Optional[Union[dict, List[dict]]] = Field(
        None
    )
