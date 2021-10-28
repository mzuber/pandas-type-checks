import inspect
from functools import wraps
from typing import List, Dict

import pandas as pd

from pandas_type_checks.core import DataFrameArgument, DataFrameReturnValue, SeriesArgument, SeriesReturnValue
from pandas_type_checks.core import PandasTypeCheckError


class PandasTypeCheckDecoratorException(Exception):
    """An exception class for errors related to the Pandas type check decorator."""
    pass


def pandas_type_check(*args, **kwargs):

    def pandas_type_check_decorator(func):

        @wraps(func)
        def pandas_type_check_wrapper(*func_args, **func_kwargs):
            # Get argument specification of wrapped function
            func_spec = inspect.getfullargspec(func)

            # Evaluate query args of the decorator
            strict: bool = kwargs.get('strict', False)

            # Argument name -> type check errors found for given argument
            type_check_errors: Dict[str, List[PandasTypeCheckError]] = {}

            for arg in args:
                if isinstance(arg, (DataFrameArgument, SeriesArgument)):
                    # Check if wrapped function has an argument with the given name
                    if arg.name in func_spec.args:
                        # Check if argument of wrapped function is a DataFrame or Series
                        func_arg = func_args[func_spec.args.index(arg.name)]
                        if not isinstance(func_arg, (pd.DataFrame, pd.Series)):
                            raise PandasTypeCheckDecoratorException(
                                f"Argument type mismatch. Expected argument '{arg.name}' of decorated "
                                f"function '{func.__name__}' to be a Pandas DataFrame or Series but "
                                f"found value of type '{str(type(func_arg))}'."
                            )

                        # Compare DataFrame/Series structure of function argument
                        # with the expected structure given in the type check marker
                        arg_type_check_errors: List[PandasTypeCheckError] = arg.type_check(func_arg, strict=strict)
                        if arg_type_check_errors:
                            type_check_errors[arg.name] = arg_type_check_errors
                    else:
                        raise PandasTypeCheckDecoratorException(
                            f"Decorated function '{func.__name__}' has no parameter '{arg.name}'."
                        )
                elif isinstance(arg, (DataFrameReturnValue, SeriesReturnValue)):
                    pass
                else:
                    raise PandasTypeCheckDecoratorException(
                        f"Unsupported argument for decorator. Expected argument of type "
                        f"'DataFrameArgument', 'DataFrameReturnValue', 'SeriesArgument', or "
                        f"'SeriesReturnValue' but found type '{str(type(arg))}'."
                    )

            # Raise type error if any type check errors were found for any of the Pandas arguments or return value
            if type_check_errors:
                # TODO: Build error message containing all collected type check errors
                error_msg = str(type_check_errors)
                raise TypeError(error_msg)

            return func(*func_args, **func_kwargs)

        return pandas_type_check_wrapper

    return pandas_type_check_decorator
