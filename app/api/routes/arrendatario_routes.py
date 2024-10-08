"""
Este módulo define los endpoints para la gestión de arrendatarios utilizando FastAPI.

Proporciona endpoints para listar todos los arrendatarios y registrar un nuevo arrendatario.
También incluye manejo de excepciones personalizadas y utiliza servicios para realizar
las operaciones necesarias en la base de datos.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.constants import (
    ERROR_GET_ALL_ARRENDATARIO,
    ERROR_CREATE_ARRENDATARIO,
    ERROR_INTERNAL_SERVER
)
from app.core.database import get_db
from app.core.logger import log_error
from app.schemas.arrendatario_schema import ArrendatarioSchema
from app.schemas.response_general import ResponseGeneral
from app.services.consulta_arrendatario_service import ConsultaArrendatarioService
from app.services.create_arrendatario_service import CreateArrendatarioService

router = APIRouter(
    tags=["arrendatarios"]
)

@router.get("", response_model=ResponseGeneral)
def list_all_arrendatarios(db: Session = Depends(get_db)):
    """
    Endpoint para listar todos los arrendatarios registrados.

    Args:
        db (Session): Sesión de la base de datos proporcionada por la dependencia `get_db`.

    Returns:
        ResponseGeneral: Respuesta con la lista de todos los arrendatarios.

    Raises:
        HTTPException: Si ocurre un error durante la consulta, se lanza una excepción HTTP
        con código 500.
    """
    service = ConsultaArrendatarioService(db)
    try:
        arrendatarios = service.get_all_arrendatarios()
        return arrendatarios
    except Exception as e:
        log_error(ERROR_GET_ALL_ARRENDATARIO.format(e))
        raise HTTPException(
            status_code=500,
            detail=ERROR_INTERNAL_SERVER
        ) from e

@router.post("", response_model=ResponseGeneral)
def registrar_arrendatario(arrendatario_schema: ArrendatarioSchema, db: Session = Depends(get_db)):
    """
    Endpoint para registrar un nuevo arrendatario.

    Args:
        arrendatario_schema (ArrendatarioSchema): Esquema de datos del arrendatario a registrar.
        db (Session): Sesión de la base de datos proporcionada por la dependencia `get_db`.

    Returns:
        ResponseGeneral: Respuesta con los detalles del arrendatario registrado.

    Raises:
        HTTPException: Si ocurre un error durante la creación, se lanza una excepción HTTP
        con código 500.
    """
    service = CreateArrendatarioService(db)
    try:
        created_arrendatario = service.create_arrendatario(arrendatario_schema)
        return created_arrendatario
    except Exception as e:
        log_error(ERROR_CREATE_ARRENDATARIO.format(e))
        raise HTTPException(
            status_code=500,
            detail=ERROR_INTERNAL_SERVER
        ) from e
