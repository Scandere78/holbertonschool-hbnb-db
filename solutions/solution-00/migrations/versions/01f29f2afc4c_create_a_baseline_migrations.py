"""Create a baseline migrations

Revision ID: 01f29f2afc4c
Revises: 
Create Date: 2024-07-01 14:30:51.270489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01f29f2afc4c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('amenity',
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('id', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('country',
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('code', sa.String(length=3), nullable=False),
    sa.Column('id', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('review',
    sa.Column('place_id', sa.String(length=60), nullable=False),
    sa.Column('user_id', sa.String(length=50), nullable=False),
    sa.Column('comment', sa.String(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('id', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('user',
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('first_name', sa.String(length=120), nullable=False),
    sa.Column('last_name', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('id', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('city',
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('country_code', sa.String(length=3), nullable=False),
    sa.Column('id', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['country_code'], ['country.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Place',
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('host_id', sa.String(length=36), nullable=False),
    sa.Column('city_id', sa.String(length=36), nullable=False),
    sa.Column('price_per_night', sa.Integer(), nullable=False),
    sa.Column('number_of_rooms', sa.Integer(), nullable=False),
    sa.Column('number_of_bathrooms', sa.Integer(), nullable=False),
    sa.Column('max_guests', sa.Integer(), nullable=False),
    sa.Column('id', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
    sa.ForeignKeyConstraint(['host_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('placeamenity',
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=False),
    sa.Column('amenity_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['amenity_id'], ['amenity.id'], ),
    sa.ForeignKeyConstraint(['place_id'], ['Place.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('placeamenity')
    op.drop_table('Place')
    op.drop_table('city')
    op.drop_table('user')
    op.drop_table('review')
    op.drop_table('country')
    op.drop_table('amenity')
    # ### end Alembic commands ###
