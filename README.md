# **Logarithmic scale VS Linear scale**

## **Overview**
This project demonstrates the impact of choosing a logarithmic or linear scale when visualizing data.
It provides an interactive tool to explore and compare data across different scales, emphasizing how each representation leads to unique patterns and insights.

Initially applied to datasets comparing **Gross Domestic Product (GDP) per capita** and **life expectancy**, the tool includes additional data such as population, and Gini coefficient to highlight the socio-economic disparities hidden behind national averages.

Designed with modularity in mind, the tool can handle any structured dataset. However, datasets must be pre-processed and cleaned to meet the following structure:
- The **first column** should contain the common header (e.g., `country`) across all datasets. The entities (or individuals in statistical terms) must overlap as much as possible to ensure robust and reliable results.
- The **remaining columns** should represent time periods, with headers as time intervals and bodies containing the respective data.

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

Usage Instructions :
The project contains the original datasets it has been developped with :
- 

    Load Your Data:
        Replace the default datasets with your own CSV files in the data/ folder.
        Ensure your files follow a structure with:
            A common column (e.g., country or entity name).
            Time-based columns for comparison.

    Configure the Tool:
        Adjust parameters in config.py (e.g., dataset paths, time ranges, labels).

    Interact:
        Use the slider to navigate through time.
        Compare visualizations directly as both scales are displayed simultaneously.
        Track entities of interest and analyze their behavior.

Example Datasets

    GDP per capita (adjusted for inflation): A measure of average income.
    Life Expectancy: Indicator of health and longevity.
    Gini Coefficient: Measure of inequality in income distribution.

Technology Stack

    Python:
        Matplotlib: Interactive scatter plots and visualizations.
        Pandas: Data manipulation and cleaning.
        NumPy: Numerical computations.
        mplcursors: Interactive point annotations.

Features for Developers

The tool is modular and can be extended or customized:

    Add new visualizations: Integrate additional types of graphs.
    Custom scaling options: Implement new scales beyond linear and logarithmic.
    Plug-and-Play Datasets: Adapt the framework to accommodate various data formats.

Contributions

Contributions are welcome!
To contribute:

    Fork the repository.
    Create a new branch:

    git checkout -b feature-new-feature

    Submit a pull request.

Author

Developed by Your Name, a Python enthusiast with a passion for data visualization and storytelling.
License

This project is licensed under the MIT License. See the LICENSE file for details.
