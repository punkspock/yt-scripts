"""
06/05/2020
Sydney Whilden

This is the beginning of a package to help operate YT more quickly.
"""
import yt


def load(inFile):
    """
    Load in a file quickly by specifying the pathway.

    Parameters:
        inFile (str): Pathway to file containing desired data set

    """
    dataSet = yt.load(inFile)
    allData = dataSet.all_data()

    return dataSet, allData


if __name__ == "__main__":

    # get file name
    filename = input("Specify data file path as string: ")

    ds, ad = load(filename)  # load file
