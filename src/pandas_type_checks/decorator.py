import inspect
from functools import wraps
from typing import List, Dict, Optional, Union

import pandas as pd

from pandas_type_checks.core import DataFrameArgument, DataFrameReturnValue, SeriesArgument, SeriesReturnValue
from pandas_type_checks.core import PandasTypeCheckError
from pandas_type_checks.core import config as pandas_type_checks_config
from pandas_type_checks.util import build_exception_message


class PandasTypeCheckDecoratorException(Exception):
    """An exception class for errors related to the Pandas type check decorator."""
    pass


def pandas_type_check(*args, **kwargs):
    """A decorator for type checking Pandas data frame and series arguments and return value of a function.

    Args:
        *args: Type specifications for Pandas data frame and series arguments and return value of the decorated function

    Keyword Arguments:
        strict (bool): Flag for strict type check mode. Keyword argument overrides global configuration.
            If strict type checking is enabled data frames cannot contain columns which are not part of the type
            specification against which they are checked. Non-strict type checking in that sense allows a form of
            structural subtyping for data frames.

    Raises:
        PandasTypeCheckDecoratorException: An error occurred specifying the Pandas types for the arguments and return
            value of the decorated function
        TypeError: Errors occurred when type checking the Pandas data frame and series arguments and return value of
            the decorated function against the given type specification
    """

    def pandas_type_check_decorator(func):

        @wraps(func)
        def pandas_type_check_wrapper(*func_args, **func_kwargs):
            # Get argument specification of wrapped function
            func_spec = inspect.getfullargspec(func)
            func_name = func.__name__

            # Evaluate query args of the decorator
            strict: bool = kwargs.get('strict', pandas_type_checks_config.strict_type_checks)

            # Argument name -> type check errors found for given argument
            arg_type_check_errors: Dict[str, List[PandasTypeCheckError]] = {}

            def check_pandas_arg(decorator_arg: Union[DataFrameArgument, SeriesArgument]) -> List[PandasTypeCheckError]:
                """Type check Pandas DataFrame and Series arguments."""
                # Check if wrapped function has an argument with the given name
                if decorator_arg.name in func_spec.args:
                    # Check if argument of wrapped function is a DataFrame
                    func_arg = func_args[func_spec.args.index(decorator_arg.name)]
                    if isinstance(decorator_arg, DataFrameArgument) and isinstance(func_arg, pd.DataFrame):
                        # Compare DataFrame structure of function argument with
                        # the expected structure given in the type check marker
                        return decorator_arg.type_check(func_arg, strict=strict)
                    elif isinstance(decorator_arg, SeriesArgument) and isinstance(func_arg, pd.Series):
                        # Compare Series type of function argument with
                        # the expected type given in the type check marker
                        return decorator_arg.type_check(func_arg)
                    else:
                        raise PandasTypeCheckDecoratorException(
                            f"Argument type mismatch. Expected argument '{decorator_arg.name}' of decorated function "
                            f"'{func_name}' to be of type '{decorator_arg.corresponding_pandas_type.__qualname__}' "
                            f"but found value of type '{type(func_arg).__qualname__}'."
                        )
                else:
                    raise PandasTypeCheckDecoratorException(
                        f"Decorated function '{func_name}' has no parameter '{decorator_arg.name}'."
                    )

            # Perform type checks for Pandas arguments defined in decorator
            ret_value_type_marker: Optional[Union[DataFrameReturnValue, SeriesReturnValue]] = None
            if pandas_type_checks_config.enable_type_checks:
                for arg in args:
                    if isinstance(arg, (DataFrameArgument, SeriesArgument)):
                        dataframe_arg_type_check_errors: List[PandasTypeCheckError] = check_pandas_arg(arg)
                        if dataframe_arg_type_check_errors:
                            arg_type_check_errors[arg.name] = dataframe_arg_type_check_errors
                    elif isinstance(arg, (DataFrameReturnValue, SeriesReturnValue)):
                        if not ret_value_type_marker:
                            ret_value_type_marker = arg
                        else:
                            raise PandasTypeCheckDecoratorException(
                                "Only one return value type marker allowed in type check decorator."
                            )
                    else:
                        raise PandasTypeCheckDecoratorException(
                            f"Unsupported argument for decorator. Expected argument of type "
                            f"'{DataFrameArgument.__qualname__}', '{DataFrameReturnValue.__qualname__}', "
                            f"'{SeriesArgument.__qualname__}', or '{SeriesReturnValue.__qualname__}' but "
                            f"found type '{type(arg).__qualname__}'."
                        )

            # Execute wrapped function
            ret_value = func(*func_args, **func_kwargs)

            # Perform type checks for Pandas return value defined in decorator
            if pandas_type_checks_config.enable_type_checks:
                ret_value_type_check_errors: List[PandasTypeCheckError] = []
                if ret_value_type_marker:
                    if isinstance(ret_value_type_marker, DataFrameReturnValue) and isinstance(ret_value, pd.DataFrame):
                        # Compare DataFrame structure of return value with the
                        # expected structure given in the type check marker
                        ret_value_type_check_errors += ret_value_type_marker.type_check(ret_value, strict=strict)
                    elif isinstance(ret_value_type_marker, SeriesReturnValue) and isinstance(ret_value, pd.Series):
                        # Compare Series type of return value with the
                        # expected type given in the type check marker
                        ret_value_type_check_errors += ret_value_type_marker.type_check(ret_value)
                    else:
                        raise PandasTypeCheckDecoratorException(
                            f"Return value type mismatch. "
                            f"Expected return value of decorated function '{func_name}' to be of type "
                            f"'{ret_value_type_marker.corresponding_pandas_type.__qualname__}' but found "
                            f"value of type '{type(ret_value).__qualname__}'."
                        )

                # Raise type error if any type check errors were found for any of the Pandas arguments or return value
                if arg_type_check_errors or ret_value_type_check_errors:
                    error_msg = build_exception_message(func_name, arg_type_check_errors, ret_value_type_check_errors)
                    # Log type errors for Pandas values if the corresponding configuration flag is set
                    if pandas_type_checks_config.log_type_errors:
                        pandas_type_checks_config.logger.error(error_msg)
                    else:
                        raise TypeError(error_msg)

            return ret_value

        return pandas_type_check_wrapper

    return pandas_type_check_decorator
