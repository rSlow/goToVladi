"""empty message

Revision ID: 7fbd85e0f673
Revises: aad5d1915828
Create Date: 2025-02-18 18:09:21.240807

"""
from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fbd85e0f673'
down_revision: Union[str, None] = 'aad5d1915828'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car_rents', sa.Column('site_url', sqlalchemy_utils.types.url.URLType(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('car_rents', 'site_url')
    # ### end Alembic commands ###
