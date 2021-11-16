import inspect
from functools import wraps
from typing import List, Dict, Union, Type

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

            def check_pandas_arg(decorator_arg: Union[DataFrameArgument, SeriesArgument],
                                 expected_function_arg_type: Union[Type[pd.DataFrame], Type[pd.Series]]
                                 ) -> List[PandasTypeCheckError]:
                """Type check Pandas DataFrame and Series arguments."""
                # Check if wrapped function has an argument with the given name
                if decorator_arg.name in func_spec.args:
                    # Check if argument of wrapped function is a DataFrame
                    func_arg = func_args[func_spec.args.index(decorator_arg.name)]
                    if isinstance(func_arg, expected_function_arg_type):
                        # Compare DataFrame structure of function argument with
                        # the expected structure given in the type check marker
                        return decorator_arg.type_check(func_arg, strict=strict)
                    else:
                        raise PandasTypeCheckDecoratorException(
                            f"Argument type mismatch. Expected argument '{decorator_arg.name}' of decorated function "
                            f"'{func.__name__}' to be of type '{expected_function_arg_type.__qualname__}' but found "
                            f"value of type '{type(func_arg).__qualname__}'."
                        )
                else:
                    raise PandasTypeCheckDecoratorException(
                        f"Decorated function '{func.__name__}' has no parameter '{decorator_arg.name}'."
                    )

            # Perform type checks for Pandas arguments and return value defined in decorator
            for arg in args:
                if isinstance(arg, DataFrameArgument):
                    arg_type_check_errors: List[PandasTypeCheckError] = check_pandas_arg(arg, pd.DataFrame)
                    if arg_type_check_errors:
                        type_check_errors[arg.name] = arg_type_check_errors
                elif isinstance(arg, SeriesArgument):
                    arg_type_check_errors: List[PandasTypeCheckError] = check_pandas_arg(arg, pd.Series)
                    if arg_type_check_errors:
                        type_check_errors[arg.name] = arg_type_check_errors
                elif isinstance(arg, (DataFrameReturnValue, SeriesReturnValue)):
                    pass
                else:
                    raise PandasTypeCheckDecoratorException(
                        f"Unsupported argument for decorator. Expected argument of type "
                        f"'{DataFrameArgument.__qualname__}', '{DataFrameReturnValue.__qualname__}', "
                        f"'{SeriesArgument.__qualname__}', or '{SeriesReturnValue.__qualname__}' but "
                        f"found type '{type(arg).__qualname__}'."
                    )

            # Raise type error if any type check errors were found for any of the Pandas arguments or return value
            if type_check_errors:
                # TODO: Build error message containing all collected type check errors
                error_msg = str(type_check_errors)
                raise TypeError(error_msg)

            return func(*func_args, **func_kwargs)

        return pandas_type_check_wrapper

    return pandas_type_check_decorator
