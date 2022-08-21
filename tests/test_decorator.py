import pytest
import pandas as pd

from pandas_type_checks import config
from pandas_type_checks.core import SeriesReturnValue, SeriesArgument, DataFrameReturnValue, DataFrameArgument
from pandas_type_checks.decorator import pandas_type_check, PandasTypeCheckDecoratorException


def test_data_frame_argument(data_frame, data_frame_type):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(DataFrameArgument('arg', data_frame_type))
    def test_function(arg: pd.DataFrame) -> pd.DataFrame:
        return arg

    result = test_function(data_frame)
    pd.testing.assert_frame_equal(result, data_frame)


def test_data_frame_return_value(data_frame, data_frame_type):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(DataFrameReturnValue(data_frame_type))
    def test_function() -> pd.DataFrame:
        return data_frame

    result = test_function()
    pd.testing.assert_frame_equal(result, data_frame)


def test_series_argument(series, series_type):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(SeriesArgument('arg', series_type))
    def test_function(arg: pd.Series) -> pd.Series:
        return arg

    result = test_function(series)
    pd.testing.assert_series_equal(result, series)


def test_series_return_value(series, series_type):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(SeriesReturnValue(series_type))
    def test_function() -> pd.Series:
        return series

    result = test_function()
    pd.testing.assert_series_equal(result, series)


def test_type_error_for_data_frame_argument(data_frame_type, wrong_data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(DataFrameArgument('arg', data_frame_type))
    def test_function(arg: pd.DataFrame) -> pd.DataFrame:
        return arg

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{test_function.__name__}'\n"
                             f"Type error in argument 'arg':\n"
                             f"\tExpected type 'float64' for column A' but found type 'int64'\n"
                             f"\tMissing column in DataFrame: 'B'"):
        test_function(wrong_data_frame)


def test_type_error_for_data_frame_return_value(data_frame_type, wrong_data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(DataFrameReturnValue(data_frame_type))
    def test_function() -> pd.DataFrame:
        return wrong_data_frame

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{test_function.__name__}'\n"
                             f"Type error in return value:\n"
                             f"\tExpected type 'float64' for column A' but found type 'int64'\n"
                             f"\tMissing column in DataFrame: 'B'"):
        test_function()


def test_strict_type_check_for_data_frame_argument(data_frame_type, extended_data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(DataFrameArgument('arg', data_frame_type), strict=True)
    def test_function(arg: pd.DataFrame) -> pd.DataFrame:
        return arg

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{test_function.__name__}'\n"
                             f"Type error in argument 'arg':\n"
                             f"\tFound unspecified column in data frame: 'D'"):
        test_function(extended_data_frame)


def test_strict_type_check_for_data_frame_return_value(data_frame_type, extended_data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    # Enable strict type check mode through keyword argument
    @pandas_type_check(DataFrameReturnValue(data_frame_type), strict=True)
    def test_function() -> pd.DataFrame:
        return extended_data_frame

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{test_function.__name__}'\n"
                             f"Type error in return value:\n"
                             f"\tFound unspecified column in data frame: 'D'"):
        test_function()


def test_type_error_for_series_argument(series_type, wrong_series):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(SeriesArgument('arg', series_type))
    def test_function(arg: pd.Series) -> pd.Series:
        return arg

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{test_function.__name__}'\n"
                             f"Type error in argument 'arg':\n"
                             f"\tExpected Series of type 'int64' but found type 'float64'"):
        test_function(wrong_series)


def test_type_error_for_series_return_value(series_type, wrong_series):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(SeriesReturnValue(series_type))
    def test_function() -> pd.Series:
        return wrong_series

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{test_function.__name__}'\n"
                             f"Type error in return value:\n"
                             f"\tExpected Series of type 'int64' but found type 'float64'"):
        test_function()


