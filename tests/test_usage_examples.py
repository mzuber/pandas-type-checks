import pytest
import pandas as pd
import numpy as np

from pandas_type_checks import config
from pandas_type_checks.core import SeriesArgument, DataFrameReturnValue, DataFrameArgument
from pandas_type_checks.decorator import pandas_type_check


def test_usage_example():
    assert config.enable_type_checks is True
    assert config.strict_type_checks is False
    assert config.log_type_errors is False
    assert config.logger is not None

    @pandas_type_check(
        DataFrameArgument('data', {
            'A': np.dtype('float64'),
            'B': np.dtype('int64'),
            'C': np.dtype('bool')
        }),
        SeriesArgument('filter_values', 'int64'),
        DataFrameReturnValue({
            'B': np.dtype('int64'),
            'C': np.dtype('bool')
        })
    )
    def filter_rows_and_remove_column(data: pd.DataFrame, filter_values: pd.Series) -> pd.DataFrame:
        return data[data['B'].isin(filter_values.values)].drop('A', axis=1)

    # Apply test function to arguments with the expected structure
    test_data = pd.DataFrame({
        'A': pd.Series(1, index=list(range(4)), dtype='float64'),
        'B': np.array([1, 2, 3, 4], dtype='int64'),
        'C': np.array([True] * 4, dtype='bool')
    })
    test_filter_values = pd.Series([3, 4], dtype='int64')
    result = filter_rows_and_remove_column(test_data, test_filter_values)

    assert result is not None
    assert result.shape == (2, 2)

    # Apply function to filter values series with wrong type
    test_filter_values_with_wrong_type = pd.Series([3, 4], dtype='int32')

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{filter_rows_and_remove_column.__name__}'\n"
                             f"Type error in argument 'filter_values':\n"
                             f"\tExpected Series of type 'int64' but found type 'int32'"):
        filter_rows_and_remove_column(test_data, test_filter_values_with_wrong_type)

    # Apply function to data frame with wrong type and missing column
    test_data_with_wrong_type_and_missing_column = pd.DataFrame({
        'A': pd.Series(1, index=list(range(4)), dtype='float64'),
        'B': np.array([1, 2, 3, 4], dtype='int32')
    })

    with pytest.raises(TypeError,
                       match=f"Pandas type error in function '{filter_rows_and_remove_column.__name__}'\n"
                             f"Type error in argument 'data':\n"
                             f"\tExpected type 'int64' for column B' but found type 'int32'\n"
                             f"\tMissing column in DataFrame: 'C'\n"
                             f"Type error in return value:\n"
                             f"\tExpected type 'int64' for column B' but found type 'int32'\n"
                             f"\tMissing column in DataFrame: 'C'"):
        filter_rows_and_remove_column(test_data_with_wrong_type_and_missing_column, test_filter_values)
