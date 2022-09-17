:hide-toc:

******************
pandas-type-checks
******************

A Python library providing means for structural type checking of `Pandas <https://pandas.pydata.org/>`_ data frames
and series:

* A decorator ``pandas_type_check`` for specifying and checking the structure of
  Pandas ``DataFrame`` and ``Series`` arguments and return values of a function.
* Support for "non-strict" type checking. In this mode data frames can contain columns which are not part of the type
  specification against which they are checked. Non-strict type checking in that sense allows a form of structural
  subtyping for data frames.
* Configuration options to raise exceptions for type errors or alternatively log them.
* Configuration option to globally enable/disable the type checks. This allows users to enable the type checking
  functionality in e.g. only testing environments.

This library focuses on providing utilities to check the structure (i.e. columns and their types) of Pandas data frames
and series arguments and return values of functions. For checking individual data frame and series values, including
formulating more sophisticated constraints on column values, `Pandera <https://github.com/unionai-oss/pandera>`_ is a
great alternative.

.. toctree::
   :caption: Usage
   :hidden:

   installation
   example
   configuration
   api

.. toctree::
   :caption: Project Links
   :hidden:

   Source Code <https://github.com/mzuber/pandas-type-checks>
   Issue Tracker <https://github.com/mzuber/pandas-type-checks/issues>
