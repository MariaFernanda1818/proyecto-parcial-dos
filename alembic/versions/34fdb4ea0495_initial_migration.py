"""Initial migration

Revision ID: 34fdb4ea0495
Revises: 
Create Date: 2024-10-07 01:24:37.834552

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34fdb4ea0495'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('arrendatarios',
    sa.Column('documento_identificacion_arrendatario', sa.String(), nullable=False),
    sa.Column('nombre_completo', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('telefono', sa.String(length=15), nullable=False),
    sa.PrimaryKeyConstraint('documento_identificacion_arrendatario'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_arrendatarios_documento_identificacion_arrendatario'), 'arrendatarios', ['documento_identificacion_arrendatario'], unique=False)
    op.create_table('pagos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('documento_identificacion_arrendatario', sa.String(), nullable=False),
    sa.Column('codigo_inmueble', sa.String(), nullable=False),
    sa.Column('valor_pagado', sa.Numeric(), nullable=False),
    sa.Column('fecha_pago', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['documento_identificacion_arrendatario'], ['arrendatarios.documento_identificacion_arrendatario'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pagos')
    op.drop_index(op.f('ix_arrendatarios_documento_identificacion_arrendatario'), table_name='arrendatarios')
    op.drop_table('arrendatarios')
    # ### end Alembic commands ###
