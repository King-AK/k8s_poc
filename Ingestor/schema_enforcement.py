"""
Define the schemas for the database tables..
"""
from marshmallow import Schema, fields, pre_load
import re
from datetime import datetime


def safename(name, lower=False):
    name = re.sub(r"[0-9\.\(\)]", "", name)
    name = re.sub(" ", "_", name)
    name = re.sub("%", "percent", name)
    if lower:
        name = name.lower()
    return name


# TODO: evaluate a bit more closely and optimize
datetime_regex = re.compile(r"20[0-9]{2}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}")

"""
class ActionsSchema(Schema):
    symbol = fields.String(attribute='symbol')
    date = fields.Date(attribute='date')
    dividend = fields.Decimal(attribute='dividend')
    split = fields.Decimal(attribute='split')


class StockSustainabilitySchema(Schema):
    symbol = fields.String(attribute='symbol')
    date = fields.Date(attribute='date')
    category = fields.String(attribute='category')
    value = fields.String(attribute='value')

class StockInstitutionalHolderSchema(Schema):
    symbol = fields.String(attribute='symbol')
    holder = fields.String(attribute='holder')
    shares = fields.Integer(attribtue='shares')
    date_reported = fields.DateTime(attribute='date_reported')
    percent_out = fields.Decimal(attribute='percent_out')
    value = fields.Decimal(attribute='value')


class StockRecommendationsSchema(Schema):
    symbol = fields.String(attribute='symbol')
    date = fields.Date(attribute='date')
    firm = fields.String(attribute='firm')
    to_grade = fields.String(attribute='to_grade')
    from_grade = fields.String(attribute='from_grade')
    action = fields.String(attribute='action')


class StockStatsSchema(Schema):
    symbol = fields.String(attribute='symbol')
    dividend_yield = fields.String(attribute='dividend_yield')
    quote_type = fields.String(attribute='quote_type')
    shares_outstanding = fields.Integer(attribute='shares_outstanding')
    shares_short = fields.Integer(attribute='shares_short')
    short_ratio = fields.Decimal(attribute='short_ratio')
    short_percent_of_float = fields.Decimal(attribute='short_percent_of_float')
    last_split_date = fields.Date(attribute='last_split_date')
    last_split_factor = fields.Decimal(attribute='last_split_factor')  # TODO: will need to convert from ratio string to decimal
    peg_ratio = fields.Decimal(attribute='peg_ratio')


class BusinessStatsSchema(Schema):
    symbol = fields.String(attribute='schema')
    date = fields.DateTime()  # TODO default to current datetime pulled
    full_time_employees = fields.Integer(attribute='full_time_employees')
    trailing_pe = fields.String(attribute='trailing_pe')
    forward_pe = fields.Decimal(attribute='forward_pe')
    enterprise_to_revenue = fields.Decimal(attribtue='enterprise_to_revenue')
    profit_margins = fields.Decimal(attribute='profit_margins')
    enterprise_ebitda = fields.Decimal(attribute='enterprise_ebitda')
    forward_eps = fields.Decimal(attribute='forward_eps')
    trailing_eps = fields.Decimal(attribute='trailing_eps')
    book_value = fields.Decimal(attribute='book_value')
    price_to_book = fields.Decimal(attribute='price_to_book')
    enterprise_value = fields.Decimal(attribute='enterprise_value')
    earnings_quarterly_growth = fields.Decimal(attribute='earnings_quarterly_growth')
"""


class BusinessLocationSchema(Schema):
    """
    Location information
    """
    symbol = fields.String(attribute='symbol')
    address = fields.String(attribute='address')
    city = fields.String(attribute='city')
    state = fields.String(attribute='state')
    country = fields.String(attribute='country')
    zip = fields.String(attribute='zip')


class StockTimeSeriesSchema(Schema):
    """
    Time series information for a stock
    """
    symbol = fields.String(attribute='symbol')
    datetime = fields.String(attribute='datetime')  # TODO: possibly convert this to datetime, w/ 4PM EST defaults
    open = fields.Decimal(attribute='open')
    high = fields.Decimal(attribute='high')
    low = fields.Decimal(attribute='low')
    close = fields.Decimal(attribute='close')
    volume = fields.Integer(attribute='volume')


class AlphaVantageTimeSeriesSchema:
    @classmethod
    def clean_time_series_dictionary_list(cls, in_data_many, symbol):
        """Clean up the AlphaVantage time series dictionary list to accomodate tables"""
        for k, v in in_data_many.items():
            v.update({"datetime": k, "symbol": symbol})
        return [v for k, v in in_data_many.items()]


