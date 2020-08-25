"""
06/12/2020

Sydney Whilden

Library of repeatedly used derived fields in YT. By importing this script you
import a bunch of derived field definitions and an easy way to add them to your
ipython session.

"""
# import statements
import yt
import numpy as np
from yt.units.yt_array import YTArray, YTQuantity

derived_fields = []  # array of all the derived fields in the library
"""
None of these fields are added yet. You have to add them using the add()
method.
"""


# define derived field class
class derivedField():
    """
    Creates a class of objects called "derived fields," of which each has a
    name, a definition function, and units.
    """

    def __init__(self, data, name, function, units):
        """
        Initialize new instance of a derived field.

        Parameters:
            name (str): Desired display name of the derived field (NOT the same
                as the name of the variable to which the instance is assigned.)

            function (callable): This is the function you want to define the
                new derived function.

            units (str): The expected units of the derived field (must be the
                same units as the ones returned by the calculation describing
                the field.)

        """
        self.name = name
        self.function = function
        self.units = units
        self.data = data

        derived_fields.append(self.name)  # appends itself to the list

    def add(self):
        """
        A method you can call on a derived field object to quickly add it to
        YT, without adding all the fields you don't need at that exact moment.
        """
        yt.add_field(
            ("gas", self.name), function=self.function, units=self.units
            )


def list():
    """
    List all available derived fields in the library.
    """
    print(derived_fields)


def numDens(field, data):
    nD = data["H_nuclei_density"] + data["He_nuclei_density"]

    return nD


def numDensSqr(field, data):
    nD2 = data["number_density"]**2

    return nD2


def lambdaT(field, data):
    """
    Uses coefficients from polyfit in coolingfunction.py to construct a
    5th-degree polynomial cooling function.

    Returns a YTArray with units W*m**3.
    """

    # coefficients of polyfit degree 5; these come from cooling_function.py
    a = 4.61963883e-02
    b = -1.58168108e+00
    c = 2.155327470e+01
    d = -1.45359217e+02
    e = 4.84925514e+02
    f = -6.58894838e+02

    lambdaT = []  # this can go. not even used

    # you have to do the math on the entire array at once.
    x = np.log10(data["temp"])  # log10 of temperature
    logLambda = a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f
    lambdaT = 10**logLambda  # undo log10
    # here i make a YTArray so i can specify the units
    lambdaT_units = YTArray(lambdaT, 'W*m**3')

    return lambdaT_units  # an array of values of the cooling function


def coolRate(field, data):
    """
    Calculates cooling rate of a cell by multiplying cooling function value for
    that cell by square of number density.

    Returns a YTArray with units W*m**(-3).
    """

    n = 1  # scale factor
    rCool = data["cooling_function"] * n*data["number_density_squared"]

    return rCool


def _nelec(field, data):
    """
    Electron number density
    """
    eND = data['H_nuclei_density'] + 2*data['He_nuclei_density']

    return eND

# ----------MAIN------------
def main(data):  # pass data source in as argument.

    # print(len(derived_fields))  # test

    # create field objects
    number_density = derivedField(data, "number_density", numDens, "m**(-3)")

    number_density_squared = derivedField(
        data, "number_density_squared", numDensSqr, "m**-6"
        )

    cooling_function = derivedField(
        data, "cooling_function", lambdaT, "W*m**3"
        )

    cooling_rate = derivedField(
        data, "cooling_rate", coolRate, "W*m**(-3)"
    )

    electron_number_density = derivedField(
        data, "electron_number_density", _nelec, "cm**(-3)"
    )


    list()  # shows you the menu.
