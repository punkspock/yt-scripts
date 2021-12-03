# make a simple O VI projection plot with no cell cuts.

import OH_fields as oh
import sys

if __name__ == "__main__":

    if len(sys.argv[1]) > 1:
    	epoch = sys.argv[1]  # epoch is a string

    # format the epoch
    while len(epoch) < 4:
        epoch = "0{}".format(epoch)  # add zeroes until right length

    time = "t={} Myr".format(epoch)

    file = "../../Data/4.2.1.density/4.2.1.density_sap_hdf5_plt_cnt_{}".format(epoch)
    ds, ad = oh.loadData(file)

    oh.addFields()

    # make plot
    oh.yt.ProjectionPlot(ds, "y", ("flash", "o5  ")).save(
        "../../Plots/ovi_projection_{}.png".format(time)
        )
