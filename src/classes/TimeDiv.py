from .LinReg import LinReg
import numpy as np
import pandas as pd
from scipy.stats import linregress


class TimeDiv:
    """
    Represents a specific time division for
    data processing, merging, and analysis.

    Attributes:
        common_column (str):
            The column common across all DataFrames,
            used for merging (e.g., 'country').
        df_dict (dict[str, pd.DataFrame]):
            Dictionary containing the individual DataFrames
            for data_x, data_y, etc.
        div (int):
            The specific division of time
            (e.g., a year) this instance represents.
        lin_reg_lin (LinReg | None):
            Linear regression results for the linear scale.
        lin_reg_log (LinReg | None):
            Linear regression results for the logarithmic scale.
        merged_data (pd.DataFrame | None):
            The merged DataFrame combining all relevant data.
    """

    def __init__(
        self,
        timediv_list: list[pd.DataFrame],
        common_column: str,
        div: int
    ):
        """
        Initializes a TimeDiv object.

        Parameters:
            timediv_list (list[pd.DataFrame]):
                A list of DataFrames for data_x, data_y, data_point_size,
                extra_data_x, and extra_data_y.
            common_column (str):
                The column common to all DataFrames,
                used for merging (e.g., 'country').
            div (int):
                The specific division of time (e.g., a year)
                this instance represents.
        """

        self.df_dict: dict[str, pd.DataFrame] = {
            "data_x": timediv_list[0],
            "data_y": timediv_list[1],
            "data_point_size": timediv_list[2],
            "extra_data_x": timediv_list[3],
            "extra_data_y": timediv_list[4]
        }
        self.common_column: str = common_column
        self.div: int = div

        self.merged_data: pd.DataFrame | None = None
        self.lin_reg_log: LinReg | None = None
        self.lin_reg_lin: LinReg | None = None

    def show(
        self,
        head_value: int = 5
    ) -> None:
        """The class show method for a TimeDiv class object"""

        print("\n=== SHOW TimeDiv class object (START) ===")

        print("\n--- General Information ---")
        print(f"Time Division: {self.div}")
        print(f"Common Column: {self.common_column}")

        print("\n--- DataFrames Dictionary (df_dict) ---")
        for key, df in self.df_dict.items():
            print(f"{key}:")
            if df is not None:
                print(df.head(head_value))
            else:
                print("None")

        print("\n--- Merged Data ---")
        if self.merged_data is not None:
            print(self.merged_data.head(head_value))
        else:
            print("No merged data available.")

        print("\n--- Linear Regression Results ---")
        if self.lin_reg_log:
            print("\nLogarithmic Scale Regression:")
            self.lin_reg_log.show()
        else:
            print("No logarithmic regression available.")

        if self.lin_reg_lin:
            print("\nLinear Scale Regression:")
            self.lin_reg_lin.show()
        else:
            print("No linear regression available.")

        print("\n=== SHOW TimeDiv class object (END) ===")

    def merge(self) -> None:
        """
        Crucial step for this program, then long detailed docstring:

        Merges the DataFrames in `df_dict` into
        a single unified DataFrame (`merged_data`),
        retaining only rows with complete data across
        all required DataFrames.

        Steps:
        1. **Validation**:
            Ensures that essential DataFrames
            (`data_x`, `data_y`, and `data_point_size`)
            exist in `df_dict`.
            Raises a `ValueError` if any of them is missing.

        2. **Index Alignment**:
            Temporarily sets the `common_column` as the index
            for key DataFrames to align data rows consistently.

        3. **Filtering**:
            Creates a mask to identify rows where all
            essential DataFrames contain valid (non-null) data,
            and applies this mask to filter out incomplete rows.

        4. **Data Merging**:
            Iteratively merges `data_x` with
            other DataFrames (`data_y`, `data_point_size`,
            `extra_data_x`, `extra_data_y`) based on the `common_column`,
            using an inner join to retain only
            rows present in all included DataFrames.

        5. **Final Output**:
            Resets the index of the merged DataFrame for
            a clean result, ready for analysis.

        The resulting `merged_data` contains only rows with consistent,
        valid entries across the relevant DataFrames,
        ensuring high-quality data for further processing.

        Raises:
            ValueError:
                If any of the required DataFrames
                (`data_x`, `data_y`, `data_point_size`) is missing.
        """

        for key in ['data_x', 'data_y', 'data_point_size']:
            if self.df_dict[key] is None:
                raise ValueError(f"Essential DataFrame '{key}' is missing.")

        for key in ['data_x', 'data_y', 'data_point_size']:
            self.df_dict[key] = self.df_dict[key].set_index(self.common_column)

        mask = (
            ~self.df_dict['data_x'].iloc[:, 0].isna() &
            ~self.df_dict['data_y'].iloc[:, 0].isna() &
            ~self.df_dict['data_point_size'].iloc[:, 0].isna()
        )

        for key in ['data_x', 'data_y', 'data_point_size']:
            self.df_dict[key] = self.df_dict[key].loc[
                mask.reindex(self.df_dict[key].index, fill_value=False)
                ].reset_index()

        self.merged_data = self.df_dict['data_x']
        for key in [
            'data_y',
            'data_point_size',
            'extra_data_x',
            'extra_data_y'
        ]:
            if self.df_dict[key] is not None:
                self.merged_data = pd.merge(
                    self.merged_data,
                    self.df_dict[key],
                    on=self.common_column,
                    how='inner'
                )

        self.merged_data.reset_index(drop=True, inplace=True)

    def harmonize_for_regression(self) -> tuple[np.ndarray]:
        """
        Extracts and returns the x and y values
        from `merged_data` as numpy arrays.

        Returns:
            tuple[np.ndarray]:
                A tuple with x-axis (independent)
                and y-axis (dependent) values.

        Raises:
            ValueError:
                If `merged_data` is None,
                meaning `merge` has not been called.
        """

        if self.merged_data is None:
            raise ValueError(
                "Merged data is not available. Did you call `merge()`?"
            )

        return (
            self.merged_data.iloc[:, 1].to_numpy(),
            self.merged_data.iloc[:, 2].to_numpy()
        )

    def calculate_linregr(
            self,
            log: bool
    ) -> LinReg:
        """
        Performs linear regression on x and y data,
        with an optional logarithmic transformation on x.

        Args:
            log (bool):
                If True, applies a base-10 logarithmic
                transformation to x-axis values.

        Returns:
            LinReg:
                The regression result,
                including predicted values, correlation, and p-value.
        """

        data_x, data_y = self.harmonize_for_regression()

        if log:
            data_x = np.log10(data_x)

        slope, intercept, corr, pvalue, _ = linregress(data_x, data_y)
        data_x_sorted = np.sort(data_x)
        predicted = slope * data_x_sorted + intercept

        return LinReg(predicted, corr, pvalue)

    def linear_regressions(self) -> None:
        """
        Computes and stores both logarithmic and
        linear regressions for the data.

        Saves the results in `lin_reg_log` and `lin_reg_lin`.
        """

        self.lin_reg_log = self.calculate_linregr(log=True)
        self.lin_reg_lin = self.calculate_linregr(log=False)
