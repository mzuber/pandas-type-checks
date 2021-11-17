from typing import Dict, Any, Union, Optional, List, Type

import pandas as pd
import numpy as np

from pandas.core.dtypes.base import ExtensionDtype


class PandasTypeCheckError(object):
    """
    Error-related information when type checking a Pandas data frame or series.

    Attributes:
        error_msg: Error message
        expected_type: Expected type for the data frame column or series
        given_type: (Optional) Actual type of the data frame column or series
        column_name: (Optional) Data frame column name, set if error occurred
                     when type checking a column of a data frame
    """

    def __init__(self, error_msg: str, expected_type: Any,
                 given_type: Optional[Any] = None,
                 column_name: Optional[str] = None):
        self.error_msg = error_msg
        self.expected_type = expected_type
        self.given_type = given_type
        self.column_name = column_name


class SeriesReturnValue(object):
    """
    The expected data type for a Pandas Series return value of a function or method.

    Attributes:
        dtype: Expected data type for the Series.
    """

    def __init__(self, dtype: Union[str, np.dtype, ExtensionDtype]):
        self.dtype = dtype

    @property
    def corresponding_pandas_type(self) -> Type:
        """Get the Pandas type corresponding to this type check decorator argument."""
        return pd.Series

    def type_check(self, series: pd.Series, strict: bool = False) -> List[PandasTypeCheckError]:
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
            Use a single numpy.dtype or Python type to mark that all columns in the DataFrame have the same type.
            Alternatively, use {col: dtype, ...}, where 'col' is a column label and 'dtype' is a numpy.dtype or
            Python type to mark that one or more of the DataFrame's columns have the given column-specific types.
    """

    def __init__(self, dtype: Dict[str, Any]):
        self.dtype = dtype

    @property
    def corresponding_pandas_type(self) -> Type:
        """Get the Pandas type corresponding to this type check decorator argument."""
        return pd.DataFrame

    def type_check(self, data_frame: pd.DataFrame, strict: bool = False) -> List[PandasTypeCheckError]:

        type_check_errors: List[PandasTypeCheckError] = []
        reference_data_frame = pd.DataFrame(columns=self.dtype.keys()).astype(self.dtype)

        for column_name in self.dtype.keys():
            expected_column_type = reference_data_frame[column_name].dtype

            if column_name not in data_frame.columns:
                type_check_error = PandasTypeCheckError(error_msg=f"Missing column in DataFrame: '{column_name}'",
                                                        expected_type=expected_column_type,
                                                        column_name=column_name)
                type_check_errors.append(type_check_error)
            else:
                column_type = data_frame[column_name].dtype
                if column_type != expected_column_type:
                    error_msg = f"""Expected type '{expected_column_type}' for column  "
                                    '{column_name}' but found type '{column_type}'"""
                    type_check_error = PandasTypeCheckError(error_msg=error_msg,
                                                            expected_type=expected_column_type,
                                                            given_type=column_type,
                                                            column_name=column_name)
                    type_check_errors.append(type_check_error)

        return type_check_errors


class DataFrameArgument(DataFrameReturnValue):
    """
    The expected data type for a Pandas DataFrame argument of a function or method.

    Attributes:
        name:
            Name of the argument.
        dtype:
            Expected data type for the DataFrame.

            Data type, or dict of column name -> data type
            Use a single numpy.dtype or Python type to mark that all columns in the DataFrame have the same type.
            Alternatively, use {col: dtype, ...}, where 'col' is a column label and 'dtype' is a numpy.dtype or
            Python type to mark that one or more of the DataFrame's columns have the given column-specific types.
    """

    def __init__(self, name: str, dtype: Dict[str, Any]):
        super().__init__(dtype)
        self.name = name
