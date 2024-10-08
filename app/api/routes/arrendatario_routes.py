from fastapi import APIRouter, Depends, HTTPException
from pytest import Session

from app.core.constants import  ERROR_CREATE_ARRENDATARIO, ERROR_INTERNAL_SERVER
from app.core.database import get_db
from app.core.logger import log_error
from app.schemas.arrendatario_schema import ArrendatarioSchema
from app.schemas.response_general import ResponseGeneral
from app.services.create_arrendatario_service import CreateArrendatarioService


router = APIRouter(
    tags=["arrendatarios"]
)

@router.get("",response_model=ResponseGeneral)
def list_all_arrendatarios(db:Session = Depends(get_db)):
    pass

@router.post("",response_model=ResponseGeneral)
def registrar_arrendatario(arrendatarioSchema:ArrendatarioSchema,db: Session = Depends(get_db)):
    service = CreateArrendatarioService(db)
    try:
        created_supplier = service.create_arrendatario(arrendatarioSchema)
        return created_supplier
    except Exception as e:
        log_error(ERROR_CREATE_ARRENDATARIO.format(e))
        raise HTTPException(status_code=500, detail=ERROR_INTERNAL_SERVER)