from marshmallow.schema import Schema
from marshmallow import fields


class StockTimeSeriesSchema(Schema):
    """
    Time series information for a stock
    """
    symbol = fields.String(attribute='symbol')
    datetime = fields.String(attribute='datetime')
    open = fields.Decimal(attribute='open')
    high = fields.Decimal(attribute='high')
    low = fields.Decimal(attribute='low')
    close = fields.Decimal(attribute='close')
    volume = fields.Integer(attribute='volume')


class CryptoTimeSeriesSchema(Schema):
    """
    Time series information for a cryptocurrency.
    """
    symbol = fields.String(attribute='symbol')
    datetime = fields.DateTime(attribute='datetime')
    open = fields.Decimal(attribute='open')
    high = fields.Decimal(attribute='high')
    low = fields.Decimal(attribute='low')
    close = fields.Decimal(attribute='close')
    volume = fields.Decimal(attribute='volume')
