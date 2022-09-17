=============
Usage Example
=============

The function ``filter_rows_and_remove_column`` is annotated with type check hints for the Pandas ``DataFrame`` and
``Series`` arguments and return value of the function:

.. code-block:: python

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


Applying the function ``filter_rows_and_remove_column`` to a filter values ``Series`` with the wrong type will result
in a ``TypeError`` exception with a detailed type error message:

.. code-block:: python

    test_data = pd.DataFrame({
        'A': pd.Series(1, index=list(range(4)), dtype='float64'),
        'B': np.array([1, 2, 3, 4], dtype='int64'),
        'C': np.array([True] * 4, dtype='bool')
    })
    test_filter_values_with_wrong_type = pd.Series([3, 4], dtype='int32')

    filter_rows_and_remove_column(test_data, test_filter_values_with_wrong_type)

.. code-block:: none

    TypeError: Pandas type error in function 'filter_rows_and_remove_column'
    Type error in argument 'filter_values':
	    Expected Series of type 'int64' but found type 'int32'

Applying the function ``filter_rows_and_remove_column`` to a data frame with a wrong column type and a missing column
will result in a ``TypeError`` exception with a detailed type error message:

.. code-block:: python

    test_data_with_wrong_type_and_missing_column = pd.DataFrame({
        'A': pd.Series(1, index=list(range(4)), dtype='float64'),
        'B': np.array([1, 2, 3, 4], dtype='int32')
    })
    test_filter_values = pd.Series([3, 4], dtype='int64')

    filter_rows_and_remove_column(test_data_with_wrong_type_and_missing_column, test_filter_values)


.. code-block:: none

    TypeError: Pandas type error in function 'filter_rows_and_remove_column'
    Type error in argument 'data':
        Expected type 'int64' for column B' but found type 'int32'
        Missing column in DataFrame: 'C'
    Type error in return value:
        Expected type 'int64' for column B' but found type 'int32'
        Missing column in DataFrame: 'C'


---------------
Pandera Support
---------------

When this library has been installed which additional `Pandera <https://github.com/unionai-oss/pandera>`_ support
`DataFrameSchema <https://pandera.readthedocs.io/en/stable/reference/generated/pandera.schemas.DataFrameSchema.html>`_
and `SeriesSchema <https://pandera.readthedocs.io/en/stable/reference/generated/pandera.schemas.SeriesSchema.html>`_
can be used as type specifications for data frame and series arguments and return values.

.. code-block:: python

    import pandas as pd
    import pandera as pa
    import numpy as np
    import pandas_type_checks as pd_types

    @pd_types.pandas_type_check(
        pd_types.DataFrameArgument('data',
                                   pa.DataFrameSchema({
                                     'A': pa.Column(np.dtype('float64'), checks=pa.Check.le(10.0)),
                                     'B': pa.Column(np.dtype('int64'), checks=pa.Check.lt(2)),
                                     'C': pa.Column(np.dtype('bool'))
                                   })),
        pd_types.SeriesArgument('filter_values', 'int64'),
        pd_types.DataFrameReturnValue({
            'B': np.dtype('int64'),
            'C': np.dtype('bool')
        })
    )
    def filter_rows_and_remove_column(data: pd.DataFrame, filter_values: pd.Series) -> pd.DataFrame:
        return data[data['B'].isin(filter_values.values)].drop('A', axis=1)
