from typing import Dict, Any

import pytest
import pandas as pd
import numpy as np

from pandas_type_checks.core import config as pandas_type_checks_config


@pytest.fixture(autouse=True)
def before_all():
    # Make sure type checking of Pandas data frames and series
    # is enabled in the global configuration for each test
    pandas_type_checks_config.enable_type_checks = True

    # Use non-strict type checking mode as default for each test
    pandas_type_checks_config.strict_type_checks = False

    # Raise exceptions for type errors as default for each test
    pandas_type_checks_config.log_type_errors = False

    yield  # run test function


@pytest.fixture(scope='session')
def data_frame_type() -> Dict[str, Any]:
    return {
        'A': np.dtype('float64'),
        'B': np.dtype('int64'),
        'C': 'string'
    }


@pytest.fixture(scope='session')
def data_frame(data_frame_type) -> pd.DataFrame:
    return pd.DataFrame({
        'A': [1.0, 2.0],
        'B': [1, 2],
        'C': ['foo', 'bar']
    }).astype(data_frame_type)


@pytest.fixture(scope='session')
def wrong_data_frame_type() -> Dict[str, Any]:
    return {
        'A': np.dtype('int64'),
        'C': 'string'
    }


@pytest.fixture(scope='session')
def wrong_data_frame(wrong_data_frame_type) -> pd.DataFrame:
    return pd.DataFrame({
        'A': [1],
        'C': ['foo']
    }).astype(wrong_data_frame_type)


@pytest.fixture(scope='session')
def extended_data_frame_type() -> Dict[str, Any]:
    return {
        'A': np.dtype('float64'),
        'B': np.dtype('int64'),
        'C': 'string',
        'D': 'string'
    }


@pytest.fixture(scope='session')
def extended_data_frame(extended_data_frame_type) -> pd.DataFrame:
    return pd.DataFrame({
        'A': [1.0, 2.0],
        'B': [1, 2],
        'C': ['foo', 'bar'],
        'D': ['baz', 'baz']
    }).astype(extended_data_frame_type)


@pytest.fixture(scope='session')
def series_type() -> np.dtype:
    return np.dtype('int64')


@pytest.fixture(scope='session')
def wrong_series_type() -> np.dtype:
    return np.dtype('float64')


@pytest.fixture(scope='session')
def series(series_type) -> pd.Series:
    return pd.Series([1, 2, 3], dtype=series_type)


@pytest.fixture(scope='session')
def wrong_series(wrong_series_type) -> pd.Series:
    return pd.Series([1.0, 2.0, 3.0], dtype=wrong_series_type)
