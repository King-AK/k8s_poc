import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.dialects.postgresql import insert as pg_insert


Base = declarative_base()

# TODO: Introduce Model analogs for stock_summary and business location


class BaseModel:
    @classmethod
    def bulk_upsert(cls, rows, engine):
        """static function to bulk upsert many rows using a list of dictionaries
        TODO: move to some higher level class"""
        session = Session(bind=engine)
        if engine.dialect.name == "postgresql":
            stmt = pg_insert(cls).values(rows).on_conflict_do_update(constraint=cls.__table__.primary_key, set_=cls.__table__.columns)
            session.execute(stmt)
        else:
            session.bulk_insert_mappings(cls, rows)  # TODO: develop a general purpose UPSERT (not insert) function
        session.commit()

    @classmethod
    def bulk_delete(cls, where_clause, engine):
        """
        TODO: move to some higher level class
        """
        session = Session(bind=engine)
        delete_stmt = cls.__table__.delete().where(where_clause)
        session.execute(delete_stmt)
        session.commit()


class BaseTimeSeries(BaseModel):
    """
    Base model representation for Time Series data.
    """

    symbol = sa.Column(sa.String(), nullable=False, primary_key=True)
    datetime = sa.Column(sa.DateTime(), nullable=False, primary_key=True)
    open = sa.Column(sa.Float(), nullable=False)
    close = sa.Column(sa.Float(), nullable=False)
    high = sa.Column(sa.Float(), nullable=False)
    low = sa.Column(sa.Float(), nullable=False)
    volume = sa.Column(sa.Integer(), nullable=False)

    def __repr__(self):
        return self.symbol

    @classmethod
    def bulk_delete_symbol(cls, symbol):
        cls.bulk_delete(cls.symbol == symbol)


class StockTimeSeries(Base, BaseTimeSeries):
    """
    Model representaion for Stock Market Time Series data. A single data point in time capturing market information for a particular stock.
    """
    __tablename__ = 'stock_time_series'
    # TODO: update models for relationships, define the symbol with a FK relation to stock summaries


class CryptoTimeSeries(Base, BaseTimeSeries):
    """
    Model representaion for Cryptocurrency Time Series data. A single data point in time capturing market information for a particular cryptocurrency.
    """
    __tablename__ = 'crypto_time_series'
    # TODO: continue development. Probably need to introduce a new migration file for crypto tables
    # TODO: update models for relationships, define the symbol with a FK relation to crypto summaries


class OptionsTimeSeries(Base, BaseModel):
    """
    Model representaion for Options Time Series data. A single data point in time capturing market information for a particular option.
    """
    __tablename__ = 'options_time_series'

    symbol = sa.Column(sa.String(), nullable=False)
    datetime = sa.Column(sa.DateTime(), nullable=False, primary_key=True)
    implied_volatility = sa.Column(sa.Float(), nullable=False)
    open_interest = sa.Column(sa.Integer(), nullable=False)
    bid = sa.Column(sa.Float(), nullable=False)
    ask = sa.Column(sa.Float(), nullable=False)
    change = sa.Column(sa.Float(), nullable=False)
    percent_change = sa.Column(sa.Float(), nullable=False)
    volume = sa.Column(sa.Integer(), nullable=False)
    option_type = sa.Column(sa.String(), nullable=False)
    last_trade_date = sa.Column(sa.DateTime(), nullable=False)
    strike = sa.Column(sa.Float(), nullable=False)
    expiration_date = sa.Column(sa.DateTime(), nullable=False)
    last_price = sa.Column(sa.Float(), nullable=False)
    contract_name = sa.Column(sa.String(), nullable=False, primary_key=True)

    def __repr__(self):
        return self.contract_name

    @classmethod
    def bulk_delete_symbol(cls, symbol):
        cls.bulk_delete(cls.symbol == symbol)


class DIXTimeSeries(Base, BaseModel):
    """
    Model representaion for DIX Time Series data. A single data point in time capturing DIX market information for a particular stock/index.
    """
    __tablename__ = 'dix_time_series'

    symbol = sa.Column(sa.String(), nullable=False, primary_key=True)
    datetime = sa.Column(sa.DateTime(), nullable=False, primary_key=True)
    close = sa.Column(sa.Float(), nullable=False)
    dix = sa.Column(sa.Float(), nullable=False)
    gex = sa.Column(sa.Float(), nullable=False)

    def __repr__(self):
        return self.symbol

    @classmethod
    def bulk_delete_symbol(cls, symbol):
        cls.bulk_delete(cls.symbol == symbol)
