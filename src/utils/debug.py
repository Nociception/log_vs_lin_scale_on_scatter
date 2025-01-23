import inspect
from typing import Callable
from functools import wraps


def debug(
    function_name: str,
    debug: int,
    step="START"
) -> None:
    """
    Prints debug information for a function,
    including its name and the current step (if written).

    Usage:
        Copy the line below the if 0 into any function
        for debugging.
        No need to write on your own the function name.
        You also can specify a STEP about the function/method
        instructions.

    Parameters:
        function_name (str):
            The name of the function to debug.
        debug (int):
            The debug level. If non-zero, the debug information is printed.
        step (str):
            The current step in the function's execution
            (e.g., "START" or "END").
    """

    if 0:  # Do not switch to 1.
        debug(inspect.currentframe().f_code.co_name, 1)  # copy this line

    if debug and 1:
        print(f"DEBUG: {step} current function -> {function_name}")


def debug_decorator(func: Callable) -> Callable:
    """
    A decorator to print debug information
    before and after a function's execution.

    Parameters:
        func (Callable): The function to wrap with debug logging.

    Usage:
        Copy that:
            @debug_decorator
        above a function/method definition.

    Returns:
        Callable: The wrapped function with debug logging enabled.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        function_name = func.__name__
        debug_level = 1
        if debug_level:
            print(f"DEBUG: START current function -> {function_name}")
        result = func(*args, **kwargs)
        if debug_level:
            print(f"DEBUG: END current function -> {function_name}")
        return result
    return wrapper


def timediv_test_value():
    """
    As we were told not to use any global variable,
    here is this "function" useful for debug.
    """

    return 1800


def target_test_value():
    """
    As we were told not to use any global variable,
    here is this "function" useful for debug.
    """

    return "Norway"
