def var_print_str(
    var_name: str,
    var_value
) -> str:
    """
    Formats a variable's name and value as a string, including its type.

    Parameters:
        var_name (str): The name of the variable.
        var_value (Any): The value of the variable.

    Returns:
        str:
            A string representation of
            the variable's name, value, and type.
    """

    return f"{var_name}:{var_value} ({type(var_value)})\n"


def dict_printer(
    d: dict,
    values_type: str,
    head_value: int = 5
) -> None:
    """
    Prints the contents of a dictionary based on the type of its values.

    Parameters:
        d (dict):
            The dictionary to print.
        values_type (str):
            The expected type of the dictionary's values
            ("pd.DataFrame", "cust class", or others).
        head_value (int):
            For DataFrame values, the number of rows to display.
            Must be greater than 0.
    """

    if d is None:
        print("The dictionnary does not exist.")
        return None

    if values_type == "pd.DataFrame":
        if head_value < 1:
            print("head_value must be greater than 0.")
            return None
        for key, value in d.items():
            if value is not None:
                print(f"{key}:\n{value}\n")

    elif values_type == "cust class":
        for _, value in d.items():
            if value is not None:
                value.show()

    else:
        for key, value in d.items():
            print(f"{key}: {value}")