class AlphaVantageStockTimeSeriesSchema(Schema, AlphaVantageTimeSeriesSchema):
    """
    Time series information for a stock using AlphaVantage. Transform incoming data into a format compatible with the DB on the fly.
    """

    @pre_load
    def data_cleanup(self, in_data, many, **kwargs):
        # if not datetime_regex.match(in_data['datetime']):
        #     in_data['datetime'] = f"{in_data['datetime']}T16:00:00.000000"
        return {safename(k): v for k, v in in_data.items()}

    symbol = fields.String(attribute='symbol')
    datetime = fields.DateTime(attribute='datetime')
    _open = fields.Decimal(attribute='open')
    _high = fields.Decimal(attribute='high')
    _low = fields.Decimal(attribute='low')
    _close = fields.Decimal(attribute='close')
    _volume = fields.Integer(attribute='volume')
    # TODO: capture market cap


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


class AlphaVantageUSDCryptoTimeSeriesSchema(Schema, AlphaVantageTimeSeriesSchema):
    """
    Time series information for a cryptocurrency using AlphaVantage. Transform incoming data into a format compatible with the DB on the fly.
    """

    @pre_load
    def data_cleanup(self, in_data, many, **kwargs):
        # in_data['datetime'] = f"{in_data['datetime']}T16:00:00.000000"  # TODO: make a conditional for appropriate intraday handling
        # TODO: ALSO figure out correct close for crypto
        return {safename(k): v for k, v in in_data.items()}

    symbol = fields.String(attribute='symbol')
    datetime = fields.DateTime(attribute='datetime')
    a_open_USD = fields.Decimal(attribute='open')
    a_high_USD = fields.Decimal(attribute='high')
    a_low_USD = fields.Decimal(attribute='low')
    a_close_USD = fields.Decimal(attribute='close')
    _volume = fields.Decimal(attribute='volume')
    # TODO: capture market cap


class AlphaVantageUSDCryptoTimeSeriesIntradaySchema(Schema, AlphaVantageTimeSeriesSchema):
    """
    Time series information for a cryptocurrency using AlphaVantage. Transform incoming data into a format compatible with the DB on the fly.
    """

    @pre_load
    def data_cleanup(self, in_data, many, **kwargs):
        # in_data['datetime'] = f"{in_data['datetime']}T16:00:00.000000"  # TODO: make a conditional for appropriate intraday handling
        # TODO: ALSO figure out correct close for crypto
        return {safename(k): v for k, v in in_data.items()}

    symbol = fields.String(attribute='symbol')
    datetime = fields.DateTime(attribute='datetime')
    _open = fields.Decimal(attribute='open')
    _high = fields.Decimal(attribute='high')
    _low = fields.Decimal(attribute='low')
    _close = fields.Decimal(attribute='close')
    _volume = fields.Decimal(attribute='volume')
    # TODO: capture market cap


class StockSummarySchema(Schema):
    """
    Cover information briefs for a stock
    """
    symbol = fields.String(attribute='symbol')
    sector = fields.String(attribute='sector')
    industry = fields.String(attribute='industry')
    business_summary = fields.String(attribute='business_summary')
    phone = fields.String(attribute='phone')
    website = fields.String(attribute='website')


class AlphaVantageBusinessSummarySchema(Schema):
    """
    Cover information briefs for a business
    """

    @pre_load
    def data_cleanup(self, in_data, many, **kwargs):
        return {safename(k): v for k, v in in_data.items()}

    Symbol = fields.String(attribute='symbol')
    AssetType = fields.String(attribute='asset_type')
    Name = fields.String(attribute='name')
    Description = fields.String(attribute='description')
    Exchange = fields.String(attribute='exchange')
    Country = fields.String(attribute='country')
    Sector = fields.String(attribute='sector')
    Industry = fields.String(attribute='industry')
    Address = fields.String(attribute='address')
    FullTimeEmployees = fields.String(attribute='full_time_employees')
    FiscalYearEnd = fields.String(attribute='fiscal_year_end')
    LatestQuarter = fields.String(attribute='latest_quarter')


