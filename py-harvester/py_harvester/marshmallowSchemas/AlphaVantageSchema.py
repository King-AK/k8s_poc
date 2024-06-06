from marshmallow import Schema, fields, pre_load
from py_harvester.marshmallowSchemas.utils import *


class AlphaVantageTimeSeriesSchema:
    @classmethod
    def clean_time_series_dictionary_list(cls, in_data_many, symbol):
        """Clean up the AlphaVantage time series dictionary list"""
        for k, v in in_data_many.items():
            v.update({"datetime": k, "symbol": symbol})
        return [v for k, v in in_data_many.items()]


class AlphaVantageStockTimeSeriesSchema(Schema, AlphaVantageTimeSeriesSchema):
    """
    Time series information for a stock using AlphaVantage.
    """

    @pre_load
    def data_cleanup(self, in_data, many, **kwargs):
        if not datetime_regex.match(in_data['datetime']):
            in_data['datetime'] = f"{in_data['datetime']}T16:00:00.000000"
        return {safename(k): v for k, v in in_data.items()}

    symbol = fields.String(attribute='symbol')
    datetime = fields.DateTime(attribute='datetime')
    _open = fields.Decimal(attribute='open')
    _high = fields.Decimal(attribute='high')
    _low = fields.Decimal(attribute='low')
    _close = fields.Decimal(attribute='close')
    _volume = fields.Integer(attribute='volume')