def test_data_frame_argument_type_mismatch(data_frame_type):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(DataFrameArgument('arg', data_frame_type))
    def test_function(arg: str) -> str:
        return arg

    with pytest.raises(PandasTypeCheckDecoratorException,
                       match=f"Argument type mismatch. Expected argument 'arg' of decorated function "
                             f"'{test_function.__name__}' to be of type '{pd.DataFrame.__qualname__}' "
                             f"but found value of type 'str'."):
        test_function("string")


def test_series_argument_type_mismatch(series_type):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(SeriesArgument('arg', series_type))
    def test_function(arg: str) -> str:
        return arg

    with pytest.raises(PandasTypeCheckDecoratorException,
                       match=f"Argument type mismatch. Expected argument 'arg' of decorated function "
                             f"'{test_function.__name__}' to be of type '{pd.Series.__qualname__}' "
                             f"but found value of type 'str'."):
        test_function("string")


def test_return_value_type_mismatch(data_frame_type):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    return_value = 0

    @pandas_type_check(DataFrameReturnValue(data_frame_type))
    def test_function():
        return return_value

    with pytest.raises(PandasTypeCheckDecoratorException,
                       match=f"Return value type mismatch. Expected return value of decorated function "
                             f"'{test_function.__name__}' to be of type '{pd.DataFrame.__qualname__}' but "
                             f"found value of type '{type(return_value).__qualname__}'."):
        test_function()


def test_unknown_argument(data_frame_type):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

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
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check("Unsupported String Argument")
    def test_function() -> int:
        return 0

    with pytest.raises(PandasTypeCheckDecoratorException,
                       match=f"Unsupported argument for decorator. Expected argument of type "
                             f"'{DataFrameArgument.__qualname__}', '{DataFrameReturnValue.__qualname__}', "
                             f"'{SeriesArgument.__qualname__}', or '{SeriesReturnValue.__qualname__}' but "
                             f"found type 'str'."):
        test_function()


def test_multiple_return_value_decorator_arguments(series, series_type, data_frame_type):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(SeriesReturnValue(series_type), DataFrameReturnValue(data_frame_type))
    def test_function() -> pd.Series:
        return series

    with pytest.raises(PandasTypeCheckDecoratorException,
                       match="Only one return value type marker allowed in type check decorator."):
        test_function()


def test_disable_type_checks_through_config(data_frame_type, wrong_data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(DataFrameArgument('arg', data_frame_type))
    def test_function(arg: pd.DataFrame) -> pd.DataFrame:
        return arg

    # Disable type checks in global configuration
    config.enable_type_checks = False
    assert config.enable_type_checks is False

    # No type error should be raised when applying the function to a data frame with the wrong structure
    result = test_function(wrong_data_frame)
    pd.testing.assert_frame_equal(result, wrong_data_frame)


def test_strict_type_check_mode_through_config(data_frame_type, extended_data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(DataFrameReturnValue(data_frame_type))
    def test_function() -> pd.DataFrame:
        return extended_data_frame

    config.strict_type_checks = True
    assert config.strict_type_checks is True

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{test_function.__name__}'\n"
                             f"Type error in return value:\n"
                             f"\tFound unspecified column in data frame: 'D'"):
        test_function()


def test_log_type_errors_through_config(data_frame_type, wrong_data_frame, caplog):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(DataFrameArgument('arg', data_frame_type))
    def test_function(arg: pd.DataFrame) -> pd.DataFrame:
        return arg

    # Disable type checks in global configuration
    config.log_type_errors = True
    assert config.log_type_errors is True

    # No type error should be raised when applying the function to a data frame with the wrong structure
    result = test_function(wrong_data_frame)
    pd.testing.assert_frame_equal(result, wrong_data_frame)

    # Instead the type error should be logged
    assert caplog.records
    log_record = caplog.records[-1]
    assert log_record.levelname == 'ERROR'
    assert log_record.message == (f"Pandas type error in function '{test_function.__name__}'\n"
                                  f"Type error in argument 'arg':\n"
                                  f"\tExpected type 'float64' for column A' but found type 'int64'\n"
                                  f"\tMissing column in DataFrame: 'B'")
