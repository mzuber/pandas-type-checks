from typing import Dict, Any, Union

import pandas as pd
import numpy as np

from pandas.core.dtypes.base import ExtensionDtype


class SeriesReturnValue(object):
    """
    The expected data type for a Pandas Series return value of a function or method.

    Attributes:
        dtype: Expected data type for the Series.
    """

    def __init__(self, dtype: Union[str, np.dtype, ExtensionDtype]):
        self.dtype = dtype

    def type_check(self, series: pd.Series, strict: bool = False):
        pass


class SeriesArgument(SeriesReturnValue):
    """
    The expected data type for a Pandas Series argument of a function or method.

    Attributes:
        name: Name of the argument.
        dtype: Expected data type for the Series.
    """

    def __init__(self, name: str, dtype: Union[str, np.dtype, ExtensionDtype]):
        super().__init__(dtype)
        self.name = name


class DataFrameReturnValue(object):
    """
    Expected data type for a Pandas DataFrame return value of a function or method.

    Attributes:
        dtype:
            Expected data type for the DataFrame.

            Data type, or dict of column name -> data type
            Use a single numpy.dtype or Python type to mark that all columns ih the DataFrame have the same type.
            Alternatively, use {col: dtype, ...}, where 'col' is a column label and 'dtype' is a numpy.dtype or
            Python type to mark that one or more of the DataFrame's columns have the given column-specific types.
    """

    def __init__(self, dtype: Dict[str, Any]):
        self.dtype = dtype

    def type_check(self, data_frame: pd.DataFrame, strict: bool = False):
        pass


class DataFrameArgument(DataFrameReturnValue):
    """
    The expected data type for a Pandas DataFrame argument of a function or method.

    Attributes:
        name:
            Name of the argument.
        dtype:
            Expected data type for the DataFrame.

            Data type, or dict of column name -> data type
            Use a single numpy.dtype or Python type to mark that all columns ih the DataFrame have the same type.
            Alternatively, use {col: dtype, ...}, where 'col' is a column label and 'dtype' is a numpy.dtype or
            Python type to mark that one or more of the DataFrame's columns have the given column-specific types.
    """

    def __init__(self, name: str, dtype: Dict[str, Any]):
        super().__init__(dtype)
        self.name = name
