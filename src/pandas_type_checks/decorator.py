from functools import wraps


def pandas_type_check(*args, **kwargs):

    def pandas_type_check_decorator(func):

        @wraps(func)
        def pandas_type_check_wrapper(*func_args, **func_kwargs):
            # TODO: type check data frame args
            return func(*func_args, **func_kwargs)

        return pandas_type_check_wrapper

    return pandas_type_check_decorator
