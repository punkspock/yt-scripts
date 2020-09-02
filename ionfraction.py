"""
Sydney Whilden
08/11/2020

Calculate O VI/O and plot as a function of temperature.

"""

import OH_fields as oh  # numpy and YT are imported through this script
import matplotlib.pyplot as plt


def ionFractionCalc():
    """
    Calculate O VI/O
    """

    t_o = cut["o_total_number"]
    ionFraction = cut["OVI_number"] / t_o

    return ionFraction


def plot(x, y):
    """
    Makes basic scatter plot of log O VI/O over log T

    Parameters:

        x (array): log of temperature
        y (array): log of O VI/O

    """
    fig = plt.figure(figsize=(15, 10))
    plt.scatter(x, y, s=4) # did s=4 for consistency with Eric's
    plt.xlabel("log T (K)")
    plt.ylabel("log (O VI/O)")
    plt.xlim(0, 8)
    plt.title("O VI/O Over Temperature, %s" % (oh.time))
    plt.savefig("../../Plots/ion_fraction_%s.png" % (oh.time))
    plt.close()


def express5(x,  y):
    """

    Outputs 5th-degree polynomial expression for the relationship between two
    equal-size arrays

    Parameters:
        x (array)
        y (array)

    """
    a, b, c, d, e, f = oh.np.polyfit(x, y, 5)

    # can't write it like below until you're using sympy. x is an array rn 
    # expr = a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f

    return a, b, c, d, e, f


def express3(x, y):
    """

    Outputs 3rd-degree polynomial expression relating two equal-size arrays

    """

    a, b, c, d = oh.np.polyfit(x, y, 3)

    return a, b, c, d



if __name__ == "__main__":
    ds, ad = oh.loadData(oh.file)  # load data file into yt
    oh.addFields()  # add all the derived fields defined in oh
    cut = oh.velocityCut(ad)

    # CALCULATE
    ionFraction = ionFractionCalc()
    logIonFraction = oh.np.log10(ionFraction)

    # PLOT
    logTemp = oh.np.log10(cut["temperature"])
    plot(logTemp, logIonFraction)

    mean = oh.np.mean(ionFraction)
    print("Mean value of O VI/O: %f" % (mean))

    # now find the rate of change w/ respect to temperature
    # have to do it with logTemp and logIonFraction because yt can't handle the numbers
    #    you get when you square the temperature values
    a, b, c, d, e, f = express5(logTemp, logIonFraction)

    # plot the expression
    logCurve = []  # initialize

    # calculate using the coefficients we generated to see how the curve fits
    for x in logTemp:
        y = a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f
        logCurve.append(y)

    fig = plt.figure(figsize=(15, 10))
    plt.plot(logTemp, logCurve)
    plt.savefig("../../Plots/curve.png")
    plt.close()

    #der = diff(expr, x)  # take derivative using symbolic differentiation
