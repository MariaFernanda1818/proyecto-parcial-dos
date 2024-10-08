"""
Este módulo contiene la definición de la aplicación FastAPI y la configuración
inicial, incluyendo el registro de rutas y el manejo personalizado de excepciones.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api.routes import arrendatario_routes, pago_routes
from app.core.config import config


def create_app() -> FastAPI:
    """
    Crea una instancia de la aplicación FastAPI con la configuración adecuada.
    """
    app = FastAPI(
        title=config.APP_NAME,
        debug=config.DEBUG
    )

    # Registrar rutas con prefijos si es necesario
    api_prefix = config.RUTA_BASE if config.RUTA_BASE else ""
    app.include_router(pago_routes.router, prefix=f"{api_prefix}/pagos")
    app.include_router(arrendatario_routes.router,
                       prefix=f"{api_prefix}/arrendatarios")

    # Manejador de excepciones personalizado
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(exc: RequestValidationError):
        # Personaliza la estructura de la respuesta
        errors = []
        for error in exc.errors():
            field = error.get("loc")[-1]
            message = error.get("msg").split(",")[1].strip()
            # 'input' podría no estar presente en todos los casos
            input_value = error.get("input", None)

            custom_error = {
                "type": error.get("type"),
                "field": field,
                "message": message,
                "input": input_value
            }
            errors.append(custom_error)

        return JSONResponse(
            status_code=400,
            content={"detail": errors},
        )

    return app


if __name__ == "__main__":
    uvicorn.run(
        "app.main:create_app",
        host="0.0.0.0",
        port=8084,
        log_level="debug",
        reload=config.DEBUG  # Habilita reload solo si estás en modo debug
    )
