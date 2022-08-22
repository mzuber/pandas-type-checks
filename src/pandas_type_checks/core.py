from typing import Dict, Any, Union, Optional, List, Type
import logging

import pandas as pd
import numpy as np

from pandas.core.dtypes.base import ExtensionDtype


default_logger = logging.getLogger('pandas_type_checks')


class PandasTypeCheckConfiguration(object):
    """
    A class for global configuration of the Pandas type check functionality.

    Attributes:
        enable_type_checks (bool): Flag for enabling/disabling type checks for specified arguments and return
            values. Defaults to True. This flag can be used to globally enable or disable the type checker in
            certain environments.
        strict_type_checks (bool): Flag for strict type check mode. Defaults to False.
            If strict type checking is enabled data frames cannot contain columns which are not part of the type
            specification against which they are checked. Non-strict type checking in that sense allows a form of
            structural subtyping for data frames.
        log_type_errors (bool): Flag indicating that type errors for Pandas dataframes or series values should be
            logged instead of raising a 'TypeError' exception. Defaults to False.
        logger (logging.Logger): Logger to be used for logging type errors when 'log_type_errors' flag is enabled.
    """

    def __init__(self, enable_type_checks: bool = True,
                 strict_type_checks: bool = False,
                 log_type_errors: bool = False,
                 logger: logging.Logger = default_logger):
        self.enable_type_checks = enable_type_checks
        self.strict_type_checks = strict_type_checks
        self.log_type_errors = log_type_errors
        self.logger = logger


config = PandasTypeCheckConfiguration()


class PandasTypeCheckError(object):
    """
    Error-related information when type checking a Pandas data frame or series.

    Attributes:
        error_msg: Error message
        expected_type: (Optional) Expected type for the data frame column or series
        given_type: (Optional) Actual type of the data frame column or series
        column_name: (Optional) Data frame column name, set if error occurred
                     when type checking a column of a data frame
    """

    def __init__(self, error_msg: str,
                 expected_type: Optional[Any] = None,
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

    def type_check(self, series: pd.Series) -> List[PandasTypeCheckError]:
        """Type check the given Pandas Series against this type specification.

        Compare the 'dtype' of the given Pandas Series with the expected 'dtype' defined in this type specification.

        Args:
            series: The Pandas Series to be type checked against this type check marker

        Returns:
            A list of all type check errors which occurred when type checking the given Pandas Series.
            If the type check succeeds an empty list will be returned.
        """
        type_check_errors: List[PandasTypeCheckError] = []

        if series.dtype != self.dtype:
            error_msg = f"Expected Series of type '{self.dtype}' but found type '{series.dtype}'"
            type_check_error = PandasTypeCheckError(error_msg=error_msg,
                                                    expected_type=self.dtype,
                                                    given_type=series.dtype)
            type_check_errors.append(type_check_error)

        return type_check_errors


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

    def type_check(self, data_frame: pd.DataFrame, strict: bool) -> List[PandasTypeCheckError]:
        """Type check the structure of the given data frame against this type specification.

        Args:
            data_frame: Pandas data frame to type check against this type specification
            strict: Flag for strict type check mode. If strict type checking is enabled the given dataframe
                cannot contain columns which are not part of this type specification. Disabling strict type
                checking in that sense allows a form of structural subtyping for data frames.

        Returns:
            A list of errors which occurred when type checking the given data frame.
            If and only if no type errors are found, this method returns an empty list.
        """
        type_check_errors: List[PandasTypeCheckError] = []
        reference_columns = list(self.dtype.keys())
        reference_data_frame = pd.DataFrame(columns=reference_columns).astype(self.dtype)

        if strict:
            unspecified_columns = set(data_frame.columns).difference(reference_columns)
            if unspecified_columns:
                unspecified_column_errors = [
                    PandasTypeCheckError(error_msg=f"Found unspecified column in data frame: '{unspecified_column}'",
                                         given_type=data_frame[unspecified_column].dtype,
                                         column_name=unspecified_column)
                    for unspecified_column in unspecified_columns
                ]
                type_check_errors.extend(unspecified_column_errors)

        for column_name in reference_columns:
            expected_column_type = reference_data_frame[column_name].dtype

            if column_name not in data_frame.columns:
                type_check_error = PandasTypeCheckError(error_msg=f"Missing column in DataFrame: '{column_name}'",
                                                        expected_type=expected_column_type,
                                                        column_name=column_name)
                type_check_errors.append(type_check_error)
            else:
                column_type = data_frame[column_name].dtype
                if column_type != expected_column_type:
                    error_msg = (f"Expected type '{expected_column_type}' for column "
                                 f"{column_name}' but found type '{column_type}'")
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
