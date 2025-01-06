# **Logarithmic scale VS Linear scale**

## **Overview**
This project demonstrates the impact of choosing a logarithmic or linear scale when visualizing data.
It provides an interactive tool to explore and compare data across different scales, emphasizing how each representation leads to unique patterns and insights.

Initially applied to datasets comparing **Gross Domestic Product (GDP) per capita** and **life expectancy**, the tool includes additional data such as population, and Gini coefficient to highlight the socio-economic disparities hidden behind national averages.

### **Required Datasets Architecture**
Designed with modularity in mind, the tool can handle any structured dataset. However, datasets must be pre-processed and cleaned to meet the following structure:
- The **first column** should contain the common header (e.g., `country`) across all datasets. The entities (or individuals in statistical terms) must overlap as much as possible to ensure robust and reliable results.
- The **remaining columns** should represent time periods, with headers as time intervals and bodies containing the respective data.
For instance :
|Country     | 1800 | 1801 | 1802 |
|------------|------|------|------|
|Afghanistan | 28.2 | 28.2 | 28.2 |
|
|Albania     | 27   | 27   | 27   |


While automation for data cleaning is not included, following this structure ensures compatibility with the tool's framework. Data cleaning is essential for ensuring the presence of overlapping time periods across datasets (especially for `data_x`, `data_y`, and `data_point_size`).

---

## **Key Features**
- **Interactive Scatter Plots**:
  - Two simultaneous visualizations with regression line:
    - **Logarithmic scale** (top section of the figure).
    - **Linear scale** (bottom section of the figure).
  
- **Dynamic Correlation and P-Values**:
  - Computation and display of correlation coefficients and p-values for all available time periods.

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
   git clone https://github.com/yourusername/data-visualization-tool.git
   cd data-visualization-tool
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the tool:
   ```bash
    python main.py
   ```

### **Initial settings (main function)**
Most of adjustable parameters are in the main function :

#### Datasets :
Four slots (and theorically a fivth, not functionnal so far): (the project contains the four original CSV datasets it has been developped with)
- `data_x`: income_per_person_gdppercapita_ppp_inflation_adjusted.csv [PPP stands for purchasing power parity](https://en.wikipedia.org/wiki/Purchasing_power_parity)
- `data_y`: life_expectancy_years.csv
- `data_point_size`: population_total.csv
- `extra_data_x`: Gini_coefficient.csv [Wikipedia page](https://en.wikipedia.org/wiki/Gini_coefficient)

As said before, it is possible to replace these datasets (provided that they meet the standard described in [this section](#required-datasets-architecture) ). Make sure your data_cleaning for each dataset work properly, otherwise the program will fail.
	
## Development Process : how this project born and evolved
### Context
