"""add file_key to invoices

Revision ID: f069ac14445e
Revises: 092672faf57e
Create Date: 2025-07-24 07:03:47.217144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f069ac14445e'
down_revision: Union[str, Sequence[str], None] = '092672faf57e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoices', sa.Column('file_key', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('invoices', 'file_key')
    # ### end Alembic commands ###
