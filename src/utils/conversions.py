import numpy as np
from typing import Any

def cust_suffixed_string_to_float(value) -> float:
    """
    Converts a string with custom suffixes (k, M, B) to a float.

    Parameters:
        value (str or numeric):
        The input value to convert.
        Strings can have suffixes 'k', 'M', or 'B'.

    Returns:
        float: The numeric value after conversion,
        or NaN if conversion fails.
    """

    factors = {'k': 1e3, 'M': 1e6, 'B': 1e9}
    try:
        if isinstance(value, str) and value[-1] in factors:
            return float(value[:-1]) * factors[value[-1]]
        return float(value)
    except (ValueError, TypeError):
        return np.nan


def put_kmb_suffix(val: float) -> str:
    """
    Converts a numeric value to a string with
    'k', 'M', or 'B' suffix for thousands, millions, or billions.

    Parameters:
        val (float): The numeric value to convert.

    Returns:
        str: The formatted string with an appropriate suffix,
        or the original number as a string if below 1,000.
    """

    for threshold, suffix in [
        (1e9, 'B'), (1e6, 'M'), (1e3, 'k')
    ]:
        if val > threshold:
            return f"{val / threshold:.2f}{suffix}"
    return str(val)


def tick_label_formatter(
    x: int | float,
    _: Any
) -> str:
    """DOCSTRING"""

    if x == 0:
        return "0"

    if abs(x) < 1000:
        return str(int(x)) if x.is_integer() else f"{x:.2f}"

    exponent = int(f"{x:.0e}".split("e")[1])  
    coefficient = x / (10 ** exponent)
    
    return (
        f"{coefficient:.0f}e{exponent}" if coefficient == 1
        else f"{coefficient:.1f}e{exponent}"
    )
