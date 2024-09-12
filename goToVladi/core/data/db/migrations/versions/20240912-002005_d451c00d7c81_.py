"""empty message

Revision ID: d451c00d7c81
Revises: a33ec73b4ad1
Create Date: 2024-09-12 00:20:05.877076

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision: str = 'd451c00d7c81'
down_revision: Union[str, None] = 'a33ec73b4ad1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('restaurants', 'site_url',
               existing_type=sa.VARCHAR(),
               type_=sqlalchemy_utils.types.url.URLType(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('restaurants', 'site_url',
               existing_type=sqlalchemy_utils.types.url.URLType(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    # ### end Alembic commands ###
