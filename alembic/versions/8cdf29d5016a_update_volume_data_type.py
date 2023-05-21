"""update_volume_data_type

Revision ID: 8cdf29d5016a
Revises: f6d1480a88c6
Create Date: 2021-09-27 16:41:03.720327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cdf29d5016a'
down_revision = 'f6d1480a88c6'
branch_labels = None
depends_on = None


def upgrade():
    """
    Update volume data type to avoid errors due to hitting max for integer type
    """
    # TODO: add FKs
    op.alter_column('stock_time_series', 'volume', existing_type=sa.Integer(), type_=sa.BigInteger())
    op.alter_column('crypto_time_series', 'volume', existing_type=sa.Integer(), type_=sa.BigInteger())


def downgrade():
    op.alter_column('stock_time_series', 'volume', existing_type=sa.BigInteger(), type_=sa.Integer())
    op.alter_column('crypto_time_series', 'volume', existing_type=sa.BigInteger(), type_=sa.Integer())
