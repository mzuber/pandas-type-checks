from typing import Dict, Any

import pytest
import pandas as pd
import numpy as np


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
        'A': [1.0],
        'B': [1],
        'C': ['foo']
    }).astype(data_frame_type)


@pytest.fixture(scope='session')
def series_type() -> np.dtype:
    return np.dtype('int64')


@pytest.fixture(scope='session')
def series(series_type) -> pd.Series:
    return pd.Series([1, 2, 3], dtype=series_type)
