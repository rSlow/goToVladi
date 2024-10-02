"""empty message

Revision ID: 188407648ee5
Revises: 14bfa761557c
Create Date: 2024-10-03 03:56:42.416066

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '188407648ee5'
down_revision: Union[str, None] = '14bfa761557c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('restaurant_medias_restaurant_id_fkey', 'restaurant_medias', type_='foreignkey')
    op.create_foreign_key(None, 'restaurant_medias', 'restaurants', ['restaurant_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'restaurant_medias', type_='foreignkey')
    op.create_foreign_key('restaurant_medias_restaurant_id_fkey', 'restaurant_medias', 'restaurants', ['restaurant_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###