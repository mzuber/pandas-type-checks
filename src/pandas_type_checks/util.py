from typing import List, Dict

from pandas_type_checks.core import PandasTypeCheckError


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
