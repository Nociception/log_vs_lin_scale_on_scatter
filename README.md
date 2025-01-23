# **Logarithmic VS Linear scale**

## **Overview**
Realize the impact of choosing a logarithmic or linear scale when visualizing data and calculating statiscical indicators.

It provides an interactive tool to explore and compare data across different scales, emphasizing how each representation leads to unique patterns and insights.

Initially applied to datasets comparing **Gross Domestic Product (GDP) per capita** and **life expectancy**, the tool includes additional data such as population, and Gini coefficient.

![preview gif](preview.gif)

### **Required Datasets Architecture**
Designed with modularity in mind, the tool can handle any structured dataset. However, datasets must be pre-processed and cleaned to meet the following structure:
- The **first column** should contain the common header (e.g., `country`) across all datasets. The entities (or individuals in statistical terms) must overlap as much as possible to ensure robust and reliable results.
- The **remaining columns** should represent time periods, with headers as time intervals and bodies containing the respective data.
#### For instance:
| country     |   1800 |   1801 |   1802 |   1803 |
|:------------|-------:|-------:|-------:|-------:|
| Afghanistan |   28.2 |   28.2 |   28.2 |   28.2 |
| Albania     |   35.4 |   35.4 |   35.4 |   35.4 |
| Algeria     |   28.8 |   28.8 |   28.8 |   28.8 |


While automation for data cleaning is not included, following this structure ensures compatibility with the tool's framework. Data cleaning is essential for ensuring the presence of overlapping time periods across datasets (especially for `data_x`, `data_y`, and `data_point_size`).

---

## **Key Features**
- **Interactive Scatter Plots**:
  - Two simultaneous visualizations with regression line:
    - **Logarithmic scale** (top left section of the figure).
    - **Linear scale** (bottom left section of the figure).
  
- **Dynamic Correlation and P-Values**:
  - Computation and display of correlation coefficients and p-values for all available time periods (right sections of the figure).

- **Annotations and Highlighting**:
  - Hover over points or curves for detailed annotations.
  - Track specific entities or countries with a real-time focus feature.

- **Temporal Navigation**:
  - Analyze data trends dynamically across a customizable time range.
  - Press play/pause the animation to visualize scatter plots from contiguous time divisions.

---

## **Getting Started**

### **Installation**
1. Clone this repository:
   ```bash
   git clone https://github.com/Nociception/undisclosed_repo.git
   cd undisclosed_repo
   ```

2. Install the required dependencies (maybe in a virtual environment):

   (Optional but recommended) creating your virtual environment (in order to install everything necessary for this program, without any version conflicts with your possible own versions of some packages already installed on your system):
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

   (Mandatory) install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the tool:
   ```bash
    python3 poo.py
   ```

### **Initial settings (main function)**
Most of adjustable parameters are in the main function. Read the main's docstring for more details.

#### Datasets :
Four slots (and theorically a fivth, not functionnal so far): (the project contains the four original CSV datasets it has been developped with)
- `data_x`: income_per_person_gdppercapita_ppp_inflation_adjusted.csv [PPP stands for purchasing power parity](https://en.wikipedia.org/wiki/Purchasing_power_parity)
- `data_y`: life_expectancy_years.csv
- `data_point_size`: population_total.csv
- `extra_data_x`: Gini_coefficient.csv [Wikipedia page](https://en.wikipedia.org/wiki/Gini_coefficient)

As said before, it is possible to replace these datasets (provided that they meet the standard described in [this section](#required-datasets-architecture)). Make sure your data_cleaning for each dataset work properly, otherwise the program will fail.
	
## Development Process : how this project born and evolved
### Context
The big class within the code is named Day02Ex03: the exercise 03 of the day 02 of the "python for datascience" [42](https://42.fr/)'s piscine. This exercise gives us two csv ([income_per_person_gdppercapita_ppp_inflation_adjusted](income_per_person_gdppercapita_ppp_inflation_adjusted.csv) and [life_expectancy_years](life_expectancy.csv)), and asks to plot a scatter_plot such as [expected.jpg](expected.jpg), with GDP on X (log scale) and life_expectancy on Y. Eventually, we are informally asked if we see any correlation.
### Cascade
After I quite quickly solved the exercise, not calculating any correlation indicator was a bit shame. And it started a kind of a spiral: what about doing this (calculating it!), and that (for every year) and then that (being able to read each point's details)..., it came to this result (which I propably will improve again and again).

![Bob the sponge "So many possibilities" meme](so-many-possibilities-meme.jpg)
### GDP per capita may be insufficient ?
As this data is a mean for each country, I wondered how I could add any nuance (especially for points with a large GDP per capita without high life expectancy): colors according to a new data concerning wealth distribution. I then chose the Gini coefficient, which is unfortunatly not calculated for so many countries and years.
