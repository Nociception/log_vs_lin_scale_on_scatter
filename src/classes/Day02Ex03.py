"""
Long file here. Here are some tips:
- It is highly recommanded to use a code editor which allows
to fold/unfold functions/methods/classes/if/triple quoted docstrings.
VSCode allows this feature with the little arrow between the line
number and the beginning of the foldable line.
Try with this triple quoted string!
Global code blocks folding (available on VSCode):
ctrl+K (keep ctrl pressed after K)
then ctrl+[indent level ; I suggest 2 for this file]

Ctrl+K ctrl+] to unfold.

After a ctr+clic on a function/method to see its definition,
navigate back with the keyboard short cut: ctrl alt -
"""

from typing import Callable

import matplotlib.collections as mplcollec
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import pandas as pd
import typeguard
from fuzzywuzzy import process
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.collections import LineCollection, PathCollection
from matplotlib.colorbar import Colorbar
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from matplotlib.widgets import Button, Slider, TextBox

from utils import (dict_printer, put_kmb_suffix, tick_label_formatter,
                   var_print_str)

from .DataFrame import DataFrame
from .TimeDiv import TimeDiv


class Day02Ex03:
    """
    Main class to manage data visualization for Day02 Exercise 03.

    Attributes:
        anim (FuncAnimation | None):
            Animation instance for the visual updates.
        ax_box_tracker (Axes | None):
            Axes object for the text box tracker.
        axes (dict[str, Axes] | None):
            Dictionary of Axes for different plots.
        cbar (Colorbar | None):
            Colorbar instance for the scatter plot.
        cmap_colors (list[str]):
            Colors used for the colormap.
        common_column (str | None):
            Common column name shared across datasets.
        corr_log (list | np.ndarray):
            Correlation coefficients for logarithmic scale.
        corr_lin (list | np.ndarray):
            Correlation coefficients for linear scale.
        correlation_cursor_container
        (dict[str, mplcursors.cursor.Cursor | None]):
            Cursors for interactive correlation plots.
        current_frame (int | None):
            Current frame value during animation.
        cursor_container (dict[str, mplcursors.cursor.Cursor | None]):
            Cursors for the main scatter plots.
        data_frames (dict[str, pd.DataFrame | None]):
            Dictionary storing loaded data.
        data_point_size_divider (int):
            Divider used to scale point sizes in scatter plots.
        fig (Figure | None):
            Matplotlib figure instance.
        first_running (bool):
            Indicates whether the animation is running for the first time.
        init_value (int | None):
            Initial value for the slider.
        pause_ax (Axes | None):
            Axes object for the pause button.
        pause_button (Button | None):
            Button widget for pausing the animation.
        play_ax (Axes | None):
            Axes object for the play button.
        play_button (Button | None):
            Button widget for starting the animation.
        precomputed_data (dict[int | float, TimeDiv]):
            Precomputed data for each time division.
        pvalue_log (list | np.ndarray):
            P-values for logarithmic regression.
        pvalue_lin (list | np.ndarray):
            P-values for linear regression.
        running_mode (bool):
            Indicates if the animation is running.
        slider (Slider | None):
            Slider widget for selecting time divisions.
        slider_title_text (str | None):
            Title text for the slider.
        timediv_range (range | None):
            Range of time divisions available in the data.
        text_box_tracker (TextBox | None):
            Text box for tracking user input.
        timediv_type (str | None):
            Type of time division (e.g., "year").
        title (str | None):
            Title of the visualization.
        tracked_element (str):
            Name of the tracked element in the visualization.
        x_label (str | None):
            Label for the x-axis.
        x_unit (str | None):
            Unit for the x-axis.
        y_label (str | None):
            Label for the y-axis.
        y_unit (str | None):
            Unit for the y-axis.
        colored_extra_data (str):
            Name of the extra data column used for coloring points.
    """

    def __init__(self):
        """Initializes the Day02Ex03 object with default values."""

        self.anim: FuncAnimation | None = None
        self.ax_box_tracker: Axes | None = None
        self.axes: dict[str, Axes] | None = None
        self.cbar: Colorbar | None = None
        self.cmap_colors: list[str] = [
            "green",
            "limegreen",
            "yellow",
            "orange",
            "red",
            "magenta",
            "mediumpurple",
            "darkviolet"
        ]
        self.common_column: str | None = None
        self.corr_log: list | np.ndarray = []
        self.corr_lin: list | np.ndarray = []
        self.correlation_cursor_container: dict[
            str, mplcursors.cursor.Cursor | None
        ] = {
            "corr_log": None,
            "pvalue_log": None,
            "corr_lin": None,
            "pvalue_lin": None,
        }
        self.current_frame: int | None = None
        self.cursor_container: dict[
            str, mplcursors.cursor.Cursor | None
            ] = {
            "log": None,
            "lin": None
        }
        self.data_frames: dict[str, pd.DataFrame | None] = {
            "data_x": None,
            "data_y": None,
            "data_point_size": None,
            "extra_data_x": None,
            "extra_data_y": None,
        }
        self.data_point_size_divider: int = None
        self.fig: Figure | None = None
        self.first_running: bool = False
        self.init_value: int | None = None
        self.interval_between_two_frames: int = 100
        self.pause_ax: Axes | None = None
        self.pause_button: Button | None = None
        self.play_ax: Axes | None = None
        self.play_button: Button | None = None
        self.precomputed_data: dict[int | float, TimeDiv] = {}
        self.pvalue_log: list | np.ndarray = []
        self.pvalue_lin: list | np.ndarray = []
        self.running_mode: bool = False
        self.slider: Slider | None = None
        self.slider_title_text: str | None = None
        self.timediv_range: range | None = None
        self.text_box_tracker: TextBox | None = None
        self.timediv_type: str | None = None
        self.title: str | None = None
        self.tracked_element: str = "None"
        self.x_label: str | None = None
        self.x_unit: str | None = None
        self.y_label: str | None = None
        self.y_unit: str | None = None

        # permanently set that way (adjustable in future versions)
        self.colored_extra_data: str = "extra_data_x"

    def show(self):
        """The class show method for a Day02Ex03 class object"""

        print("\n=== SHOW Day02Ex03 object (START) ===")

        print("\n--- General Settings ---")
        print(f"Title: {self.title}")
        print(f"Timediv Range: {self.timediv_range}")
        print(f"Timediv Type: {self.timediv_type}")
        print(f"Initial Value: {self.init_value}")
        print(f"Running Mode: {self.running_mode}")
        print(f"First Running: {self.first_running}")

        print("\n--- Labels and Units ---")
        print(f"X Label: {self.x_label}")
        print(f"X Unit: {self.x_unit}")
        print(f"Y Label: {self.y_label}")
        print(f"Y Unit: {self.y_unit}")

        print("\n--- Correlation and P-Values ---")
        print(f"Correlation (Log): {self.corr_log}")
        print(f"P-Values (Log): {self.pvalue_log}")
        print(f"Correlation (Lin): {self.corr_lin}")
        print(f"P-Values (Lin): {self.pvalue_lin}")

        print("\n--- Tracking ---")
        print(f"Tracked Element: {self.tracked_element}")

        print("\n--- Data Frames ---")
        dict_printer(self.data_frames, values_type="cust class")

        print("\n--- Color Map and Color Bar ---")
        print(f"Color Map Colors: {self.cmap_colors}")
        print(f"Colored Extra Data: {self.colored_extra_data}")
        print(f"Color Bar: {self.cbar}")

        print("\n--- Interactive Elements ---")
        print(f"Slider: {self.slider}")
        print(f"Slider Title Text: {self.slider_title_text}")
        print(f"Play Button: {self.play_button}")
        print(f"Pause Button: {self.pause_button}")
        print(f"Tracker Text Box: {self.text_box_tracker}")

        print("\n--- Axes and Figures ---")
        print(f"Figure: {self.fig}")
        print(f"Axes: {self.axes}")

        print("\n=== SHOW Day02Ex03 object (END) ===\n")

    def add_data_path(
        self,
        data_path: str,
        data_type: str,
        short_name: str
    ) -> None:
        """
        Adds a data path to the data_frames dictionary.

        Args:
            data_path (str):
                Path to the dataset file.
            data_type (str):
                Type of the data (e.g., "data_x", "data_y").
            short_name (str):
                Shortened name for the dataset.

        Raises:
            ValueError:
                If any argument is not a valid string or
                `data_path` is too short.
        """

        if (
            all(
                isinstance(arg, str) for arg in (
                data_path,
                data_type,
                short_name
                )
            )
            and len(data_path) >= 3
        ):
            self.data_frames[data_type] = DataFrame(
                data_type,
                data_path,
                short_name
            )
        else:
            raise ValueError(
                f"data_path (min length 3),"
                f"data_type and short_name must be str, not:\n"
                f"{var_print_str('data_path', data_path)}\n"
                f"{var_print_str('data_type', data_type)}\n"
                f"{var_print_str('data_type', short_name)}"
            )

    @typeguard.typechecked
    def add_data_x_path(
        self,
        data_x_path: str,
        short_name: str,
        x_label: str,
        x_unit: str
    ) -> None:
        """
        Adds the X-axis dataset and related metadata.

        Args:
            data_x_path (str):
                File path for the X-axis dataset.
            short_name (str):
                Abbreviated name for the dataset, used in legends or labels.
            x_label (str):
                Label for the X-axis.
            x_unit (str):
                Unit associated with the X-axis values.
        """

        self.add_data_path(
            data_x_path,
            "data_x",
            short_name
        )
        self.x_label = x_label
        self.x_unit = x_unit

    @typeguard.typechecked
    def add_data_y_path(
        self,
        data_y_path: str,
        short_name: str,
        y_label: str,
        y_unit: str
    ) -> None:
        """
        Adds the Y-axis dataset and related metadata.

        Args:
            data_y_path (str):
                File path for the Y-axis dataset.
            short_name (str):
                Abbreviated name for the dataset, used in legends or labels.
            y_label (str):
                Label for the Y-axis.
            y_unit (str):
                Unit associated with the Y-axis values.
        """

        self.add_data_path(
            data_y_path,
            "data_y",
            short_name
        )
        self.y_label = y_label
        self.y_unit = y_unit

    @typeguard.typechecked
    def add_data_point_size_path(
        self,
        data_point_size_path: str,
        short_name: str,
        divider: int | float
    ) -> None:
        """
        Adds the dataset for determining the size of scatter plot points.

        Args:
            data_point_size_path (str):
                File path for the dataset controlling point sizes.
            short_name (str):
                Abbreviated name for the dataset, used in legends or labels.
            divider (int | float):
                Scaling factor to adjust the point sizes.
        """

        self.data_point_size_divider = divider
        self.add_data_path(
            data_point_size_path,
            "data_point_size",
            short_name
        )

    @typeguard.typechecked
    def add_extra_data_x_path(
        self,
        extra_data_x_path: str,
        short_name: str
    ) -> None:
        """
        Adds an additional dataset related to
        the X-axis for coloring or metadata.

        Args:
            extra_data_x_path (str):
                File path for the additional X-axis dataset.
            short_name (str):
                Abbreviated name for the dataset, used in legends or labels.
        """

        self.add_data_path(
            extra_data_x_path,
            "extra_data_x",
            short_name
        )

    @typeguard.typechecked
    def add_extra_data_y_path(
        self,
        extra_data_y_path: str,
        short_name: str
    ) -> None:
        """
        Adds an additional dataset related to
        the Y-axis for coloring or metadata.

        Args:
            extra_data_y_path (str):
                File path for the additional Y-axis dataset.
            short_name (str):
                Abbreviated name for the dataset, used in legends or labels.
        """

        self.add_data_path(
            extra_data_y_path,
            "extra_data_y",
            short_name
        )

    @typeguard.typechecked
    def add_title(
        self,
        title: str
    ) -> None:
        """
        Sets the title for the visualization.

        Args:
            title (str): The title of the visualization.
        """

        self.title = title

    @typeguard.typechecked
    def add_timediv_range(
        self,
        start: int,
        stop: int,
        init_value: int,
        type: str
    ) -> None:
        """
        Defines the range of time divisions for the visualization.

        Args:
            start (int):
                Starting value for the time division.
            stop (int):
                Ending value for the time division.
            init_value (int):
                Initial time division to be displayed.
            type (str):
                Label for the type of time division (e.g., "year").
        """

        self.timediv_range = range(start, stop + 1)
        self.timediv_type = type
        self.init_value = init_value
        self.current_frame = init_value

    @typeguard.typechecked
    def add_common_column(
        self,
        common_column: str
    ) -> None:
        """
        Sets the common column name shared across datasets.

        Args:
            common_column (str):
                Column name that links datasets together.
        """

        self.common_column = common_column

    @typeguard.typechecked
    def set_autoplay_at_start(
        self,
        autoplay_at_start: bool
    ) -> None:
        """
        Configures whether the animation starts automatically.

        Args:
            autoplay_at_start (bool):
                True to start the animation automatically; False otherwise.
        """

        self.first_running = autoplay_at_start

    def clean_data_x(self) -> None:
        """
        Cleans the DataFrame associated with `data_x`.

        - Sorts the DataFrame by the `common_column`.
        - Resets the index to ensure a clean sequential order.
        - Marks the DataFrame as cleaned.

        Raises:
            ValueError: If `data_x` is not properly initialized.
        """

        df = self.data_frames['data_x']
        if df is not None:
            df.data_frame.sort_values(
                by=self.common_column
                ).reset_index(drop=True)
            df.data_cleaned = True

    def clean_data_y(self) -> None:
        """
        Cleans the DataFrame associated with `data_y`.

        - Sorts the DataFrame by the `common_column`.
        - Resets the index to ensure a clean sequential order.
        - Marks the DataFrame as cleaned.

        Raises:
            ValueError: If `data_y` is not properly initialized.
        """

        df = self.data_frames['data_y']
        if df is not None:
            df.data_frame.sort_values(
                by=self.common_column
                ).reset_index(drop=True)
            df.data_cleaned = True

    def clean_data_point_size(self) -> None:
        """
        Cleans the DataFrame associated with `data_point_size`.

        - Sorts the DataFrame by the `common_column`.
        - Resets the index to ensure a clean sequential order.
        - Marks the DataFrame as cleaned.

        Raises:
            ValueError: If `data_point_size` is not properly initialized.
        """

        df = self.data_frames['data_point_size']
        if df is not None:
            df.data_frame.sort_values(
                by=self.common_column
                ).reset_index(drop=True)
            df.data_cleaned = True

    def clean_extra_data_x(self) -> None:
        """
        Cleans the DataFrame associated with `extra_data_x`.

        - Removes irrelevant columns such as
        'Country Code', 'Indicator Name',
        'Indicator Code', and 'Unnamed: 68'.
        - Renames the 'Country Name' column to match `common_column`.
        - Matches country names in `extra_data_x` with those in `data_x`,
        using fuzzy matching to align similar names.
        - Drops rows with unmatched or duplicate entries in `common_column`.
        - Sorts the DataFrame by `common_column`.
        - Marks the DataFrame as cleaned.

        Raises:
            ValueError: If `extra_data_x` is not properly initialized.

        Notes:
            - A match is considered valid if the similarity score is >= 80.
        """

        if self.data_frames['extra_data_x'] is not None:
            df = self.data_frames['extra_data_x'].data_frame
            df = df.drop(
                columns=[
                    "Country Code",
                    "Indicator Name",
                    "Indicator Code",
                    "Unnamed: 68"
                ],
                errors="ignore"
            )
            df = df.rename(
                columns={"Country Name": self.common_column}
            )

            data_y_countries = self.data_frames[
                'data_x'
                ].data_frame[self.common_column].unique()

            def match_country_name(country: str) -> int | None:
                """
                Returns the first score >= 80 found during the
                fuzzywuzzy process.extractOne.

                This function calculates a match score between
                an entity name (from the extra_data_x df)
                and every entity names in data_y.
                """

                match, score = process.extractOne(country, data_y_countries)
                return match if score >= 80 else None

            df[self.common_column] = df[self.common_column].apply(
                match_country_name
            )

            df = df.dropna(subset=[self.common_column])
            df = df.drop_duplicates(
                subset=[self.common_column],
                keep="first"
            )
            df = df.sort_values(
                by=self.common_column).reset_index(drop=True)

            self.data_frames['extra_data_x'].data_frame = df
            self.data_frames['extra_data_x'].data_cleaned = True

    def clean_extra_data_y(self) -> None:
        """
        Marks the DataFrame associated with `extra_data_y` as cleaned.

        - Simply sets the `data_cleaned` attribute to True, as no
        specific cleaning steps are defined for this DataFrame so far.

        Raises:
            ValueError: If `extra_data_y` is not properly initialized.
        """

        if self.data_frames['extra_data_y'] is not None:
            self.data_frames['extra_data_y'].data_cleaned = True

    def clean_data_frames(self) -> None:
        """
        Cleans all associated DataFrames in the `data_frames` attribute.

        - Sequentially calls individual cleaning methods:
            - `clean_data_x`
            - `clean_data_y`
            - `clean_data_point_size`
            - `clean_extra_data_x`
            - `clean_extra_data_y`

        Raises:
            ValueError:
                If any DataFrame is missing or improperly initialized.
        """

        self.clean_data_x()
        self.clean_data_y()
        self.clean_data_point_size()
        self.clean_extra_data_x()
        self.clean_extra_data_y()

    def get_first_last_column_names(self) -> None:
        """
        Retrieves and stores the first and
        last column names for each DataFrame.

        - Iterates over all DataFrames in `data_frames`.
        - Checks if each DataFrame has been cleaned before proceeding.
        - Calls the `get_first_last_column_names` method for each DataFrame.

        Raises:
            DataFrameNotCleanedException: If any DataFrame is not cleaned
            before this operation.
        """

        for key, data_frame in self.data_frames.items():
            if data_frame is None:
                continue
            if not data_frame.data_cleaned:
                raise data_frame.DataFrameNotCleanedException(
                    f"The DataFrame '{key}' has not been cleaned."
                )
            data_frame.get_first_last_column_names()

    def subsets_timediv_extraction(
        self,
        timediv: int,
    ) -> list[pd.DataFrame]:
        """
        Extracts subsets of data for a given
        time division across all DataFrames.

        Args:
            timediv (int):
                The time division for which data should be extracted.

        Returns:
            list[pd.DataFrame]:
                A list of DataFrames, one for each entry in `data_frames`.
                If a DataFrame is `None`,
                its corresponding subset will also be `None`.
        """

        res = list()
        for df in self.data_frames.values():
            if df is not None:
                res.append(
                    df.subset_timediv_extraction(
                        timediv,
                        self.common_column
                    )
                )
            else:
                res.append(None)

        return res

    def precompute_data(self):
        """
        Precomputes and stores data for all time divisions.

        Extracts subsets for each time division.
        Merges the subsets into a single DataFrame for each division.
        Calculates linear regressions for both logarithmic and linear scales.
        Fills attributes for correlation coefficients and p-values over time.

        Raises:
            ValueError:
                If the data is not properly cleaned or initialized.
        """

        self.get_first_last_column_names()

        for div in self.timediv_range:
            timediv = TimeDiv(
                self.subsets_timediv_extraction(div),
                self.common_column,
                div
            )
            timediv.merge()
            timediv.linear_regressions()

            self.precomputed_data[div] = timediv
            self.corr_log.append(timediv.lin_reg_log.corr)
            self.pvalue_log.append(timediv.lin_reg_log.pvalue)
            self.corr_lin.append(timediv.lin_reg_lin.corr)
            self.pvalue_lin.append(timediv.lin_reg_lin.pvalue)

        self.corr_log = np.array(self.corr_log)
        self.pvalue_log = np.array(self.pvalue_log)
        self.corr_lin = np.array(self.corr_lin)
        self.pvalue_lin = np.array(self.pvalue_lin)

    def get_text_sizes(
        self,
        fig_width: float,
        fig_height: float
    ) -> dict:
        """
        Calculate text sizes dynamically based on figure dimensions.

        Args:
            fig_width (float): The current width of the figure in inches.
            fig_height (float): The current height of the figure in inches.

        Returns:
            dict: A dictionary containing font sizes for various elements.
        """

        base_size = min(fig_width, fig_height) * 1.5
        return {
            "title": base_size * 1.2,
            "label": base_size * 0.8,
            "ticks": base_size * 0.6,
            "annotation": base_size * 0.7,
        }

    def on_resize(self, event):
        """
        Handle the resize event to adjust layout and text sizes dynamically.

        - Adjusts spacing between subplots based on figure size.
        - Updates text sizes for titles, labels, and ticks.
        """

        fig_width, fig_height = self.fig.get_size_inches()

        scale = min(fig_width / 10, fig_height / 6)
        self.fig.subplots_adjust(
            top=0.96,
            bottom=0.1,
            left=0.05,
            right=0.99,
            hspace=0.25 * scale,
            wspace=0.2 * scale
        )

        text_sizes = self.get_text_sizes(fig_width, fig_height)
        for _, ax in self.axes.items():
            ax.set_title(ax.get_title(), fontsize=text_sizes["title"])
            ax.set_xlabel(ax.get_xlabel(), fontsize=text_sizes["label"])
            ax.set_ylabel(ax.get_ylabel(), fontsize=text_sizes["label"])
            ax.tick_params(axis="both", labelsize=text_sizes["ticks"])

        self.fig.canvas.draw_idle()

    def build_fig_axes(self) -> None:
        """
        Sets up the main figure and axes for visualization.

        - Creates a mosaic layout with two scatter plots (log and linear)
        and two correlation graphs.
        - Adjusts spacing dynamically based on the figure size.
        - Connects a resize event to maintain responsiveness.

        Notes:
            Adjustments are tailored for a default figure size of (10, 6).
        """

        fig_w, fig_h = 10, 6

        self.fig, self.axes = plt.subplot_mosaic(
            [
                ["log", "log", "log", "corr_log"],
                ["log", "log", "log", "corr_log"],
                ["log", "log", "log", "corr_diff"],
                ["lin", "lin", "lin", "corr_diff"],
                ["lin", "lin", "lin", "corr_lin"],
                ["lin", "lin", "lin", "corr_lin"],
            ],
            figsize=(fig_w, fig_h)
        )

        ticks_labelticks_space = 1
        for ax in self.axes.values():
            ax.tick_params(axis='x', pad=ticks_labelticks_space)
            ax.tick_params(axis='y', pad=ticks_labelticks_space)

        self.fig.canvas.mpl_connect('resize_event', self.on_resize)

        self.fig.subplots_adjust(
            top=0.96,
            bottom=0.1,
            left=0.05,
            right=0.99,
            hspace=0.25,
            wspace=0.2
        )

    def build_colorbar(
        self,
        ax: Axes,
        extra_data: DataFrame,
    ) -> None:
        """
        Adds a colorbar to the specified axis based on extra data.

        Args:
            ax (Axes):
                The axis to which the colorbar will be added.
            extra_data (DataFrame):
                The data to use for determining color scaling.

        Notes:
            - The colorbar is based on a linear segmented colormap.
            - The default range for values is 0 to 100.
        """

        vmin: float = 0
        vmax: float = 100
        orientation: str = "vertical"
        label_position: str = "right"
        ticks_position: str = "left"
        pad: float = 0.05
        fraction: float = 0.02
        aspect: int = 50
        labelpad: int = 1
        nb_divs: int = 100
        cmap = LinearSegmentedColormap.from_list(
            name=extra_data.data_name,
            colors=self.cmap_colors,
            N=nb_divs
        )
        norm = Normalize(vmin=vmin, vmax=vmax)
        sm = ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        self.cbar = self.fig.colorbar(
            sm,
            ax=ax,
            orientation=orientation,
            pad=pad,
            fraction=fraction,
            aspect=aspect
        )
        self.cbar.set_label(
            label=extra_data.short_name,
            labelpad=labelpad
        )
        self.cbar.ax.yaxis.set_label_position(label_position)
        self.cbar.ax.yaxis.set_ticks_position(ticks_position)

    def get_points_color(
        self,
        data: pd.DataFrame
    ) -> list[str]:
        """
        Determines the colors for scatter plot points based on extra data.

        Args:
            data (pd.DataFrame):
                The data for which colors need to be assigned.

        Returns:
            list[str]: A list of RGBA tuples for each data point.
            Points without extra data are assigned a default blue color.
        """

        extra_data_colored_name = self.data_frames[
            self.colored_extra_data].data_name
        if extra_data_colored_name in data.columns:
            colors = self.cmap_colors
            gray = (0.5, 0.5, 0.5, 1.0)
            cmap = LinearSegmentedColormap.from_list(
                "cmap_name",
                colors,
                N=100
            )
            colored_extra_data_values = data[extra_data_colored_name]
            norm = Normalize(vmin=0, vmax=100)
            colors = [
                cmap(norm(g)) if not np.isnan(g) else gray
                for g in colored_extra_data_values
            ]

        else:
            colors = ['blue'] * len(data)

        return colors

    def plot_scatter(
        self,
        ax: Axes,
        data: pd.DataFrame,
        points_color: list[str],
    ) -> mplcollec.PathCollection:
        """
        Plots a scatter graph with optional
        highlighting of a tracked element.

        Args:
            ax (Axes):
                The axis on which to plot the scatter graph.
            data (pd.DataFrame):
                The data to plot.
            points_color (list[str]):
                The color of each point.

        Returns:
            mplcollec.PathCollection:
                The collection of scatter plot points.

        Highlights:
            - Uses circle sizes proportional to the `data_point_size`.
            - Highlights the tracked element in cyan if specified.
        """

        pt_size_s_name = self.data_frames["data_point_size"].short_name
        scatter = ax.scatter(
            data[self.data_frames["data_x"].data_name].values,
            data[self.data_frames["data_y"].data_name].values,
            s=data[
                self.data_frames["data_point_size"].data_name
                ].values / self.data_point_size_divider,
            c=points_color,
            alpha=0.7,
            label=f"{self.common_column.title()} ({pt_size_s_name}-sized)"
        )

        if self.tracked_element:
            highlighted = data[
                data[self.common_column].str.contains(
                    self.tracked_element,
                    case=False,
                    na=False
                )
            ]
            if not highlighted.empty:
                ax.scatter(
                    highlighted[self.data_frames["data_x"].data_name],
                    highlighted[self.data_frames["data_y"].data_name],
                    s=highlighted[
                        self.data_frames["data_point_size"].data_name
                        ] / self.data_point_size_divider,
                    color='cyan',
                    label=f"Tracked: {self.tracked_element}",
                    edgecolor='black'
                )
        return scatter

    def plot_regressline(
            self,
            timediv: TimeDiv,
            is_log_scale: bool,
            ax: Axes,
            color: str
    ) -> None:
        """
        Plots the regression line on the specified axis.

        Args:
            timediv (TimeDiv):
                The time division containing regression data.
            is_log_scale (bool):
                Whether the regression is log-scaled.
            ax (Axes):
                The axis on which to plot the regression line.
            color (str):
                The color of the regression line.

        Notes:
            - The regression line is dashed and
            annotated with its correlation coefficient.
            - Points with NaN values are filtered out before plotting.
        """

        x = np.sort(
                timediv.merged_data[self.data_frames["data_x"].data_name])
        regression = (
            timediv.lin_reg_log
            if is_log_scale
            else timediv.lin_reg_lin
        )
        y = regression.predicted

        mask = ~np.isnan(x) & ~np.isnan(y)
        x_cleaned = x[mask]
        y_cleaned = y[mask]

        reg_line_type = 'log-linear' if is_log_scale else 'linear'
        ax.plot(
            x_cleaned,
            y_cleaned,
            color=color,
            linestyle='--',
            label=f"Regression Line ({reg_line_type})"
                  f" - Corr: {regression.corr:.2f}"
        )

    def set_graph_meta_data(
        self,
        timediv: TimeDiv,
        is_log_scale: bool,
        ax: Axes,
        color: str
    ) -> None:
        """
        Sets metadata (titles, labels, scales) for a scatter plot.

        Args:
            timediv (TimeDiv):
                The time division for which the graph is being set.
            is_log_scale (bool):
                Whether the graph is log-scaled.
            ax (Axes):
                The axis to set metadata for.
            color (str):
                The highlight color for text annotations.

        Notes:
            - Adds bold watermark text indicating "LOG" or "LINEAR" scaling.
            - Titles and labels are set dynamically based on the scale type.
        """

        if is_log_scale:
            ax.set_xscale('log')
            ax.set_title(f"{self.title} in {timediv.div}")
            ax.set_xlabel(
                f"{self.x_label} ({self.x_unit}, log scale)",
                labelpad=-5
            )
        else:
            ax.set_xlabel(f"{self.x_label} ({self.x_unit})")
        ax.set_ylabel(f"{self.y_label} ({self.y_unit})")

        ax.xaxis.set_major_formatter(FuncFormatter(tick_label_formatter))
        ax.xaxis.set_major_formatter(FuncFormatter(tick_label_formatter))

        ax.legend(loc="best")

        ax.text(
            0.5,
            0.5,
            "LOG" if is_log_scale else "LINEAR",
            transform=ax.transAxes,
            fontsize=100,
            color=color,
            alpha=0.08,
            ha="center", va="center",
            weight="bold",
        )

    def manage_cursor(
        self,
        ax_name: str,
        scatter: PathCollection,
        data: pd.DataFrame
    ) -> None:
        """
        Adds interactivity with a cursor to a scatter plot.

        Args:
            ax_name (str):
                Name of the axis.
            scatter (PathCollection):
                The scatter plot collection.
            data (pd.DataFrame):
                The data corresponding to the scatter plot.

        Notes:
            - Annotations display detailed information for each point.
            - Removes existing cursors on the axis before adding a new one.
        """

        if (
            ax_name in self.cursor_container
            and self.cursor_container[ax_name]
        ):
            try:
                self.cursor_container[ax_name].remove()
                self.cursor_container[ax_name] = None
            except Exception as e:
                print(
                    f"Warning: Failed to remove cursor on "
                    f"{ax_name}: {e}"
                )

        cursor = mplcursors.cursor(
            scatter,
            hover=True
        )

        @cursor.connect("add")
        def on_add(sel):
            """
            Handles the addition of cursor annotations for scatter plots.

            Args:
                sel (mplcursors.Selection):
                    The selection object for the hovered data point.

            Functionality:
                - Retrieves the index and data of the selected point.
                - Formats and displays an annotation with relevant details:
                x-value, y-value, point size, and extra data (if available).
                - Styles the annotation box for clarity.
                - Ensures robust handling of missing or invalid data.

            Raises:
                KeyError:
                    If a required column is missing in the DataFrame.
                Exception:
                    For unexpected errors during the annotation process.
            """

            idx = sel.index

            try:
                row = data.iloc[idx]
                data_x_name = self.data_frames["data_x"].data_name
                data_y_name = self.data_frames["data_y"].data_name
                data_point_size_name = self.data_frames[
                    "data_point_size"].data_name
                extra_data_x_text = 'N/A'
                extra_data_x_name = self.data_frames[
                    "extra_data_x"].data_name

                if (
                    extra_data_x_name in row.index
                    and pd.notna(row[extra_data_x_name])
                ):
                    extra_data_x_text = f"{row[extra_data_x_name]:.2f}"

                sel.annotation.set(
                    text=(
                        f"{row[self.common_column]}\n"
                        f"{self.data_frames['data_x'].short_name}: "
                        f"{put_kmb_suffix(row[data_x_name])} {self.x_unit}\n"
                        f"{self.data_frames['data_y'].short_name}: "
                        f"{row[data_y_name]:.1f} {self.y_unit}\n"
                        f"{self.data_frames['data_point_size'].short_name}: "
                        f"{put_kmb_suffix(row[data_point_size_name])}\n"
                        f"{self.data_frames['extra_data_x'].short_name}: "
                        f"{extra_data_x_text}"
                    ),
                    fontsize=10,
                    fontweight="bold"
                )
                sel.annotation.get_bbox_patch().set(alpha=0.6, color="white")

            except KeyError as e:
                print(f"KeyError during cursor annotation: {e}")
            except Exception as e:
                print(f"Unexpected error during cursor annotation: {e}")

        self.cursor_container[ax_name] = cursor

    def plot(
        self,
        timediv: TimeDiv,
        ax: Axes,
        is_log_scale: bool,
        ax_name: str,
        color: str
    ) -> None:
        """
        Plots a scatter graph, regression line, and adds interactivity.

        Args:
            timediv (TimeDiv): The time division data to plot.
            ax (Axes): The axis to plot on.
            is_log_scale (bool): Whether the graph uses a log scale.
            ax_name (str): The name of the axis.
            color (str): The highlight color for the regression line.

        Notes:
            - Combines scatter plots,
            regression lines, and cursor interactivity.
        """

        data = timediv.merged_data
        points_color = self.get_points_color(data)
        scatter = self.plot_scatter(
            ax,
            data,
            points_color)
        self.plot_regressline(
            timediv,
            is_log_scale,
            ax,
            color,
        )
        self.set_graph_meta_data(
            timediv,
            is_log_scale=is_log_scale,
            ax=ax,
            color=color,
        )

        self.manage_cursor(
            ax_name,
            scatter,
            data
        )

    def update_color_point_from_extra_data(
        self,
        timediv: TimeDiv
    ) -> None:
        """
        Updates the visibility of the colorbar
        based on the presence of extra data.

        Args:
            timediv (TimeDiv):
                The current time division data.

        Notes:
            - Hides or shows the colorbar dynamically
            depending on whether extra data is available.
        """

        extra_data_x_name = self.data_frames["extra_data_x"].data_name
        if extra_data_x_name in timediv.merged_data.columns:
            if not self.cbar.ax.get_visible():
                self.cbar.ax.set_visible(True)
        else:
            if self.cbar.ax.get_visible():
                self.cbar.ax.set_visible(False)

    def update_corr_graphs(self) -> None:
        """
        Updates the correlation graphs with a vertical line
        indicating the current slider value.

        Notes:
            - Removes any existing vertical lines before adding a new one.
            - The vertical line highlights the selected year on the graph.
        """

        for corr_name, corr_ax in self.axes.items():
            if "corr" in corr_name:
                selected_x = self.slider.val

                if hasattr(self, f"{corr_name}_vline"):
                    getattr(self, f"{corr_name}_vline").remove()

                setattr(
                    self,
                    f"{corr_name}_vline",
                    corr_ax.axvline(
                        x=selected_x,
                        color="orange",
                        linestyle="--",
                        linewidth=0.8
                    )
                )

    def update(
        self,
        slider_val=None
    ) -> None:
        """
        Updates the main plots (scatter and correlation graphs)
        based on the slider value.

        Args:
            slider_val (int, optional):
                The current value of the slider. Defaults to None.

        Notes:
            - Replots scatter graphs with updated data.
            - Updates regression lines and correlation graphs.
            - Adjusts colorbar visibility and correlation graph indicators.
        """

        self.axes["log"].cla()
        self.axes["lin"].cla()

        if slider_val is None:
            slider_val = int(self.slider.val)

        timediv = self.precomputed_data[slider_val]

        self.plot(
            timediv=timediv,
            ax=self.axes['log'],
            is_log_scale=True,
            ax_name="log",
            color="red"
        )
        self.plot(
            timediv=timediv,
            ax=self.axes['lin'],
            is_log_scale=False,
            ax_name="lin",
            color="green"
        )

        self.update_color_point_from_extra_data(timediv)

        self.update_corr_graphs()

        plt.draw()

    def update_slider_title(
        self,
        val: int
    ) -> None:
        """
        Updates the title text of the slider to reflect the current year.

        Args:
            val (int):
                The current slider value.

        Notes:
            - Dynamically updates the displayed text with the current year.
        """

        self.slider_title_text.set_text(
            f"{self.timediv_type.title()}: {int(val)}"
        )
        self.fig.canvas.draw_idle()

    def build_slider(
        self,
        update_callback_function: Callable
    ) -> None:
        """
        Builds the slider with many fixed numbers and values.
        Buttons slider linked are also created here.
        """

        ax_slider = self.fig.add_axes([0.05, 0.01, 0.5, 0.03])
        self.slider = Slider(
            ax_slider,
            "",
            self.timediv_range.start,
            self.timediv_range.stop - 1,
            valinit=self.init_value,
            valstep=1,
            color="olive"
        )
        self.slider_title_text = ax_slider.text(
            0.5, 0.3,
            f"{self.timediv_type.title()}: {int(self.slider.val)}",
            transform=ax_slider.transAxes,
            fontsize=10,
            ha='left'
        )
        self.slider.on_changed(self.update_slider_title)
        self.slider.on_changed(update_callback_function)

        self.play_ax = self.fig.add_axes([0.56, 0.01, 0.03, 0.03])
        self.play_button = Button(self.play_ax, '\u25B6')
        self.play_button.on_clicked(self.start_animation)

        self.pause_ax = self.fig.add_axes([0.6, 0.01, 0.03, 0.03])
        self.pause_button = Button(self.pause_ax, r'$\mathbf{| |}$')
        self.pause_button.on_clicked(self.stop_animation)

    def start_animation(
        self,
        event=None
    ) -> None:
        """
        Starts the animation of the slider and associated plots.

        Args:
            event (optional):
                The triggering event, typically from a UI interaction.

        Notes:
            - If the animation is already running
            (`self.running_mode` is True), the method does nothing.
            - The animation iterates over frames
            starting from the current slider value.
        """

        if self.running_mode and not self.first_running:
            return

        self.first_running = False
        self.running_mode = True
        self.anim = FuncAnimation(
            self.fig,
            self.update_slider,
            frames=range(self.slider.val, self.timediv_range.stop),
            repeat=True,
            interval=self.interval_between_two_frames,
        )
        plt.draw()

    def stop_animation(
        self,
        event=None
    ) -> None:
        """
        Stops the animation of the slider.

        Args:
            event (optional):
                The triggering event, typically from a UI interaction.

        Notes:
            - If the animation is not running, the method does nothing.
        """
        if not self.running_mode:
            return
        self.running_mode = False
        if self.anim is not None:
            self.anim.pause()

    def update_slider(self, frame):
        """
        Updates the slider value and the current frame
        during the animation.

        Args:
            frame (int):
                The current frame value.

        Notes:
            - Updates the slider's position
            and stores the current frame value.
        """

        self.slider.set_val(frame)
        self.current_frame = frame

    def set_right_side_graphs_cursors(self) -> None:
        """
        Adds interactivity (cursors) to the curves
        in the correlation and p-value graphs.

        Notes:
            - Cursors provide hover annotations for
            correlation and p-value graphs.
            - Existing cursors are removed before new ones are added.
        """

        curve_labels = {
            "corr_log": ["corr log", "pvalue log"],
            "corr_diff": ["corr_diff"],
            "corr_lin": ["corr lin", "pvalue lin"],
        }

        for ax_name, labels in curve_labels.items():
            if ax_name in self.axes:
                ax = self.axes[ax_name]

                for label in labels:
                    if (
                        label in self.correlation_cursor_container
                        and self.correlation_cursor_container[label]
                    ):
                        try:
                            self.correlation_cursor_container[label].remove()
                            self.correlation_cursor_container[label] = None
                        except Exception as e:
                            print(
                                f"Warning: Failed to remove"
                                f" cursor on {label}: {e}"
                            )

                for line in ax.get_lines():
                    if line.get_label() in labels:
                        cursor = mplcursors.cursor(line, hover=True)

                        @cursor.connect("add")
                        def on_add(sel, label=line.get_label()):
                            """
                            Callback function to handle hover events
                            on correlation and p-value curves.

                            Args:
                                sel:
                                    The mplcursors selection object,
                                    providing details about
                                    the hovered point.
                                label (str):
                                    The label of the curve being annotated,
                                    used to distinguish between correlation
                                    and p-value curves.

                            Functionality:
                                - Retrieves the year (x) and
                                the curve value (y) of the hovered point.
                                - Sets an annotation displaying the year
                                and the value with a prefix
                                ('Corr' or 'Pval') based on the curve type.
                                - Styles the annotation for better
                                visibility and clarity.
                            """
                            x, y = sel.target

                            sel.annotation.set(
                                text=f"{self.timediv_type}: "
                                f"{x:.0f}\n{label.title()}: {y:.4f}",
                                fontsize=10,
                                fontweight="bold",
                            )
                            sel.annotation.get_bbox_patch().set(
                                alpha=0.8,
                                color="white"
                            )

                        self.correlation_cursor_container[
                            line.get_label()
                        ] = cursor

    def add_tracker(
        self,
        text: str
    ) -> None:
        """
        Adds or updates a tracked element to be highlighted in the plots.

        Args:
            text (str):
                The name of the element to track.

        Notes:
            - Updates the main plots to reflect the tracked element.
            - Resets and re-applies cursors to the right-side graphs.
        """

        self.tracked_element = text.strip()
        self.update()
        self.set_right_side_graphs_cursors()

    def build_tracker(self) -> None:
        """
        Builds a text box for tracking a specific element in the plots.

        Notes:
            - Adds a text box UI element for user input to
            track a specific data element.
            - Associates the text box with the `add_tracker`
            method for interactivity.
        """

        self.ax_box_tracker = self.fig.add_axes([0.81, 0.005, 0.18, 0.05])
        self.text_box_tracker = TextBox(
            self.ax_box_tracker,
            f"Track {self.common_column}"
        )
        self.text_box_tracker.on_submit(self.add_tracker)

    def set_and_plot_corr_diff(self) -> None:
        """
        Plots the absolute difference between log and linear correlations.
        Colors the segments based on which correlation is dominant.
        """

        if (
            self.corr_log is None
            or self.corr_lin is None
            or self.timediv_range is None
        ):
            raise ValueError(
                "Error: Missing data: corr_log, corr_lin, or timediv_range"
            )

        corr_log = np.array(self.corr_log, dtype=float)
        corr_lin = np.array(self.corr_lin, dtype=float)

        if (
            len(corr_log) != len(corr_lin)
            or len(corr_log) != len(self.timediv_range)
        ):
            raise ValueError(
                "Error: Mismatched lengths of "
                "corr_log, corr_lin, or timediv_range"
            )

        abs_diff = np.abs(corr_log - corr_lin)
        is_log_dominant = np.abs(corr_log) > np.abs(corr_lin)

        x_values = np.array(list(self.timediv_range))

        ax = self.axes["corr_diff"]

        ax.plot(x_values, abs_diff, color="blue", label="corr_diff")

        segments = []
        colors = []
        for i in range(len(x_values) - 1):
            x_segment = x_values[i:i + 2]
            y_segment = abs_diff[i:i + 2]
            segments.append(list(zip(x_segment, y_segment)))

            color = "red" if is_log_dominant[i] else "green"
            colors.append(color)

        lc = LineCollection(
            segments,
            colors=colors,
            linewidths=2,
            alpha=0.8
        )
        ax.add_collection(lc)

        ax.set_xlabel(self.timediv_type, labelpad=-30)
        ax.set_xlim(self.timediv_range.start, self.timediv_range.stop)
        ax.set_ylabel(
            "|Corr(log) - Corr(lin)|",
            labelpad=-25,
            loc="center"
        )
        ax.set_ylim(0, 2)
        ax.set_yticks([0, 0.25, 1.75, 2])
        ax.text(
            0.5,
            0.5,
            f"Absolute Difference of Correlations\n"
            f" VS {self.timediv_type}",
            transform=ax.transAxes,
            fontsize=10,
            color="blue",
            alpha=0.2,
            ha="center",
            va="center",
            weight="bold",
        )

        red_patch = plt.Line2D([], [], color='red', label='log>lin')
        green_patch = plt.Line2D([], [], color='green', label='log<lin')
        ax.legend(handles=[red_patch, green_patch], loc='best')

    def set_and_plot_right_side_graph(
        self,
        graph: str
    ) -> None:
        """
        Plots and configures the correlation and
        p-value graph for a given axis.

        Args:
            graph (str):
                The name of the graph, either "log" or "lin".

        Notes:
            - Configures axis labels, legends, and titles dynamically.
            - Adds correlation and p-value curves to the specified graph.
        """

        ax = self.axes["corr_" + graph]

        ax.plot(
            np.array(self.timediv_range),
            self.corr_log if graph == "log" else self.corr_lin,
            label="corr " + graph,
            color="red" if graph == "log" else "green",
        )
        ax.plot(
            np.array(self.timediv_range),
            self.pvalue_log if graph == "log" else self.pvalue_lin,
            label="pvalue " + graph,
            color="purple" if graph == "log" else "olive",
        )

        ax.set_xlabel(self.timediv_type, labelpad=-27)
        ax.set_xlim(self.timediv_range.start, self.timediv_range.stop)
        ax.set_ylabel("Corr. Coeff. or Pvalue", labelpad=-30, loc="center")
        ax.set_ylim(-1, 1)
        ax.set_yticks([-1, -0.75, 0.75, 1])
        ax.text(
            0.5,
            0.5,
            graph.upper(),
            transform=ax.transAxes,
            fontsize=30,
            color="red" if graph == "log" else "green",
            alpha=0.08,
            ha="center",
            va="center",
            weight="bold",
        )
        ax.legend()

        if graph == "log":
            ax.set_title(f"Corr. Coeff. and Pvalue VS {self.timediv_type}")

    def build_mpl_window(
        self,
    ) -> None:
        """
        Builds the matplotlib window with all elements,
        including graphs, sliders, and trackers.

        Notes:
            - Sets up axes, colorbars, sliders, and right-side graphs.
            - Configures dynamic window resizing and graph adjustments.
        """

        self.build_fig_axes()

        self.build_colorbar(
            ax=self.axes["log"],
            extra_data=self.data_frames['extra_data_x']
        )

        self.build_slider(
            update_callback_function=self.update)

        self.build_tracker()

        self.set_and_plot_right_side_graph("log")
        self.set_and_plot_corr_diff()
        self.set_and_plot_right_side_graph("lin")

        self.fig.canvas.manager.set_window_title(
            f"{self.data_frames['data_x'].short_name} VS "
            f"{self.data_frames['data_y'].short_name} for each "
            f"{self.timediv_type} between "
            f"{self.timediv_range.start} and "
            f"{self.timediv_range.stop - 1}"
        )

    def pltshow(self) -> None:
        """
        Displays the matplotlib window and starts the animation if enabled.

        Raises:
            RuntimeError:
                If the figure is not initialized before calling this method.

        Notes:
            - Ensures the animation starts if `first_running` is True.
        """

        if self.fig is not None:
            if self.first_running:
                self.start_animation()
            plt.show()
        else:
            raise RuntimeError(
                "Figure not initialized.\n"
                "Make sure build_figure_axes Day02Ex03"
                "method has beed called before."
            )

    @typeguard.typechecked
    def set_interval_between_two_frames(
        self,
        interval: int = 100
    ) -> None:
        """
        Sets the time interval between two frames during the animation.

        Args:
            interval (int): the interval, in ms, between two frames.

        Notes:
            - A big interval will make the animation slower.
        """

        self.interval_between_two_frames = interval
