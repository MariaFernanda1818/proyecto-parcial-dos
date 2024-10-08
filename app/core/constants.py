from fastapi import status


ERROR_INTERNAL_SERVER = "Internal Server Error"

ERROR_INTERNAL_SERVER = "Internal Server Error"

ERROR_INVALID_DATABASE_URL = "Invalid DATABASE_URL: {}"
ERROR_DATABASE_URL_VALIDATION_FAILED = "DATABASE_URL validation failed"
ERROR_SQLALCHEMY = "SQLAlchemy error: {}"
ERROR_UNEXPECTED_DB_SESSION = "Unexpected error while handling the database session: {}"

ALEMBIC_INI_RELATIVE_PATH = '../../alembic.ini'
ERROR_FILE_NOT_FOUND = "El archivo de configuración Alembic no se encuentra en la ruta: {}"
INFO_STARTING_MIGRATIONS = "Iniciando migraciones con el archivo de configuración: {}"
INFO_GENERATING_REVISION = "Generando nueva revisión..."
INFO_CHECKING_CURRENT_REVISION = "Verificando la revisión actual..."
INFO_APPLYING_MIGRATIONS = "Aplicando migraciones hasta la última versión (head)..."
INFO_MIGRATIONS_COMPLETED = "Migraciones completadas exitosamente."
ERROR_MIGRATIONS_FAILED = "Error durante la ejecución de las migraciones: {}"

ERROR_GET_ALL_PAGO = "Error al obtener todos los pagos: {}"
ERROR_CREATE_PAGO = "Error al crear el pago: {}"
ERROR_PAGO_PRICE_NEGATIVE = "El precio del producto no puede ser negativo"
ERROR_GET_PAGO = "Error al obtener el pago: {}"

ERROR_GET_ALL_ARRENDATARIO = "Error al obtener todos los arrendatarios: {}"
ERROR_CREATE_ARRENDATARIO = "Error al crear el arrendatario: {}"
ERROR_EXIST_ARRENDATARIO_BY_NAME = "Error al verificar la existencia del arrendatario: {}"


ID_COMMENT = "Identificador único del proveedor"
COMPANY_NAME_COMMENT = "Nombre de la empresa proveedora"
CONTACT_NAME_COMMENT = "Nombre del contacto en la empresa proveedora"
PHONE_COMMENT = "Número de teléfono del proveedor"
PHONE_MAX_LENGTH = 12
PHONE_REGEX = r'^\+?\d{1,12}$'
PHONE_LENGTH_ERROR = "El número de teléfono no debe exceder los 12 caracteres"
PHONE_FORMAT_ERROR = "El formato del número de teléfono es inválido"
NAME_MIN_LENGTH = 3
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
NAME_LENGTH_ERROR = "El {key} debe tener al menos {min_length} caracteres"
NAME_FORMAT_ERROR = "El {key} solo debe contener letras y espacios"
EMAIL_FORMAT_ERROR = "El formato del email es incorrecto. Asegúrate de que sea una dirección válida, por ejemplo, usuario@dominio.com."
DATE_FORMAT_ERROR = "El formato de la fecha es incorrecto. Debe ser dd/mm/yyyy."
CODE_FORMAT_ERROR = "El código del inmueble debe ser alfanumérico."


PRICE_GT = 0
PRICE_MAX_DIGITS = 10
PRICE_DECIMAL_PLACES = 2


MENSAJE_DESCRIPTION = "Mensaje descriptivo sobre la operación"
STATUS_DESCRIPTION = "Estado de la operación, por ejemplo, 'success' o 'error'"



ID_DESCRIPTION = "Identificador único del proveedor, solo para actualizar o eliminar"
COMPANY_NAME_DESCRIPTION = "Nombre de la empresa proveedora (mínimo 3 caracteres)"
CONTACT_NAME_DESCRIPTION = "Nombre del contacto en la empresa proveedora (mínimo 3 caracteres)"
PHONE_DESCRIPTION = "Número de teléfono del proveedor, formato válido con máximo 12 dígitos"

COMPANY_NAME_PATTERN = r'^[A-Za-z\s]+$'
CONTACT_NAME_PATTERN = r'^[A-Za-z\s]+$'
PHONE_PATTERN = r'^\+?\d{1,12}$'
DOCUMENT_REGEX = r'^\d+$'

STATUS_SUCCESS = status.HTTP_200_OK

DOCUMENT_FORMAT_ERROR = "El documento de identificación debe contener solo números."


EXAMPLE_DATA_PAGO = {
    "documento_identificacion_arrendatario": "1036946622",
    "codigo_inmueble": "8870ABC",
    "valor_pagado": "1000000.00",
    "fecha_pago": "2023-09-25"
}

EXAMPLE_DATA_ARRENDATARIO = {
    "documento_identificacion_arrendatario": "1036946622",
    "nombre_completo": "Juan Pérez",
    "email": "juan.perez@example.com",
    "telefono": "3001234567"
}

MESSAGE_PAGO_CREATED_SUCCESS = "Pago registrado correctamente"
MESSAGE_PAGO_CREATED_ERROR = "El pago no se pudo registrar"

MESSAGE_ARRENDATARIO_CREATED_SUCCESS ="Arrendatario registrado correctamente"
MESSAGE_ARRENDATARIO_CREATED_ERROR ="El arrendatario no se pudo registrar {}"

STATUS_BAD_REQUEST = status.HTTP_400_BAD_REQUEST
STATUS_INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR

# Constantes para mensajes y estado
MESSAGE_PHONE_EXISTS = "El teléfono del proveedor ya existe, debes escoger otro"

