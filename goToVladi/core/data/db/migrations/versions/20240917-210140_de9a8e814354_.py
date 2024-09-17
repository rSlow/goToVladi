"""empty message

Revision ID: de9a8e814354
Revises: d451c00d7c81
Create Date: 2024-09-17 21:01:40.827273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'de9a8e814354'
down_revision: Union[str, None] = 'd451c00d7c81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('restaurants', sa.Column('is_inner', sa.Boolean(), nullable=False, server_default=sa.sql.true()))
    op.add_column('restaurants', sa.Column('is_delivery', sa.Boolean(), nullable=False, server_default=sa.sql.false()))
    op.drop_column('restaurants', 'type_')
    sa.Enum('DELIVERY', 'INNER', name='restauranttype').drop(op.get_bind())
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum('DELIVERY', 'INNER', name='restauranttype').create(op.get_bind())
    op.add_column('restaurants', sa.Column('type_', postgresql.ENUM('DELIVERY', 'INNER', name='restauranttype', create_type=False), autoincrement=False, nullable=False))
    op.drop_column('restaurants', 'is_delivery')
    op.drop_column('restaurants', 'is_inner')
    # ### end Alembic commands ###
