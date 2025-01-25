"""
This package contains utility functions for debugging, data conversions,
and helper methods used across the project.

# noqa: F401
This comment is used here to silence flake8 concerning this rule:
`imported but unused`

Modules:
- debug: Functions and decorators for debugging.
- helpers: General-purpose utility functions.
- conversions: Functions for data conversions.
- get_data_name: A helper for extracting dataset names.

Usage:
from utils import debug, put_kmb_suffix
"""


from .debug import (  # noqa: F401
    debug,
    debug_decorator,
    timediv_test_value,
    target_test_value
)
from .helpers import dict_printer, var_print_str  # noqa: F401
from .conversions import (  # noqa: F401
    cust_suffixed_string_to_float,
    put_kmb_suffix,
    tick_label_formatter
)
from .get_data_name import get_data_name  # noqa: F401
from .load_csv import load  # noqa: F401

__all__ = [
    name
    for name in locals()
    if not name.startswith("_")
]
