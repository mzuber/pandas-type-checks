Pandas Type Checks
==================

[![Build Status](https://dev.azure.com/martin-zuber/pandas-type-checks/_apis/build/status/mzuber.pandas-type-checks?branchName=main)](https://dev.azure.com/martin-zuber/pandas-type-checks/_build/latest?definitionId=1&branchName=main)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mzuber_pandas-type-checks&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mzuber_pandas-type-checks)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=mzuber_pandas-type-checks&metric=coverage)](https://sonarcloud.io/summary/new_code?id=mzuber_pandas-type-checks)

Structural type checking for Pandas data frames and series.

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
TypeError: Pandas type error
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
TypeError: Pandas type error
Type error in argument 'data':
    Expected type 'int64' for column B' but found type 'int32'
    Missing column in DataFrame: 'C'
Type error in return value:
    Expected type 'int64' for column B' but found type 'int32'
    Missing column in DataFrame: 'C'
```

References
----------

* [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
* [Python Packaging User Guide](https://packaging.python.org/en/latest/)

