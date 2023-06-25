from typing import List, Optional

from pandera.errors import SchemaErrors

from pandas_type_checks.errors import PandasTypeCheckError


def pandera_schema_errors_to_type_check_errors(schema_errors: SchemaErrors) -> List[PandasTypeCheckError]:
    """
    Transform a Pandera ``SchemaErrors`` exception into the error abstraction of this library.

    Args:
        schema_errors: Pandera ``SchemaErrors`` exception raised from validating
          a Pandera ``DataFrameSchema`` or ``SeriesSchema``

    Returns: A list containing a type check error for each schema error
    """
    type_check_errors: List[PandasTypeCheckError] = []

    for schema_error in schema_errors.schema_errors:
        # Check if error relates to a specific column
        column_name: Optional[str] = None
        if schema_error.failure_cases is not None:
            column_name = schema_error.schema.name if schema_error == "schema_component_check" else None

        type_check_error = PandasTypeCheckError(error_msg=str(schema_error), column_name=column_name)
        type_check_errors.append(type_check_error)

    return type_check_errors
