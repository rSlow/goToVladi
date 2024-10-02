"""empty message

Revision ID: ad46cf48baff
Revises: a92c45678206
Create Date: 2024-10-02 19:13:24.320474

"""
from typing import Sequence, Union

import sqlalchemy_file
from alembic import op
import sqlalchemy as sa

from goToVladi.core.data.db.types.url import PydanticURLType

# revision identifiers, used by Alembic.
revision: str = 'ad46cf48baff'
down_revision: Union[str, None] = 'a92c45678206'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trips',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('site_url', PydanticURLType(), nullable=True),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['region_id'], ['regions.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trip_medias',
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.Column('content', sqlalchemy_file.types.FileField(), nullable=True),
    sa.Column('content_type', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('hotels_district_id_fkey', 'hotels', type_='foreignkey')
    op.create_foreign_key(None, 'hotels', 'hotel_districts', ['district_id'], ['id'], ondelete='SET NULL')
    op.drop_constraint('restaurant_medias_restaurant_id_fkey', 'restaurant_medias', type_='foreignkey')
    op.create_foreign_key(None, 'restaurant_medias', 'restaurants', ['restaurant_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'restaurant_medias', type_='foreignkey')
    op.create_foreign_key('restaurant_medias_restaurant_id_fkey', 'restaurant_medias', 'restaurants', ['restaurant_id'], ['id'])
    op.drop_constraint(None, 'hotels', type_='foreignkey')
    op.create_foreign_key('hotels_district_id_fkey', 'hotels', 'hotel_districts', ['district_id'], ['id'])
    op.drop_table('trip_medias')
    op.drop_table('trips')
    # ### end Alembic commands ###
