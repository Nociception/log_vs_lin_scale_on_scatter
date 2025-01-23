import numpy as np

class LinReg:
    """
    Represents the results of a linear regression analysis.

    Attributes:
        corr (float):
            The correlation coefficient of the regression.
        predicted (np.ndarray):
            The predicted values resulting from the regression.
        pvalue (float):
            The p-value indicating the significance of the correlation.
    """

    def __init__(self,
                 predicted: np.ndarray,
                 corr: float,
                 pvalue: float):
        """
        Initializes a LinReg object with regression results.

        Parameters:
            corr (float):
                The correlation coefficient of the regression.
            predicted (np.ndarray):
                The predicted values from the regression model.
            pvalue (float):
                The p-value indicating the significance of the regression.
        """

        self.predicted: np.ndarray = predicted
        self.corr: float = corr
        self.pvalue: float = pvalue

    def show(self) -> None:
        """The class show method for a LinReg class object"""

        print("\n=== SHOW LinReg class object (START) ===")

        print(f"Correlation Coefficient (corr): {self.corr:.4f}")
        print(f"P-Value (pvalue): {self.pvalue:.4e}")

        print("\nPredicted Values (predicted):")
        print(self.predicted)

        print("\n=== SHOW LinReg class object (END) ===")
