import pytest
import pandas as pd

from pandas_type_checks.core import SeriesReturnValue, SeriesArgument, DataFrameReturnValue, DataFrameArgument
from pandas_type_checks.decorator import pandas_type_check, PandasTypeCheckDecoratorException


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


def test_argument_type_mismatch(data_frame_type):

    @pandas_type_check(DataFrameArgument('arg', data_frame_type))
    def test_function(arg: str) -> str:
        return arg

    with pytest.raises(PandasTypeCheckDecoratorException,
                       match="Argument type mismatch. Expected argument 'arg' of decorated function "
                             "'test_function' to be of type 'DataFrame' but found value of type 'str'."):
        test_function("string")


def test_unknown_argument(data_frame_type):
    # Decorated function has no arguments
    @pandas_type_check(DataFrameArgument('arg', data_frame_type))
    def test_function1() -> str:
        return "string"

    with pytest.raises(PandasTypeCheckDecoratorException,
                       match=f"Decorated function '{test_function1.__name__}' has no parameter 'arg'."):
        test_function1()

    # Decorated function has arguments but not the one's defined in the decorator
    @pandas_type_check(DataFrameArgument('arg', data_frame_type))
    def test_function2(another_arg: str) -> str:
        return another_arg

    with pytest.raises(PandasTypeCheckDecoratorException,
                       match=f"Decorated function '{test_function2.__name__}' has no parameter 'arg'."):
        test_function2("string")


def test_unsupported_decorator_argument():

    @pandas_type_check("Unsupported String Argument")
    def test_function() -> int:
        return 0

    with pytest.raises(PandasTypeCheckDecoratorException,
                       match=f"Unsupported argument for decorator. Expected argument of type "
                             f"'{DataFrameArgument.__qualname__}', '{DataFrameReturnValue.__qualname__}', "
                             f"'{SeriesArgument.__qualname__}', or '{SeriesReturnValue.__qualname__}' but "
                             f"found type 'str'."):
        test_function()
