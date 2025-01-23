def get_data_name(file_name: str) -> str:
    """
    Extracts the base name from a file path,
    removing the extension and replacing underscores with spaces.

    Parameters:
        file_name (str): The full file path or name.

    Returns:
        str: The extracted base name with spaces instead of underscores.
    """

    extension = file_name[file_name.index('.'):]
    return file_name[:file_name.index(extension)].replace('_', ' ')
