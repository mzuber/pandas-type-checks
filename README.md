Pandas Type Checks
==================

[![Build Status](https://dev.azure.com/martin-zuber/pandas-type-checks/_apis/build/status/mzuber.pandas-type-checks?branchName=main)](https://dev.azure.com/martin-zuber/pandas-type-checks/_build/latest?definitionId=1&branchName=main)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mzuber_pandas-type-checks&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mzuber_pandas-type-checks)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=mzuber_pandas-type-checks&metric=coverage)](https://sonarcloud.io/summary/new_code?id=mzuber_pandas-type-checks)

A Python library providing means for structural type checking of Pandas data frames and series:
- A decorator `pandas_type_check` for specifying and checking the structure of Pandas `DataFrame` and `Series`
  arguments and return values of a function.
- Support for "non-strict" type checking. In this mode data frames can contain columns which are not part of the type
  specification against which they are checked. Non-strict type checking in that sense allows a form of structural
  subtyping for data frames.
- Configuration options to raise exceptions for type errors or alternatively log them.
- Configuration option to globally enable/disable the type checks. This allows users to enable the type checking
  functionality in e.g. only testing environments.

This library focuses on providing utilities to check the structure (i.e. columns and their types) of Pandas data frames
and series arguments and return values of functions. For checking individual data frame and series values, including
formulating more sophisticated constraints on column values, [Pandera](https://github.com/unionai-oss/pandera) is a
great alternative.

Installation
------------

Packages for all released versions are available at the
[Python Package Index (PyPI)](https://pypi.org/project/pandas-type-checks) and can be installed with `pip`:

```
pip install pandas-type-checks
```

Usage Example
-------------

The function `filter_rows_and_remove_column` is annotated with type check hints for the Pandas `DataFrame` and `Series`
arguments and return value of the function:

```python
import pandas as pd
import numpy as np
import pandas_type_checks as pd_types

@pd_types.pandas_type_check(
    pd_types.DataFrameArgument('data', {
        'A': np.dtype('float64'),
        'B': np.dtype('int64'),
        'C': np.dtype('bool')
    }),
    pd_types.SeriesArgument('filter_values', 'int64'),
    pd_types.DataFrameReturnValue({
        'B': np.dtype('int64'),
        'C': np.dtype('bool')
    })
)
def filter_rows_and_remove_column(data: pd.DataFrame, filter_values: pd.Series) -> pd.DataFrame:
    return data[data['B'].isin(filter_values.values)].drop('A', axis=1)
```

Applying the function `filter_rows_and_remove_column` to a filter values `Series` with the wrong type will result in a
`TypeError` exception with a detailed type error message:

```python
test_data = pd.DataFrame({
    'A': pd.Series(1, index=list(range(4)), dtype='float64'),
    'B': np.array([1, 2, 3, 4], dtype='int64'),
    'C': np.array([True] * 4, dtype='bool')
})
test_filter_values_with_wrong_type = pd.Series([3, 4], dtype='int32')

filter_rows_and_remove_column(test_data, test_filter_values_with_wrong_type)
```

```
TypeError: Pandas type error in function 'filter_rows_and_remove_column'
Type error in argument 'filter_values':
	Expected Series of type 'int64' but found type 'int32'
```

Applying the function `filter_rows_and_remove_column` to a data frame with a wrong column type and a missing column
will result in a `TypeError` exception with a detailed type error message:

```python
test_data_with_wrong_type_and_missing_column = pd.DataFrame({
    'A': pd.Series(1, index=list(range(4)), dtype='float64'),
    'B': np.array([1, 2, 3, 4], dtype='int32')
})
test_filter_values = pd.Series([3, 4], dtype='int64')

filter_rows_and_remove_column(test_data_with_wrong_type_and_missing_column, test_filter_values)
```

```
TypeError: Pandas type error in function 'filter_rows_and_remove_column'
Type error in argument 'data':
    Expected type 'int64' for column B' but found type 'int32'
    Missing column in DataFrame: 'C'
Type error in return value:
    Expected type 'int64' for column B' but found type 'int32'
    Missing column in DataFrame: 'C'
```

Configuration
-------------

The global configuration object `pandas_type_checks.config` can be used to configure the behavior of the library:
- `config.enable_type_checks` (`bool`): Flag for enabling/disabling type checks for specified arguments and return
  values. This flag can be used to globally enable or disable the type checker in certain environments.

  Default: `True`
- `config.strict_type_checks` (`bool`): Flag for strict type check mode. If strict type checking is enabled data frames
  cannot contain columns which are not part of the type specification against which they are checked. Non-strict type
  checking in that sense allows a form of structural subtyping for data frames.

  Default: `False`
- `config.log_type_errors` (`bool`): Flag indicating that type errors for Pandas dataframes or series values should be
  logged instead of raising a `TypeError` exception. Type errors will be logged with log level `ERROR`.

  Default: `False`
- `config.logger` (`logging.Logger`): Logger to be used for logging type errors when the `log_type_errors` flag is enabled.
  When no logger is specified via the configuration a built-in default logger is used.

References
----------

* [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
* [Python Packaging User Guide](https://packaging.python.org/en/latest/)

