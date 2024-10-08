"""
Este módulo define los endpoints para la gestión de pagos utilizando FastAPI.

Proporciona endpoints para listar todos los pagos y registrar un nuevo pago.
Incluye manejo de excepciones personalizadas y utiliza servicios para realizar
las operaciones necesarias en la base de datos.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.constants import ERROR_GET_ALL_PAGO, ERROR_INTERNAL_SERVER
from app.core.database import get_db
from app.core.logger import log_error
from app.schemas.pago_input_schema import PagoInputSchema
from app.schemas.response_general import ResponseGeneral
from app.services.consulta_pago_service import ConsultaPagoService
from app.services.create_pago_service import CreatePagoService

router = APIRouter(
    tags=["pagos"]
)

@router.get("", response_model=ResponseGeneral)
def list_all_pagos(db: Session = Depends(get_db)):
    """
    Endpoint para listar todos los pagos registrados.

    Args:
        db (Session): Sesión de la base de datos proporcionada por la dependencia `get_db`.

    Returns:
        ResponseGeneral: Respuesta con la lista de todos los pagos.

    Raises:
        HTTPException: Si ocurre un error durante la consulta, se lanza una excepción HTTP
        con código 500.
    """
    service = ConsultaPagoService(db)
    try:
        pagos = service.get_all_pagos()
        return pagos
    except Exception as e:
        log_error(ERROR_GET_ALL_PAGO.format(e))
        raise HTTPException(
            status_code=500,
            detail=ERROR_INTERNAL_SERVER
        ) from e

@router.post("", response_model=ResponseGeneral)
def registrar_pago(pago: PagoInputSchema, db: Session = Depends(get_db)):
    """
    Endpoint para registrar un nuevo pago.

    Args:
        pago (PagoInputSchema): Esquema de datos del pago a registrar.
        db (Session): Sesión de la base de datos proporcionada por la dependencia `get_db`.

    Returns:
        ResponseGeneral: Respuesta con los detalles del pago registrado.

    Raises:
        HTTPException: Si ocurre un error durante la creación, se lanza una excepción HTTP
        con el código de estado correspondiente.
    """
    service = CreatePagoService(db)
    created_pago = service.create_pago(pago)
    # Personaliza el código de estado en función de la respuesta
    if created_pago.status == 200:
        return created_pago
    raise HTTPException(
        status_code=created_pago.status,
        detail=created_pago.mensaje
    )
