from fastapi import APIRouter, Depends, HTTPException
from pytest import Session

from app.core.constants import  ERROR_CREATE_PAGO, ERROR_INTERNAL_SERVER
from app.core.database import get_db
from app.core.logger import log_error
from app.schemas.pago_input_schema import PagoInputSchema
from app.schemas.pago_schema import PagoSchema
from app.schemas.response_general import ResponseGeneral
from app.services.create_pago_service import CreatePagoService

router = APIRouter(
    tags=["pagos"]
)

@router.get("",response_model=ResponseGeneral)
def list_all_pagos(db:Session = Depends(get_db)):
    pass

@router.post("",response_model=ResponseGeneral)
def registrar_pago(pago:PagoInputSchema,db: Session = Depends(get_db)):
    service = CreatePagoService(db)
    created_pago = service.create_pago(pago)
    # Personaliza el código de estado en función de la respuesta
    if created_pago.status == 200:
        return created_pago
    else:
        raise HTTPException(
            status_code=created_pago.status,
            detail=created_pago.mensaje
        )
   