"""Create phone number column for users table

Revision ID: d593fcdae005
Revises: 
Create Date: 2024-09-11 23:30:29.823545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd593fcdae005'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String(),nullable = True))


def downgrade() -> None:
    op.drop_column('users','phone_number')
