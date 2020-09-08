import OH_fields as oh
import matplotlib.pyplot as plt

if __name__ == "__main__":
    ds, ad = oh.loadData(oh.file)
    oh.addFields()
    cut = oh.velocityCut(ad)

    wfile = open("../../Plots/%s.txt" % (oh.time), 'a')

    M_sun = oh.M_sun

    # calculations
    hIonMass = sum(cut["h_ion_mass"]) / M_sun
    hNeutralMass = sum(cut["h_neutral_mass"]) / M_sun
    hTotalMass = sum(cut["h_total_mass"]) / M_sun

    # print statements
    wfile.write("\nMass of ionized hydrogen: {:.2e}".format(hIonMass))
    wfile.write("\nMass of neutral hydrogen: {:.2e}".format(hNeutralMass))
    wfile.write("\nTotal hydrogen mass: {:.2e}".format(hTotalMass))
    wfile.close()

    # plot
    log_temp = oh.np.log10(cut["temperature"])
    # log_ttl = oh.np.log10(cut["h_total_mass"] / M_sun)
    log_ntl = oh.np.log10(cut["h_neutral_mass"] / M_sun)
    log_ion = oh.np.log10(cut["h_ion_mass"] / M_sun)

    fig, ax = plt.subplots()
    ax.scatter(log_temp, log_ntl, c="b", s=6, label="Neutral")
    ax.scatter(log_temp, log_ion, c="g", s=6, label="Ionized")
    plt.xlabel("log T (K)")
    plt.ylabel("$M_{\odot}$")
    ax.legend()

    plt.title(
        "Mass of Ionized and Neutral Hydrogen Over Temperature, %s" %
        (oh.time)
        )
    plt.savefig("../../Plots/ionized_neutral_%s.png" % (oh.time))
    plt.close()