class AlphaVantageBusinessStatsSchema(Schema):
    """
    Cover stat briefs for a business
    # TODO: isolate and break this up into smaller tables: business_summary, business_stats, and stock_stats?
    """

    @pre_load
    def data_cleanup(self, in_data, many, **kwargs):
        return {safename(k): v for k, v in in_data.items()}

    Symbol = fields.String(attribute='symbol')
    MarketCapitalization = fields.String(attribute='market_capitalization')
    EBITDA = fields.String(attribute='ebitda')
    PERatio = fields.String(attribute='pe_ratio')
    PEGRatio = fields.String(attribute='peg_ratio')
    BookValue = fields.String(attribute='book_value')
    DividendPerShare = fields.String(attribute='dividend_per_share')
    DividendYield = fields.String(attribute='dividend_yield')
    EPS = fields.String(attribute='eps')
    RevenuePerShareTTM = fields.String(attribute='revenue_per_share_ttm')
    ProfitMargin = fields.String(attribute='profit_margin')
    OperatingMarginTTM = fields.String(attribute='operating_margin_ttm')
    ReturnOnAssetsTTM = fields.String(attribute='return_on_assets_ttm')
    ReturnOnEquityTTM = fields.String(attribute='return_on_equity_ttm')
    RevenueTTM = fields.String(attribute='revenue_ttm')
    GrossProfitTTM = fields.String(attribute='gross_profit_ttm')
    DilutedEPSTTM = fields.String(attribute='diluted_eps_ttm')
    QuarterlyEarningsGrowthYOY = fields.String(attribute='quarterly_earnings_growth_yoy')
    QuarterlyRevenueGrowthYOY = fields.String(attribute='quarterly_revenue_growth_yoy')
    AnalystTargetPrice = fields.String(attribute='analyst_target_price')
    TrailingPE = fields.String(attribute='trailing_pe')
    ForwardPE = fields.String(attribute='forward_pe')
    PriceToSalesRatioTTM = fields.String(attribute='price_to_sales_ratio_ttm')
    PriceToBookRatio = fields.String(attribute='price_to_book_ratio')
    EVToRevenue = fields.String(attribute='ev_to_revenue')
    EVToEBITDA = fields.String(attribute='ev_to_ebitda')

# TODO: add tests for the stats schemas and also add the necessary logic for the other new endpoints
# TODO: sit down and reconfirm desired database archtiecture. Get pen and paper, or whiteboard, sit down and sketch it out.


class AlphaVantageStockStatsSchema(Schema):
    """
    Cover stat briefs for a stock
    # TODO: isolate and break this up into smaller tables: business_summary, business_stats, and stock_stats?
    """

    @pre_load
    def data_cleanup(self, in_data, many, **kwargs):
        return {safename(k): v for k, v in in_data.items()}

    Symbol = fields.String(attribute='symbol')
    Beta = fields.String(attribute='beta')
    WeekHigh = fields.String(attribute='week_high')
    WeekLow = fields.String(attribute='week_low')
    DayMovingAverage = fields.String(attribute='day_moving_average')
    SharesOutstanding = fields.String(attribute='shares_outstanding')
    SharesFloat = fields.String(attribute='shares_float')
    SharesShort = fields.String(attribute='shares_short')
    SharesShortPriorMonth = fields.String(attribute='shares_short_prior_month')
    ShortRatio = fields.String(attribute='short_ratio')
    ShortPercentOutstanding = fields.String(attribute='short_percent_outstanding')
    ShortPercentFloat = fields.String(attribute='short_percent_float')
    PercentInsiders = fields.String(attribute='percent_insiders')
    PercentInstitutions = fields.String(attribute='percent_institutions')
    ForwardAnnualDividendRate = fields.String(attribute='forward_annual_dividend_rate')
    ForwardAnnualDividendYield = fields.String(attribute='forward_annual_dividend_yield')
    PayoutRatio = fields.String(attribute='payout_ratio')
    DividendDate = fields.String(attribute='dividend_date')
    ExDividendDate = fields.String(attribute='ex_dividend_date')
    LastSplitFactor = fields.String(attribute='last_split_factor')
    LastSplitDate = fields.String(attribute='last_split_date')


