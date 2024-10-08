"""
Este módulo define el modelo de pago utilizado por SQLAlchemy.

Proporciona validaciones para los campos de pagos, como el valor pagado y el código del inmueble,
para garantizar la consistencia de los datos.
"""
import re
from sqlalchemy import Column, String, Numeric, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship, validates
from app.core.constants import (
    CODE_FORMAT_ERROR, ERROR_PAGO_PRICE_NEGATIVE
)
from app.core.database import Base


class PagoModel(Base):
    """
    Modelo para representar un pago en la base de datos.
    """
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_identificacion_arrendatario = Column(
        String, ForeignKey("arrendatarios.documento_identificacion_arrendatario"), nullable=False
    )
    codigo_inmueble = Column(String, nullable=False)
    valor_pagado = Column(Numeric, nullable=False)
    fecha_pago = Column(Date, nullable=False)

    # Relación con arrendatario
    arrendatario = relationship("ArrendatarioModel", back_populates="pagos")

    @validates("valor_pagado")
    def validate_price(self, _, value):
        """
        Valida que el valor pagado sea mayor o igual a cero.

        Args:
            value (Numeric): El valor pagado a validar.

        Returns:
            Numeric: El valor pagado validado.

        Raises:
            ValueError: Si el valor pagado es negativo.
        """
        if value < 0:
            raise ValueError(ERROR_PAGO_PRICE_NEGATIVE)
        return value

    @validates("codigo_inmueble")
    def validate_codigo_inmueble(self, _, value):
        """
        Valida que el código del inmueble sea alfanumérico.

        Args:
            value (str): El código del inmueble a validar.

        Returns:
            str: El código del inmueble validado.

        Raises:
            ValueError: Si el código del inmueble no es alfanumérico.
        """
        if not re.match(r"^[a-zA-Z0-9]+$", value):
            raise ValueError(CODE_FORMAT_ERROR)
        return value
