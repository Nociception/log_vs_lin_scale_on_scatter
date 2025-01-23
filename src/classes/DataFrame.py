import pandas as pd
from utils import (
    cust_suffixed_string_to_float,
    get_data_name,
    load,
    var_print_str,
)


class DataFrame:
    """
    Represents a data structure to handle and process
    CSV or other tabular data.

    Attributes:
        data_cleaned (bool):
            Indicates if the data has been cleaned.
        data_frame (pd.DataFrame):
            The loaded pandas DataFrame containing the data.
        data_name (str):
            The name of the data derived from the file path.
        data_type (str):
            The type of data (e.g., 'numerical', 'categorical').
        file_path (str):
            The path to the file containing the data.
        first_column_name (int | float | None):
            The name of the first data column (used for time ranges).
        last_column_name (int | float | None):
            The name of the last data column (used for time ranges).
        short_name (str):
            A shorter, descriptive name for the data.
    """

    def __init__(
        self,
        data_type: str,
        file_path: str,
        short_name: str,
    ):
        """
        Initializes a DataFrame object
        and loads data from the provided file.

        Parameters:
            data_type (str):
                The type of data (e.g., 'numerical', 'categorical').
            file_path (str):
                The path to the file containing the data.
            short_name (str):
                A shorter, descriptive name for the data.

        Raises:
            ValueError: If any parameter is not a string.
        """

        if all(
            isinstance(arg, str) for arg in (
                data_type,
                file_path,
                short_name)
        ):
            self.data_type: str = data_type
            self.file_path: str = file_path
            self.data_name: str = get_data_name(file_path)
            self.short_name: str = short_name
            self.data_frame: pd.DataFrame = load(file_path)
        else:
            raise ValueError(
                f"Both data_type and data_type must be str, not:\n"
                f"{var_print_str('data_type', data_type)}\n"
                f"{var_print_str('file_path', file_path)}"
            )

        self.first_column_name: int | float | None = None
        self.last_column_name: int | float | None = None
        self.data_cleaned: bool = False

    def show(self) -> None:
        """The class show method for a DataFrame class object"""

        print("\n=== SHOW DataFrame class object (START) ===")

        print("\n--- General Information ---")
        print(f"Data Type: {self.data_type}")
        print(f"File Path: {self.file_path}")
        print(f"Data Name: {self.data_name}")
        print(f"Short Name: {self.short_name}")

        print("\n--- Column Information ---")
        print(f"First Column Name: {self.first_column_name}")
        print(f"Last Column Name: {self.last_column_name}")

        print("\n--- Data Cleaning Status ---")
        print(f"Data Cleaned: {self.data_cleaned}")

        print("\n--- DataFrame Content ---")
        print(self.data_frame)

        print("\n=== SHOW DataFrame class object (END) ===")

    class DataFrameException(Exception):
        """
        A base exception class for errors related to the DataFrame class.
        """
        pass

    class DataFrameNotCleanedException(DataFrameException):
        """
        Exception raised when an operation requiring
        a cleaned DataFrame is attempted.

        Attributes:
            msg (str): A descriptive message about the error.
        """

        def __init__(
            self,
            msg="DataFrame object still not cleaned.\n"
                "This exception appears because something has been"
                " attempted which needs the DataFrame to be cleaned"
                " before."
        ):
            """DOCSTRING"""

            super().__init__(msg)

    def get_first_last_column_names(self) -> None:
        """
        Extracts and sets the first and last
        column names as integer or float values.
        """

        self.first_column_name = int(self.data_frame.columns[1])
        self.last_column_name = int(self.data_frame.columns[-1])

    def subset_timediv_extraction(
        self,
        timediv: int,
        common_column: str
    ) -> pd.DataFrame | None:
        """
        Extracts a subset of the DataFrame for a specific time division.

        Parameters:
            timediv (int):
                The time division (year or other) to extract.
            common_column (str):
                The name of the common column (e.g., 'country').

        Returns:
            pd.DataFrame | None:
                A subset DataFrame with the time division and common column,
                or None if the time division is not within the valid range.
        """

        if timediv in range(self.first_column_name, self.last_column_name + 1):
            df_timediv = self.data_frame[
                    [common_column, str(timediv)]
                ].rename(columns={str(timediv): self.data_name})
            df_timediv[self.data_name] = df_timediv[self.data_name].apply(
                cust_suffixed_string_to_float
            )

            return df_timediv

        return None