class AlphaVantageFullBusinessSummarySchema(Schema):
    """
    Cover information briefs for a stock
    # TODO: isolate and break this up into smaller tables: business_summary, business_stats, and stock_stats?
    """

    @pre_load
    def data_cleanup(self, in_data, many, **kwargs):
        return {safename(k): v for k, v in in_data.items()}

    Symbol = fields.String(attribute='symbol')
    AssetType = fields.String(attribute='asset_type')
    Name = fields.String(attribute='name')
    Description = fields.String(attribute='description')
    Exchange = fields.String(attribute='exchange')
    Country = fields.String(attribute='country')
    Sector = fields.String(attribute='sector')
    Industry = fields.String(attribute='industry')
    Address = fields.String(attribute='address')
    FullTimeEmployees = fields.String(attribute='full_time_employees')
    FiscalYearEnd = fields.String(attribute='fiscal_year_end')
    LatestQuarter = fields.String(attribute='latest_quarter')
    MarketCapitalization = fields.String(attribute='market_capitalization')
    EBITDA = fields.String(attribute='ebitda')
    PERatio = fields.String(attribute='pe_ratio')
    PEGRatio = fields.String(attribute='peg_ratio')
    BookValue = fields.String(attribute='book_value')
    DividendPerShare = fields.String(attribute='dividend_per_share')
    DividendYield = fields.String(attribute='dividend_yield')
    EPS = fields.String(attribute='eps')
    RevenuePerShareTTM = fields.String(attribute='revenue_per_share_ttm')
    ProfitMargin = fields.String(attribute='profit_margin')
    OperatingMarginTTM = fields.String(attribute='operating_margin_ttm')
    ReturnOnAssetsTTM = fields.String(attribute='return_on_assets_ttm')
    ReturnOnEquityTTM = fields.String(attribute='return_on_equity_ttm')
    RevenueTTM = fields.String(attribute='revenue_ttm')
    GrossProfitTTM = fields.String(attribute='gross_profit_ttm')
    DilutedEPSTTM = fields.String(attribute='diluted_eps_ttm')
    QuarterlyEarningsGrowthYOY = fields.String(attribute='quarterly_earnings_growth_yoy')
    QuarterlyRevenueGrowthYOY = fields.String(attribute='quarterly_revenue_growth_yoy')
    AnalystTargetPrice = fields.String(attribute='analyst_target_price')
    TrailingPE = fields.String(attribute='trailing_pe')
    ForwardPE = fields.String(attribute='forward_pe')
    PriceToSalesRatioTTM = fields.String(attribute='price_to_sales_ratio_ttm')
    PriceToBookRatio = fields.String(attribute='price_to_book_ratio')
    EVToRevenue = fields.String(attribute='ev_to_revenue')
    EVToEBITDA = fields.String(attribute='ev_to_ebitda')
    Beta = fields.String(attribute='beta')
    WeekHigh = fields.String(attribute='week_high')
    WeekLow = fields.String(attribute='week_low')
    DayMovingAverage = fields.String(attribute='day_moving_average')
    SharesOutstanding = fields.String(attribute='shares_outstanding')
    SharesFloat = fields.String(attribute='shares_float')
    SharesShort = fields.String(attribute='shares_short')
    SharesShortPriorMonth = fields.String(attribute='shares_short_prior_month')
    ShortRatio = fields.String(attribute='short_ratio')
    ShortPercentOutstanding = fields.String(attribute='short_percent_outstanding')
    ShortPercentFloat = fields.String(attribute='short_percent_float')
    PercentInsiders = fields.String(attribute='percent_insiders')
    PercentInstitutions = fields.String(attribute='percent_institutions')
    ForwardAnnualDividendRate = fields.String(attribute='forward_annual_dividend_rate')
    ForwardAnnualDividendYield = fields.String(attribute='forward_annual_dividend_yield')
    PayoutRatio = fields.String(attribute='payout_ratio')
    DividendDate = fields.String(attribute='dividend_date')
    ExDividendDate = fields.String(attribute='ex_dividend_date')
    LastSplitFactor = fields.String(attribute='last_split_factor')
    LastSplitDate = fields.String(attribute='last_split_date')


class YahooStockOptionsSchema(Schema):

    @pre_load
    def data_cleanup(self, in_data, many, **kwargs):
        data = {safename(k, lower=True): v for k, v in in_data.items()}
        # NOTE: dropping the timezone because Docker is crapping itself when utilizing strptime()
        data['last_trade_date'] = datetime.strptime(data['last_trade_date'].strip(" EDT"), "%Y-%m-%d %I:%M%p").strftime('%Y-%m-%d %H:%M')
        for key in ['bid', 'ask', 'volume', 'open_interest']:
            if data[key] == '-':
                data[key] = 0
        for key in ['implied_volatility', 'percent_change']:
            if data[key] == '-':
                data[key] = 0.0
            else:
                data[key] = float(re.sub(r'[,%]', '', data[key]))/100.0
        return data

    symbol = fields.String(attribute='symbol')
    datetime = fields.DateTime(attribute='datetime')
    contract_name = fields.String(attribute='contract_name')
    option_type = fields.String(attribute='option_type')
    expiration_date = fields.DateTime(attribute='expiration_date')
    last_trade_date = fields.DateTime(attribute='last_trade_date')
    strike = fields.Decimal(attribute='strike')
    last_price = fields.Decimal(attribute='last_price')
    bid = fields.Decimal(attribute='bid')
    ask = fields.Decimal(attribute='ask')
    change = fields.Decimal(attribute='change')
    percent_change = fields.Decimal(attribute='percent_change')
    volume = fields.Integer(attribute='volume')
    open_interest = fields.Integer(attribute='open_interest')
    implied_volatility = fields.Decimal(attribute='implied_volatility')


class DIXSchema(Schema):
    datetime = fields.DateTime(attribute='datetime')
    symbol = fields.String(attribute='symbol')
    price = fields.Decimal(attribute='close')
    dix = fields.Decimal(attribute='dix')
    gex = fields.Decimal(attribute='gex')
