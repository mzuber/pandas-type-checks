from typing import List, Dict, Optional, Any

import pandas as pd
from pandera.errors import SchemaErrors, SchemaError


class PandasTypeCheckError(object):
    """
    Error-related information when type checking a Pandas data frame or series.

    Attributes:
        error_msg: Error message
        expected_type: (Optional) Expected type for the data frame column or series
        given_type: (Optional) Actual type of the data frame column or series
        column_name: (Optional) Data frame column name, set if error occurred
                     when type checking a column of a data frame
        pandera_failure_cases: (Optional) Data frame containing the failure cases found
                               by the Pandera data frame or series validation.
                               This attribute effectively contains the 'failure_cases'
                               property of a
    """

    def __init__(self, error_msg: str,
                 expected_type: Optional[Any] = None,
                 given_type: Optional[Any] = None,
                 column_name: Optional[str] = None,
                 pandera_failure_cases: Optional[pd.DataFrame] = None):
        self.error_msg = error_msg
        self.expected_type = expected_type
        self.given_type = given_type
        self.column_name = column_name
        self.pandera_failure_cases = pandera_failure_cases


def build_exception_message(func_name: str,
                            arg_type_check_errors: Dict[str, List[PandasTypeCheckError]],
                            ret_value_type_check_errors: List[PandasTypeCheckError]) -> str:
    """
    Build a formatted error message for all the given type check errors.

    Args:
        func_name: Name of the function in which the typer errors occurred
        arg_type_check_errors: Dictionary containing the type check errors found for all
          arguments of an annotated function
        ret_value_type_check_errors: list containing the type check errors found for the
          return value of an annotated function

    Returns:
        A formatted string with the full error message containing all given type check errors
    """
    exec_msg: List[str] = [f"Pandas type error in function '{func_name}'"]

    # Add argument type check errors to exception message
    for arg_name, type_check_errors in arg_type_check_errors.items():
        type_check_error_msgs = ['\t' + err.error_msg for err in type_check_errors]
        exec_msg.append(f"Type error in argument '{arg_name}':\n" + "\n".join(type_check_error_msgs))

    # Add return value type check errors to exception message
    if ret_value_type_check_errors:
        type_check_error_msgs = ['\t' + err.error_msg for err in ret_value_type_check_errors]
        exec_msg.append("Type error in return value:\n" + "\n".join(type_check_error_msgs))

    return "\n".join(exec_msg)


def pandera_schema_errors_to_type_check_errors(schema_errors: SchemaErrors) -> List[PandasTypeCheckError]:
    """
    Transform a Pandera ``SchemaErrors`` exception into the error abstraction of this library.

    Args:
        schema_errors: Pandera ``SchemaErrors`` exception raised from validating
          a Pandera ``DataFrameSchema`` or ``SeriesSchema``

    Returns: A list containing a type check error for each schema error
    """
    type_check_errors: List[PandasTypeCheckError] = []

    for schema_error_dict in schema_errors.schema_errors:
        schema_error: SchemaError = schema_error_dict['error']

        # Check if error relates to a specific column
        column_name: Optional[str] = None
        if schema_error.failure_cases is not None:
            if "column" in schema_error.failure_cases:
                column_name = schema_error.failure_cases["column"]
            else:
                column_name = (
                    schema_error.schema.name
                    if schema_error == "schema_component_check"
                    else None
                )

        type_check_error = PandasTypeCheckError(error_msg=str(schema_error), column_name=column_name)
        type_check_errors.append(type_check_error)

    return type_check_errors