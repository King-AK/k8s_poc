"""MAT baseline

Revision ID: d899a5d8a519
Revises:
Create Date: 2021-06-29 11:21:05.808137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd899a5d8a519'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # TODO: add FKs
    op.create_table('stock_summary',  # TODO: flesh out general stock summary information, move business information to business_summary table
                    sa.Column('symbol', sa.String(), nullable=False),
                    sa.Column('sector', sa.String(), nullable=False),
                    sa.Column('industry', sa.String(), nullable=False),
                    sa.Column('business_summary', sa.String(), nullable=False),
                    sa.Column('phone', sa.String(), nullable=False),
                    sa.Column('website', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('symbol')
                    )
    op.create_table('stock_time_series',
                    sa.Column('symbol', sa.String(), nullable=False),
                    sa.Column('datetime', sa.DateTime(), nullable=False),
                    sa.Column('open', sa.Float(), nullable=False),
                    sa.Column('low', sa.Float(), nullable=False),
                    sa.Column('high', sa.Float(), nullable=False),
                    sa.Column('close', sa.Float(), nullable=False),
                    sa.Column('volume', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('symbol', 'datetime')
                    )
    op.create_table('business_location',  # TODO: change to business_summary
                    sa.Column('symbol', sa.String(), nullable=False),
                    sa.Column('address', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('country', sa.String(), nullable=False),
                    sa.Column('zip', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('symbol')
                    )
    op.create_table('crypto_time_series',
                    sa.Column('symbol', sa.String(), nullable=False),
                    sa.Column('datetime', sa.DateTime(), nullable=False),
                    sa.Column('open', sa.Float(), nullable=False),
                    sa.Column('low', sa.Float(), nullable=False),
                    sa.Column('high', sa.Float(), nullable=False),
                    sa.Column('close', sa.Float(), nullable=False),
                    sa.Column('volume', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('symbol', 'datetime')
                    )
    # TODO: add additional tables: business_income_statement, business_balance_sheet, business_cash_flow, each with FK to business_summary


def downgrade():
    op.drop_table('stock_summary')
    op.drop_table('stock_time_series')
    op.drop_table('business_summary')
    op.drop_table('crypto_time_series')
