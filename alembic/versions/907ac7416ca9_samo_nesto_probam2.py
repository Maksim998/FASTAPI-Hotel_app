"""Samo nesto probam2

Revision ID: 907ac7416ca9
Revises: 9d0c2994d952
Create Date: 2024-06-25 19:01:49.941083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '907ac7416ca9'
down_revision: Union[str, None] = '9d0c2994d952'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('guests',
    sa.Column('guest_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('phone', sa.String(length=50), nullable=True),
    sa.Column('address', sa.String(length=50), nullable=True),
    sa.Column('date_of_birth', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('guest_id'),
    sa.UniqueConstraint('phone')
    )
    op.create_index(op.f('ix_guests_email'), 'guests', ['email'], unique=True)
    op.create_table('rooms',
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('room_type', sa.String(length=20), nullable=True),
    sa.Column('price_per_night', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('availability_status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('room_id')
    )
    op.create_table('bookings',
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('guest_id', sa.Integer(), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.Column('check_in_date', sa.DateTime(), nullable=True),
    sa.Column('check_out_date', sa.DateTime(), nullable=True),
    sa.Column('total_amount', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('booking_status', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['guest_id'], ['guests.guest_id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.room_id'], ),
    sa.PrimaryKeyConstraint('booking_id')
    )
    op.create_table('payments',
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=True),
    sa.Column('payment_date', sa.DateTime(), nullable=True),
    sa.Column('payment_method', sa.String(length=20), nullable=True),
    sa.Column('payment_status', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['booking_id'], ['bookings.booking_id'], ),
    sa.PrimaryKeyConstraint('payment_id'),
    sa.UniqueConstraint('booking_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    op.drop_table('bookings')
    op.drop_table('rooms')
    op.drop_index(op.f('ix_guests_email'), table_name='guests')
    op.drop_table('guests')
    # ### end Alembic commands ###
