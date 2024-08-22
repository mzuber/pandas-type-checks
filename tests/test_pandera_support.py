import re

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


@pytest.fixture(scope='module')
def data_frame_schema_with_checks() -> pa.DataFrameSchema:
    return pa.DataFrameSchema({
        'A': pa.Column(np.dtype('float64'), checks=pa.Check.le(10.0)),
        'B': pa.Column(np.dtype('int64'), checks=pa.Check.lt(2)),
        'C': pa.Column('string', checks=pa.Check.str_startswith("f"))
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

    with pytest.raises(TypeError, match=re.escape(
            f"Pandas type error in function '{test_function.__name__}'\n"
            f"Type error in argument 'arg':\n"
            f"\tcolumn 'B' not in dataframe. Columns in dataframe: ['A', 'C']\n"
            f"\texpected series 'A' to have type float64, got int64")):
        test_function(wrong_data_frame)


def test_type_error_for_data_frame_return_value_with_pandera_schema(data_frame_schema, wrong_data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False

    @pandas_type_check(DataFrameReturnValue(data_frame_schema))
    def test_function() -> pd.DataFrame:
        return wrong_data_frame

    with pytest.raises(TypeError, match=re.escape(
            f"Pandas type error in function '{test_function.__name__}'\n"
            f"Type error in return value:\n"
            f"\tcolumn 'B' not in dataframe. Columns in dataframe: ['A', 'C']\n"
            f"\texpected series 'A' to have type float64, got int64")):
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


def test_type_error_for_data_frame_argument_with_pandera_schema_with_checks(data_frame_schema_with_checks, data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False

    @pandas_type_check(DataFrameArgument('arg', data_frame_schema_with_checks))
    def test_function(arg: pd.DataFrame) -> pd.DataFrame:
        return arg

    with pytest.raises(TypeError, match=re.escape(
            f"Pandas type error in function '{test_function.__name__}'\n"
            f"Type error in argument 'arg':\n"
            f"\tColumn 'B' failed element-wise validator number 0: less_than(2) failure cases: 2\n"
            f"\tColumn 'C' failed element-wise validator number 0: str_startswith('f') failure cases: bar")):
        test_function(data_frame)

#


def test_type_error_for_data_frame_return_value_with_pandera_schema_with_checks(data_frame_schema_with_checks,
                                                                                data_frame):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False

    @pandas_type_check(DataFrameReturnValue(data_frame_schema_with_checks))
    def test_function() -> pd.DataFrame:
        return data_frame

    with pytest.raises(TypeError, match=re.escape(
            f"Pandas type error in function '{test_function.__name__}'\n"
            f"Type error in return value:\n"
            f"\tColumn 'B' failed element-wise validator number 0: less_than(2) failure cases: 2\n"
            f"\tColumn 'C' failed element-wise validator number 0: str_startswith('f') failure cases: bar")):
        test_function()


@pytest.fixture(scope='module')
def series_schema() -> pa.SeriesSchema:
    return pa.SeriesSchema(dtype=np.dtype('int64'))


def test_series_argument_with_pandera_schema(series_schema, series):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False

    @pandas_type_check(SeriesArgument('arg', series_schema))
    def test_function(arg: pd.Series) -> pd.Series:
        return arg

    result = test_function(series)
    pd.testing.assert_series_equal(result, series)


def test_series_return_value_with_pandera_schema(series_schema, series):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False

    @pandas_type_check(SeriesReturnValue(series_schema))
    def test_function() -> pd.Series:
        return series

    result = test_function()
    pd.testing.assert_series_equal(result, series)


def test_type_error_for_series_argument_with_pandera_schema(series_schema, wrong_series):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False

    @pandas_type_check(SeriesArgument('arg', series_schema))
    def test_function(arg: pd.Series) -> pd.Series:
        return arg

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{test_function.__name__}'\n"
                             f"Type error in argument 'arg':\n"
                             f"\texpected series 'None' to have type int64, got float64"):
        test_function(wrong_series)


def test_type_error_for_series_return_value_with_pandera_schema(series_schema, wrong_series):
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False

    @pandas_type_check(SeriesReturnValue(series_schema))
    def test_function() -> pd.Series:
        return wrong_series

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{test_function.__name__}'\n"
                             f"Type error in return value:\n"
                             f"\texpected series 'None' to have type int64, got float64"):
        test_function()
