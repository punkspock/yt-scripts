"""
Sydney Whilden
11/11/2020

Test what happens to the ionization curve O VI/O when we change starting
abundance to different values.

"""

import OH_fields as oh  # as always.
import matplotlib.pyplot as plt

# initialize arrays for Ac and Aa

Aa = [0, 0.1, 0.5, 1]  # ambient
colors = ['r', 'b', 'g']
# Ac = []  # cloud  # actually don't need to change this
Ac = 0.001  # in solar masses

def ionFrac(ion1, ion2):  # ion fraction calculation. just to keep it simple
    abundance = ion1 / ion2  # both of these arguments are ARRAYS
    log_ab = oh.np.log10(abundance)

    return log_ab


if __name__ == "__main__":
    ds, ad = oh.loadData(oh.file)
    oh.addFields()
    cut = oh.velocityCut(ad)  # getting regular shit out of the way

    # get your graph started
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)
    plt.xlabel("log(T)")
    plt.ylabel("log([O/H])")
    plt.title("Polynomial fit of [O/H], %s" % (oh.time))

    # make sure the arrays are equal
    i = 0  # initialize

    while i < len(Aa):
        # Usually functions go before the main part of the function, but here,
        # I need them to be defined in the loop so I can reuse them with diff-
        # erent parameters a number of times. If yt would just allow me to pass
        # in arguments in definition functions...

        def newAbundance(field, ad):  # set the new Aa, Ac vals to get new A
            """

            Set new abundance parameters

            """
            # AcNew = Ac[i]
            AcNew = Ac
            AaNew = Aa[i]

            ANew = AcNew*ad["ambient_fraction"] + AaNew*ad["cloud_fraction"]

            return ANew

        oh.yt.add_field(
            ("gas", "new_abundance"), units='dimensionless',
            function=newAbundance, force_override=True
        )

        def changeFactor(field, ad):  # determine the factor to multiply by
            """

            A'/A

            """
            A = ad["o_total_number"] / ad["h_total_number"]
            factor = ad["new_abundance"] / A

            return factor

        oh.yt.add_field(
            ('gas', 'change_factor'), units='dimensionless',
            function=changeFactor, force_override=True
        )

        newOxy = cut['o_neutral_number'] * cut['change_factor']
        newHydro = cut['h_neutral_number']  # should i multiply by cf here too?
        logTemp = oh.np.log10(cut['temperature'])
        logTemp = logTemp[(~oh.np.isnan(logTemp)) & (~oh.np.isinf(logTemp))]

        # get the abundance set up
        logAb = ionFrac(newOxy, newHydro)
        logAb = logAb[(~oh.np.isnan(logAb)) & (~oh.np.isinf(logAb))]
        logAb = logAb[0:len(logTemp)]  # make arrays the same length

        # make sure logAb and logTemp arrays are same length so we can fit them
        if len(logAb) > len(logTemp):
            logAb = logAb[0:len(logTemp)]
        elif len(logTemp) > len(logAb):
            logTemp = logTemp[0:len(logAb)]
        elif len(logTemp) == len(logAb):
            pass
        else:
            print("exception: can't compare array lengths")
            break

        # do a polynomial fit

        # has an illegal value
        x = oh.np.linspace(2.5, 6.5, num=150)  # create your x-axis for plot
        # you need to create the x-axis because plotting function, not scatter
        y = []  # initialize

        a, b, c, d, e, f = oh.np.polyfit(logTemp, logAb, 5)  # get coeffs

        for i in x:
            j = a*i**5 + b*i**4 + c*i**3 + d*i**2 + e*i + f
            y.append(j)

        # plot the fit
        ax.plot(x, y, c='r', linewidth=4)

        i += 1  # iterate

    ax.legend()
    plt.savefig("../../Plots/abundance_%s.png" % (oh.time))
    plt.close()




# plot
