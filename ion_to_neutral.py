"""

Sydney Whilden
09/05/2020

Calculate the fraction of all oxygen ions to all oxygen, and compare it to the
percentage of ionized hydrogen as predicted by ionizedmass.py to make sure
they agree.

"""
import OH_fields as oh

if __name__ == "__main__":
    ds, ad = oh.loadData(oh.file)
    oh.addFields()
    cut = oh.velocityCut(ad)
    wfile = open("../../Plots/%s.txt" % (oh.time), 'a')

    oNeutralFrac = oh.np.mean(cut["o_neutral_number"] / cut["o_total_number"])
    oIonFrac = 1 - oNeutralFrac

    hNeutralFrac = oh.np.mean(cut["h_neutral_number"] / cut["h_total_number"])
    hIonFrac = 1 - hNeutralFrac

    wfile.write(
        "\nPredicted ionization fraction of oxygen: {:.2e}".format(oIonFrac)
        )
    wfile.write(
        "\nPredicted ionization fraction of hydrogen:{:.2e}".format(
        oNeutralFrac)
        )
    wfile.close()
