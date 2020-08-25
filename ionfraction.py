"""
Sydney Whilden
08/11/2020

Calculate O VI/O I and plot as a function of temperature.
*** Change to over TOTAL OXYGEN
"""

import OH_fields as oh  # numpy and YT are imported through this script
import matplotlib.pyplot as plt

if __name__ == "__main__":
    ds, ad = oh.loadData(oh.file)  # load data file into yt
    oh.addFields()  # add all the derived fields defined in oh
    cut = oh.velocityCut(ad)

    # CALCULATE
    t_o = cut["o_total_number"]
    t_o = t_o[(~oh.np.isnan(t_o))]  # try to avoid dividing by zero
    ion_fraction = cut["OVI_number"] / t_o
    log_ion_fraction = oh.np.log10(ion_fraction)

    # PLOT
    log_temp = oh.np.log10(cut["temperature"])
    fig = plt.figure(figsize=(15, 10))
    plt.scatter(log_temp, log_ion_fraction, s=4)
    # s=4 for consistency with Eric's
    plt.xlabel("log T (K)")
    plt.ylabel("log (O VI/O)")
    # plt.ylim(0, 10)
    plt.xlim(0, 8)
    plt.title("O VI/O Over Temperature, %s" % (oh.time))
    plt.savefig("../Plots/IonizedRatio/ion_fraction_%s.png" % (oh.time))
    plt.close()
    # plt.show()  # test
