import pytest
import numpy as np
import pandas as pd
import pandera as pa

from pandas_type_checks import config
from pandas_type_checks.core import SeriesReturnValue, SeriesArgument, DataFrameReturnValue, DataFrameArgument
from pandas_type_checks.decorator import pandas_type_check


@pytest.fixture(scope='module')
def data_frame_schema() -> pa.DataFrameSchema:
    return pa.DataFrameSchema({
        'A': pa.Column(np.dtype('float64')),
        'B': pa.Column(np.dtype('int64')),
        'C': pa.Column('string')
    })


def test_data_frame_argument_with_pandera_schema(data_frame_schema, data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False

    @pandas_type_check(DataFrameArgument('arg', data_frame_schema))
    def test_function(arg: pd.DataFrame) -> pd.DataFrame:
        return arg

    result = test_function(data_frame)
    pd.testing.assert_frame_equal(result, data_frame)


def test_data_frame_return_value_with_pandera_schema(data_frame_schema, data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False

    @pandas_type_check(DataFrameReturnValue(data_frame_schema))
    def test_function() -> pd.DataFrame:
        return data_frame

    result = test_function()
    pd.testing.assert_frame_equal(result, data_frame)


def test_type_error_for_data_frame_argument_with_pandera_schema(data_frame_schema, wrong_data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False

    @pandas_type_check(DataFrameArgument('arg', data_frame_schema))
    def test_function(arg: pd.DataFrame) -> pd.DataFrame:
        return arg

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{test_function.__name__}'\n"
                             f"Type error in argument 'arg':\n"
                             f"\tcolumn 'B' not in dataframe\n   A    C\n0  1  foo\n"
                             f"\texpected series 'A' to have type float64, got int64"):
        test_function(wrong_data_frame)


def test_type_error_for_data_frame_return_value_with_pandera_schema(data_frame_schema, wrong_data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False

    @pandas_type_check(DataFrameReturnValue(data_frame_schema))
    def test_function() -> pd.DataFrame:
        return wrong_data_frame

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{test_function.__name__}'\n"
                             f"Type error in return value:\n"
                             f"\tcolumn 'B' not in dataframe\n   A    C\n0  1  foo\n"
                             f"\texpected series 'A' to have type float64, got int64"):
        test_function()


def test_strict_type_check_for_data_frame_argument_with_pandera_schema(data_frame_schema, extended_data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False

    @pandas_type_check(DataFrameArgument('arg', data_frame_schema), strict=True)
    def test_function(arg: pd.DataFrame) -> pd.DataFrame:
        return arg

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{test_function.__name__}'\n"
                             f"Type error in argument 'arg':\n"
                             f"\tFound unspecified column in data frame: 'D'"):
        test_function(extended_data_frame)


def test_strict_type_check_for_data_frame_return_value_with_pandera_schema(data_frame_schema, extended_data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False

    # Enable strict type check mode through keyword argument
    @pandas_type_check(DataFrameReturnValue(data_frame_schema), strict=True)
    def test_function() -> pd.DataFrame:
        return extended_data_frame

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{test_function.__name__}'\n"
                             f"Type error in return value:\n"
                             f"\tFound unspecified column in data frame: 'D'"):
        test_function()
