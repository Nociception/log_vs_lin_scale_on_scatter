"""
Enable or disable debugging:
in the debug function (defined here: src/utils/debug.py)
(on VSCode, ctrl + Clic on the `debug` word just above to
reach its definition),
by switching on 0 or 1 the second condition in the if
(in this line (35th) `if debug and 1:`)
"""

from classes import Day02Ex03
import matplotlib
import typeguard
from utils import (  # noqa: F401
    debug,
    debug_decorator,
    timediv_test_value,
    target_test_value,
)
# noqa: F401 is used to silence flake8
# These functions are not used by default,
# but are available if needed.

if matplotlib.get_backend() != 'TkAgg':
    matplotlib.use('TkAgg')


def main() -> None:
    """
    Main function to set up and execute the Day02Ex03 application.

    Workflow:
        - Initializes the `Day02Ex03` object.
        - Adds paths for data and metadata.
        - Cleans and precomputes data.
        - Configures the matplotlib window and its elements.
        - Optionally enables autoplay.
        - Displays the application window.

    Most of all adjustable parameters lie her.
        For all add_data* or add_extra_data* methods:
        - data_file_name
        - `short_name`
        - `axis_label`
        - `unit`
        - specific parameter for add_data_point_size:
            `divider`; adjust it according to reach a proper point size.
        Set the title in the `add_title` method.
        Set the part of your data you want to study in
            the `add_timediv_range` method.
        Set the very important parameter `common_column`
            (necessary to merge the datasets)
            in the `add_common_column` method.
        Set the animation parameters:
            - `auto_play` in the `set_autoplay_at_start` method
                (`True` or `False`)
            - speed in the the `set_interval_between_two_frames` method
                in milliseconds.
    """

    try:
        exo03 = Day02Ex03()

        exo03.add_data_x_path(
            "data/gdppercapita_ppp_inflation_adjusted.csv",
            short_name="GDP per capita inflation adjusted at PPP",
            x_label="GDP per capita inflation adjusted at PPP",
            x_unit="USD"
        )
        exo03.add_data_y_path(
            "data/life_expectancy_years.csv",
            short_name="life expectancy",
            y_label="Life expectancy",
            y_unit="year"
        )
        exo03.add_data_point_size_path(
            "data/population_total.csv",
            short_name="population",
            divider=1e6
        )
        exo03.add_extra_data_x_path(
            "data/Gini_coefficient.csv",
            short_name="Gini coefficient"
        )
        # exo03.add_extra_data_y_path(
        #     "",
        #     short_name=""
        # )
        exo03.add_title(
            "Life Expectancy"
            " VS "
            "Inflation-adjusted GDP per capita "
            "at purchasing power parity (PPP)"
        )
        exo03.add_timediv_range(
            start=1800,
            stop=2050,
            init_value=1900,
            type="year",
        )
        exo03.add_common_column('country')

        exo03.clean_data_frames()
        exo03.precompute_data()

        exo03.build_mpl_window()
        exo03.update()
        exo03.set_right_side_graphs_cursors()

        exo03.set_autoplay_at_start(True)
        exo03.set_interval_between_two_frames(200)

        exo03.pltshow()

    except ValueError as error:
        print(f"{type(error).__name__}: {error}")
    except typeguard.TypeCheckError as error:
        print(f"{type(error).__name__}: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()
