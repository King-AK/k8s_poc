"""add_options_data

Revision ID: f6d1480a88c6
Revises: d899a5d8a519
Create Date: 2021-08-11 17:54:43.514256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6d1480a88c6'
down_revision = 'd899a5d8a519'
branch_labels = None
depends_on = None


def upgrade():
    """
    Add tables for options data

    'Contract Name', 'Last Trade Date', 'Strike', 'Last Price', 'Bid',
       'Ask', 'Change', '% Change', 'Volume', 'Open Interest',
       'Implied Volatility'
    """
    # TODO: add FKs
    op.create_table('options_time_series',
                    sa.Column('symbol', sa.String(), nullable=False),
                    sa.Column('datetime', sa.DateTime(), nullable=False),
                    sa.Column('contract_name', sa.String(), nullable=False),
                    sa.Column('option_type', sa.String(), nullable=False),
                    sa.Column('expiration_date', sa.DateTime(), nullable=False),
                    sa.Column('last_trade_date', sa.DateTime(), nullable=False),
                    sa.Column('strike', sa.Float(), nullable=False),
                    sa.Column('last_price', sa.Float(), nullable=False),
                    sa.Column('bid', sa.Float(), nullable=False),
                    sa.Column('ask', sa.Float(), nullable=False),
                    sa.Column('change', sa.Float(), nullable=False),
                    sa.Column('percent_change', sa.Float(), nullable=False),
                    sa.Column('volume', sa.Integer(), nullable=False),
                    sa.Column('open_interest', sa.Integer(), nullable=False),
                    sa.Column('implied_volatility', sa.Float(), nullable=False),
                    sa.PrimaryKeyConstraint('contract_name', 'datetime')
                    )


def downgrade():
    op.drop_table('options_time_series')
