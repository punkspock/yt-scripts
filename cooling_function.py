import numpy as np
import pandas as pd


# import sutherland and dopita data
def loadCoolingData(filename):
    """
    Take in filename, load CSV file. Output file name, temperature column, and
    net cooling function column.

    """
# I'm sure there's a quicker way to get the column names.
    headers = [
        "log(T)", "ne", "nH", "nt", "log(lambda net)", "log(lambda norm)",
        "log(U)", "log(taucool)", "P12", "rho24", "Ci", "mubar"
        ]

    df = pd.read_csv(
        filename, sep="\t", header=None, names=headers, skiprows=4
        )
    logTempColumn = df["log(T)"]
    logLambdaColumn = df["log(lambda net)"]

    return df, logTempColumn, logLambdaColumn


if __name__ == "__main__":
    filename = "../Data/SutherlandDopita/m-00.csv"
    df, logTempColumn, logLambdaColumn = loadCoolingData(filename)
    # 5th-degree polynomial
    function = np.polyfit(logTempColumn, logLambdaColumn, 5)
    print(function)  # get coefficients

    # i'd like to visually check how close that approximation is.
