"""
05/22/2020

Find the cooling rate per unit volume.

"""
# -------------------------- import statements --------------------------------
import yt
import numpy as np
from yt.units.yt_array import YTArray


# ------------------------ function definitions -------------------------------
# define number density field
# This requires an assumption that all the gas is H, He, pretty much
def numberDensity(field, ad):
    """
    Field definition function for number density. Sums the number density of
    hydrogen nuclei and of helium nuclei, derived fields I found in YT.

    Returns YTArray with units 1/cm**3.
    """

    # using derived fields I found
    nD = ad["H_nuclei_density"] + ad["He_nuclei_density"]

    # alternate method:
    # make a YTQuantity to give H_mass units
    # H_mass = YTQuantity(1.6735575e-24, 'g')  # in grams
    # nD = ad["density"] / H_mass

    return nD


# define field for square of number density
def numDensSqr(field, ad):
    """
    Field definition function for the square of number density.

    Returns YTArray with units m**(-6)
    """

    nDS = ad["number_density"]**2

    return nDS


# define cooling function
def lambdaT(field, ad):
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

    lambdaT = []

    # you have to do the math on the entire array at once.
    x = np.log10(ad["temp"])  # log10 of temperature
    logLambda = a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f
    lambdaT = 10**logLambda  # undo log10
    # here i make a YTArray so i can specify the units
    lambdaT_units = YTArray(lambdaT, 'W*m**3')

    return lambdaT_units  # an array of values of the cooling function


# define cooling rate
def coolRate(field, ad):
    """
    Calculates cooling rate of a cell by multiplying cooling function value for
    that cell by square of number density.

    Returns a YTArray with units W*m**(-3).
    """

    n = 1  # scale factor
    rCool = ad["cooling_function"] * n*ad["number_density_squared"]

    return rCool


# --------------------- the main part where stuff happens ---------------------
if __name__ == "__main__":

    # load data
    file = "../Data/4.2.1.density_sap_hdf5_plt_cnt_0075"  # specify file name
    ds = yt.load(file)  # load data

    ad = ds.all_data()  # why do we do this step again?

    # add number density field
    yt.add_field(
        ("gas", "number_density"), function=numberDensity, units="m**(-3)",
        force_override=True
        )

    yt.add_field(
        ("gas", "number_density_squared"), function=numDensSqr,
        units="m**(-6)", force_override=True
        )

    # create cooling function field
    yt.add_field(
        ("gas", "cooling_function"), function=lambdaT,  # Sutherland & Dopita
        units="W*m**3", force_override=True
        )

    # create cooling rate field
    yt.add_field(
        ("gas", "cooling_rate"), function=coolRate, units="W/m**3",
        force_override=True
        )

    # project cooling rate
    plt1 = yt.ProjectionPlot(ds, "x", "cooling_rate")
    plt2 = yt.ProjectionPlot(ds, "y", "cooling_rate")
    plt3 = yt.ProjectionPlot(ds, "z", "cooling_rate")

    # save plots
    plt1.save("../Plots/Cooling Rate/cooling_rate_x.png")
    plt2.save("../Plots/Cooling Rate/cooling_rate_y.png")
    plt3.save("../Plots/Cooling Rate/cooling_rate_z.png")

    # alternate method
    # plt2 = yt.ProjectionPlot(
    #     ds, "x", "cooling_function", weight_field="number_density_squared"
    #     )
