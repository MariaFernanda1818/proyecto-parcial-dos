import re
from sqlalchemy import Column, String, Numeric, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship, validates
from app.core.constants import CODE_FORMAT_ERROR, DATE_FORMAT_ERROR, ERROR_PAGO_PRICE_NEGATIVE
from app.core.database import Base
from datetime import datetime

class PagoModel(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_identificacion_arrendatario = Column(String, ForeignKey("arrendatarios.documento_identificacion_arrendatario"), nullable=False)
    codigo_inmueble = Column(String, nullable=False)
    valor_pagado = Column(Numeric, nullable=False)
    fecha_pago = Column(Date, nullable=False)

    # Relación con arrendatario
    arrendatario = relationship("ArrendatarioModel", back_populates="pagos")
    
    @validates("valor_pagado")
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError(ERROR_PAGO_PRICE_NEGATIVE)
        return value

    
    @validates("codigo_inmueble")
    def validate_codigo_inmueble(self, key, value):
        # Validar que el código del inmueble sea alfanumérico
        if not re.match("^[a-zA-Z0-9]+$", value):
            raise ValueError(CODE_FORMAT_ERROR)
        return value