"""empty message

Revision ID: 2ff5611b8617
Revises: 926ded765ebb
Create Date: 2025-01-05 06:57:09.446624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlalchemy_file


# revision identifiers, used by Alembic.
revision: str = '2ff5611b8617'
down_revision: Union[str, None] = '926ded765ebb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car_classes',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('car_rents',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('min_age', sa.Integer(), nullable=True),
    sa.Column('min_experience', sa.Integer(), nullable=True),
    sa.Column('min_price', sa.Integer(), nullable=True),
    sa.Column('phone', sqlalchemy_utils.types.phone_number.PhoneNumberType(length=20), nullable=True),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['region_id'], ['regions.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('car_rent_medias',
    sa.Column('car_rent_id', sa.Integer(), nullable=False),
    sa.Column('content', sqlalchemy_file.types.FileField(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_rent_id'], ['car_rents.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('car_rents_classes',
    sa.Column('car_rent_id', sa.Integer(), nullable=False),
    sa.Column('car_class_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_class_id'], ['car_classes.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['car_rent_id'], ['car_rents.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('car_rent_id', 'car_class_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('car_rents_classes')
    op.drop_table('car_rent_medias')
    op.drop_table('car_rents')
    op.drop_table('car_classes')
    # ### end Alembic commands ###
