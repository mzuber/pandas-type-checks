=============
Configuration
=============

The global configuration object ``pandas_type_checks.config`` can be used to configure the behavior of the library:

* ``config.enable_type_checks`` (``bool``): Flag for enabling/disabling type checks for specified arguments and return
  values. This flag can be used to globally enable or disable the type checker in certain environments.
  Default: ``True``
* ``config.strict_type_checks`` (``bool``): Flag for strict type check mode. If strict type checking is enabled data
  frames cannot contain columns which are not part of the type specification against which they are checked. Non-strict
  type checking in that sense allows a form of structural subtyping for data frames.
  Default: ``False``
* ``config.log_type_errors`` (``bool``): Flag indicating that type errors for Pandas dataframes or series values should
  be logged instead of raising a ``TypeError`` exception. Type errors will be logged with log level ``ERROR``.
  Default: ``False``
* ``config.logger`` (``logging.Logger``): Logger to be used for logging type errors when the ``log_type_errors`` flag
  is enabled. When no logger is specified via the configuration a built-in default logger is used.
