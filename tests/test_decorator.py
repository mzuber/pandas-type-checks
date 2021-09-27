import pandas as pd

from pandas_type_checks.core import SeriesReturnValue, SeriesArgument, DataFrameReturnValue, DataFrameArgument
from pandas_type_checks.decorator import pandas_type_check


def test_data_frame_argument(data_frame, data_frame_type):

    @pandas_type_check(DataFrameArgument('arg', data_frame_type))
    def test_function(arg: pd.DataFrame) -> pd.DataFrame:
        return arg

    result = test_function(data_frame)
    assert result.equals(data_frame) is True


def test_data_frame_return_value(data_frame, data_frame_type):

    @pandas_type_check(DataFrameReturnValue(data_frame_type))
    def test_function() -> pd.DataFrame:
        return data_frame

    result = test_function()
    assert result.equals(data_frame) is True


def test_series_argument(series, series_type):

    @pandas_type_check(SeriesArgument('arg', series_type))
    def test_function(arg: pd.Series) -> pd.Series:
        return arg

    result = test_function(series)
    assert result.equals(series) is True


def test_series_return_value(series, series_type):

    @pandas_type_check(SeriesReturnValue(series_type))
    def test_function() -> pd.Series:
        return series

    result = test_function()
    assert result.equals(series) is True
