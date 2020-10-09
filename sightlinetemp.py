"""
Sydney Whilden
10/09/2020

Plot projection of column density of O VI over temperature averaged over a
sight line.

"""

import OH_fields as oh
import ionfraction as ifr
import matplotlib.pyplot as plt


def dummyField(field, ad):
    ones = ad["density"] / ad["density"]

    return ones


if __name__ == "__main__":
    # add this field we just made. has to go first for some reason
    oh.yt.add_field(
        ("gas", "dummy"), units="dimensionless", function=dummyField,
        force_override=True
    )

    # now the regular stuff
    ds, ad = oh.loadData(oh.file)
    oh.addFields()
    cut = oh.velocityCut(ad)
    # wfile = open("../../Plots/%s.txt" % (oh.time), 'a')

    #ionFraction = ifr.ionFractionCalc(cut)

    proj_x = ds.proj("temperature", "x", method="sum", data_source=cut)

    # get the average temperature
    avgTemp = proj_x["temperature"] / proj_x["gas", "dummy"]

    logIonFrac = oh.np.log10(proj_x["OVI/O"])  # this is PROJECTED

    logTemp = oh.np.log10(avgTemp)  # averaged over the sight line

    fig = plt.figure(figsize=(15, 10))
    plt.scatter(logTemp, logIonFrac)
    plt.xlabel("log(T) K")
    plt.ylabel("log(O VI/O)")
    plt.savefig("../../Plots/projectedionfrac_%s.png" % (oh.time))
    plt.close()
