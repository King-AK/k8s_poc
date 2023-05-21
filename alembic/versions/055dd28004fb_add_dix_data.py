"""add_dix_data

Revision ID: 055dd28004fb
Revises: 8cdf29d5016a
Create Date: 2021-10-09 14:23:58.279276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '055dd28004fb'
down_revision = '8cdf29d5016a'
branch_labels = None
depends_on = None


def upgrade():
    """
    Add tables for DIX data
    """
    # TODO: add FKs
    op.create_table('dix_time_series',
                    sa.Column('symbol', sa.String(), nullable=False),
                    sa.Column('datetime', sa.DateTime(), nullable=False),
                    sa.Column('close', sa.Float(), nullable=False),
                    sa.Column('dix', sa.Float(), nullable=False),
                    sa.Column('gex', sa.Float(), nullable=False),
                    sa.PrimaryKeyConstraint('symbol', 'datetime')
                    )


def downgrade():
    op.drop_table('dix_time_series')
