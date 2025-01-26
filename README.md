# **Overview**
Realize the impact of choosing a logarithmic or linear scale when visualizing data and calculating statiscical indicators ; see both at once !

Compare the correlation difference between log and lin across time.

Initially applied to datasets comparing **Gross Domestic Product (GDP) per capita** and **life expectancy**, the tool includes additional data such as population, and Gini coefficient.

![preview.gif](https://github.com/Nociception/assets_storage/blob/main/log_vs_lin_scale_on_scatter/preview.gif)

---

# Summary
1. [Getting Started](#Getting-Started)
2. [Setting basic tools](#Setting-basic-tools)
3. [Extended Use](#Extended-Use)
4. [Key Features](#Key-Features)
5. [Development Process](#Development-Process)
6. [Discussion](#Discussion)

---

# **Getting Started**
## **Installation and running**
Note: most of these steps are managed with a Makefile. Take a look at the [commands](Makefile).
Note: if you do not know/have git, python3, make, please go first to [this section](#Setting-basic-tools).
1. Clone this repository:
   ```bash
   git clone https://github.com/Nociception/log_vs_lin_scale_on_scatter.git ; cd log_vs_lin_scale_on_scatter
   ```
2. Install the required dependencies (maybe in a **virtual environment**):
   (Optional but recommended) Create your virtual environment (in order to install everything necessary for this program, without any version conflicts with your possible own versions of some packages already installed on your local system):
   ```bash
   make create-virtual-env
   ```
   (Mandatory) install all dependencies:
   ```bash
   make install
   ```
3. Run the tool:
   ```bash
   make
   ```
4. (Finally, if you have used a virtual environment) Deactivate the virtual environment:
   Deleting the cloned repo will not be enough.
   ```bash
   deactivate
   ```

---

# Setting basic tools
This section is designed for users who do not know git, python3 or make. Skip it is not the case.
Otherwise, read carefuly the following steps.
1. Open a terminal window which should look like this (search among your app/software list):
![terminal_picture](https://github.com/Nociception/assets_storage/blob/main/global/terminal_picture.png)

You are now going to type some things in this basic window which accepts text, also called commands:
type it, and then press Enter to run it.
You cannot type anything you would like to, as not everything is a valid command: `lol` will not work, whereas `ls` will.

The following steps contain black boxes where proper commands are showed. To run the program, follow then these steps by typing and running these commands in your terminal window.
Some of them may require you to type your computer password. You will not see any * character as you are maybe used to. If you want to move on these steps with these commands, type it and press Enter.

Some commands will lead to new lines (not typed by you) display. They sometime can be numerous ; reading all of them can be quite long, provided that you would understand them. During this display, you cannot type any new command. Once the process is done, the prompt is given back to you, and you can type a new command.

Tip: spot the little square on each of these code black boxes (just below in this tutorial), on top right: click on it to copy the command (it can be faster and easier than selecting and copying it). Once back in your terminal, Ctrl + Shift + v to paste it. (The Shift is important ; without, the paste could somehow fail).

2. Install `git`:
   You maybe already have it ; check it out:
   ```bash
   git --version
   ```
   If you have something like: git version 2.34.1 (version number can be different)
   Then go to the step 3.
   Otherwise, install it:
   ```bash
   sudo apt install git
   ```

   You can now clone the project, but you should reach the end of this section before. Read more about git [here](https://en.wikipedia.org/wiki/Git)

3. Install python3:
   As this is a python project, you need `python3` installed on your computer:
   You maybe already have it ; check it out:
   ```bash
   python3 --version
   ```
   If you have something like: Python 3.10.12 (version number can be different)
   Then go to the step 4.
   Otherwise, install it:
   ```bash
   sudo apt install python3
   ```
   You also need the package manager `pip3`:
   ```bash
   sudo apt install python3-pip
   ```

   [Python](https://en.wikipedia.org/wiki/Python_(programming_language) is language programming, used to develop this program. Installing it allows you to run it (which is not possible without).

4. (if necessary and prefered) Install `make`:
   You can run the program with or without `make`.
   The Makefile manages some things for you, that you definetly can do on your own.
   But if you would like to use the Makefile, then install `make`.

   You maybe already have it ; check it out:
   ```bash
   make --version
   ```
   If you have something like:

   GNU Make 4.3
   Built for x86_64-pc-linux-gnu
   Copyright (C) 1988-2020 Free Software Foundation, Inc.
   License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
   This is free software: you are free to change and redistribute it.
   There is NO WARRANTY, to the extent permitted by law.

   Then skip this step and go back to [the main installation guide](#Getting-Started).

   Otherwise, install it:
   ```bash
   sudo apt install make
   ```
   By the way, it could be useful for other projects you would clone!
   Some of them automate many things.
   It would require a lot of manual typing in your terminal without it.
   Read more about `make` [here](https://en.wikipedia.org/wiki/Make_(software)).

   You and your computer are now ready to install the program! Go back to [the main installation guide](#Getting-Started).

---

# Extended use
## **Initial settings (main function)**
Most of adjustable parameters are in the main function. Read the main's docstring for more details.
## **Required Datasets Architecture**
Designed with modularity in mind, the tool can handle any structured dataset. However, datasets must be retrieved from .csv files, and be pre-processed and cleaned to meet the following structure:
- The **first column** should contain the common header (e.g., `country`) across all datasets. The entities (or individuals in statistical terms) must overlap as much as possible to ensure robust and reliable results.
- The **remaining columns** should represent time periods, with headers as time intervals and bodies containing the respective data.
### For instance:
| country     |   1800 |   1801 |   1802 |   1803 |
|:------------|-------:|-------:|-------:|-------:|
| Afghanistan |   28.2 |   28.2 |   28.2 |   28.2 |
| Albania     |   35.4 |   35.4 |   35.4 |   35.4 |
| Algeria     |   28.8 |   28.8 |   28.8 |   28.8 |


While automation for data cleaning is not included, following this structure ensures compatibility with the tool's framework. Data cleaning is essential for ensuring the presence of overlapping time periods across datasets (especially for `data_x`, `data_y`, and `data_point_size`).

### Datasets :
Four slots (and theorically a fivth, not functionnal so far): (the project contains the four original CSV datasets it has been developped with)
- `data_x`: gdppercapita_ppp_inflation_adjusted.csv [PPP stands for purchasing power parity](https://en.wikipedia.org/wiki/Purchasing_power_parity)
- `data_y`: life_expectancy_years.csv
- `data_point_size`: population_total.csv
- `extra_data_x`: Gini_coefficient.csv [Wikipedia page](https://en.wikipedia.org/wiki/Gini_coefficient)

As said before, it is possible to replace these datasets (provided that they meet the standard described in [this section](#required-datasets-architecture)). Make sure your data_cleaning for each dataset work properly, otherwise the program will fail.

---

# **Key Features**
- **Interactive Scatter Plots**:
  - Two simultaneous visualizations with regression line:
    - **Logarithmic scale** (top left section of the figure).
    - **Linear scale** (bottom left section of the figure).
    Please note that the log scale is only applied on the X axis of the top left graph.
  
- **Dynamic Correlation and P-Values**:
  - Computation and display of correlation coefficients and p-values for all available time periods (right sections of the figure).
  - Middle rigth-side graph: Visualize the correlation difference across time.

- **Annotations and Highlighting**:
  - Hover over points or curves for detailed annotations.
  - Track specific entities or countries with a real-time focus feature.

- **Temporal Navigation**:
  - Analyze data trends dynamically across a customizable time range.
  - Press play/pause the animation to visualize scatter plots from contiguous time divisions.

---

# Development Process
How this project born and evolved.
## Context
The big class within the code is named Day02Ex03: [the exercise 03 of the day 02 of the "python for datascience"](https://github.com/Nociception/piscine_python_for_datascience/tree/master/Python-2-DataTable/ex03) [42](https://42.fr/)'s piscine. This exercise gives us two CSV ([gdppercapita_ppp_inflation_adjusted](data/gdppercapita_ppp_inflation_adjusted.csv) and [life_expectancy_years](data/life_expectancy.csv)), and asks to plot a scatter plot, with GDP on X (log scale) and life expectancy on Y. Eventually, we are informally asked if we see any correlation.

![expected.jpg](https://github.com/Nociception/assets_storage/blob/main/log_vs_lin_scale_on_scatter/expected.jpg)
## Spiral
After I quite quickly solved the exercise, not calculating any correlation indicator was a bit shame to me. And it started a kind of a spiral: what about doing this (calculating it!), and that (for every year) and then that (being able to read each point's details), and that (using the [population.csv file](data/population.csv) to set the points' size)..., it came to this result (which I propably will improve again and again).

![Bob the sponge "So many possibilities" meme](https://github.com/Nociception/assets_storage/blob/main/global/so-many-possibilities-meme.jpg)
## GDP per capita may be insufficient ?
As this data is a mean for each country, I wondered how I could add any nuance (especially for points with a large GDP per capita without high life expectancy): colors according to a new data concerning wealth distribution. I then chose the Gini coefficient, which is unfortunatly not calculated for so many countries/years, and also not perfect (other indicators were also possible, such as Theil index, or Hover index).

---

# Discussion
This project has been started for two main reasons:
- Proposing a tool to visualize the difference... (Already explained above)
- Discovering better Matplotlib, and applying OOP aproach
It is then more a pedagogical project than a serious/professional one.

Many choices (and probably most of my code) are questionable:
- probably polar > pandas
- more inner classes
- responsive could be better
- transitions between two timedivs could be more fluid
And probably many other aspects ; I am of course open to feedback.

Feature ideas for next versions:
- add a remove_outliers tool, with adjustable criteria
- allow to plot scatter for one targeted entity (country with the original data), and be able to go back to the overall scatter
- allow to provide only two CSV (no data_point_size (n)or extra_data_x)
- allow to receive (as input data) entities group, for targeting them in the scatter plot (for example: EU, former USSR, military alliances, free trade agreement, continent, any group in fact)
