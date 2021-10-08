"""
Sydney Whilden
08/11/2020

Calculate O VI/O and plot as a function of temperature.

"""

import OH_fields as oh  # numpy and YT are imported through this script
import matplotlib.pyplot as plt
import read_gnat as rg
import sys
import scaleeverything as se


def ionFractionCalc(cut, scale_arg):
    """
    Calculate O VI/O
    """
    if scale_arg == 'scaled':
        t_o = cut['o_total_scaled']
        ovi = cut['OVI_scaled']
    elif scale_arg == 'unscaled':
        t_o = cut['o_total_number']
        ovi = cut['OVI_number']
    else:
        t_o = cut['o_total_number']  # default to unscaled
        ovi = cut['OVI_number']

    ionFraction = ovi / t_o

    return ionFraction


def ionFractionNew(cut):
    """
    Calculate O VI/O
    """

    t_o = cut["o_total_number"]
    ionFraction = cut["OVI_number"] / t_o * cut["change_factor"]

    return ionFraction


def plot(x, y, epoch):
    """
    Makes basic scatter plot of log O VI/O over log T

    Parameters:

        x (array): log of temperature
        y (array): log of O VI/O

    """
    fig = plt.figure(figsize=(15, 10))
    plt.scatter(x, y, s=4)  # did s=4 for consistency with Eric's
    plt.xlabel("log T (K)")
    plt.ylabel("log (O VI/O)")
    plt.xlim(0, 8)
    plt.title("O VI/O Over Temperature, t={}".format(epoch))
    plt.savefig('../../Plots/ion_fraction_{}.png'.format(epoch))
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
    # ds, ad = oh.loadData(oh.file)  # load data file into yt
    # oh.addFields()  # add all the derived fields defined in oh
    # cut = oh.velocityCut(ad)
    # wfile = open("../../Plots/%s.txt" % (oh.time), 'a')
    #
    # # CALCULATE
    # q = input("Are you changing the abundance? (y/n): ")
    # if q == "n":
    #     ionFraction = ionFractionCalc(cut)
    # elif q == "y":
    #     ionFraction = ionFractionNew(cut)

    if len(sys.argv[1]) > 1:
        epoch = sys.argv[1]

    if len(sys.argv[2]) > 1:
        scale_arg = sys.argv[2]

    file, time, ds, ad, cut = oh.main(epoch)
    se.main()
    wfile = open('../../Plots/{}.txt'.format(epoch), 'a')

    ionFraction = ionFractionCalc(cut, scale_arg)
    logIonFraction = oh.np.log10(ionFraction)
    logIonFraction = logIonFraction[(~oh.np.isnan(logIonFraction)) & (
        ~oh.np.isinf(logIonFraction))]

    # find the mean value
    mean = oh.np.mean(ionFraction)
    wfile.write("Mean value of O VI/O: %f" % (mean))
    wfile.close()

    # PLOT
    temp = cut["temperature"]
    logTemp = oh.np.log10(cut["temperature"])

    # make basic plot of the curve BEFORE doing polyfit
    plot(logTemp, logIonFraction, epoch)

    # necessary for polyfit.
    lT = logTemp[(~oh.np.isnan(logTemp)) & (~oh.np.isinf(logTemp))]
    # make sure the arrays are the same length
    # this is a temporary solution. not good if many data points removed
    #   from logTemp.
    lIF = logIonFraction[0:len(lT)]

    # now find the rate of change w/ respect to temperature
    # have to do it with logTemp and logIonFraction because yt can't handle the
    #    numbers you get when you square the temperature values
    a, b, c, d, e, f = express5(lT, lIF)

    # plot the expression
    logCurve = []  # initialize

    # calculate using the coefficients we generated to see how the curve fits
    x = oh.np.linspace(2.5, 6.5, num=150)  # for curve-plotting purposes

    for i in x:
        y = a*i**5 + b*i**4 + c*i**3 + d*i**2 + e*i + f
        logCurve.append(y)

    # Read in Gnat & Sternberg data
    df = rg.readGnat()
    gnat_x, gnat_y = rg.logData(df)

    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)
    ax.scatter(logTemp, logIonFraction, label='Cell')  # use "old" versions of the arrays
    ax.plot(x, logCurve, c='r', linewidth=4, label='Simulation fit')
    ax.plot(gnat_x, gnat_y, c='c', linewidth=4, label='Gnat & Sternberg (2007)')
    ax.set_xlim(3.0, 6.5)
    ax.set_ylim(-4.0, 0)
    ax.set_title('O VI/O vs temperature, t={} Myr'.format(epoch))
    ax.set_xlabel("log(T)")
    ax.set_ylabel("log(O VI/O)")
    ax.legend()
    plt.savefig("../../Plots/curve_t={} Myr.png".format(epoch))
    plt.close()

    f = open('coefficients_t={}'.format(epoch), 'w')
    f.write("{},{},{},{},{},{}".format(a, b, c, d, e, f))
    f.close()
