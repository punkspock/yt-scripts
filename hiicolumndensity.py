"""
Sydney Whilden
08/13/2020

Put a lower bound on column density of H II in Fox's high ion phases.
See page 1058 of Fox (2010)

"""

import OH_fields as oh
import OHmetallicity as om

if __name__ == "__main__":
    ds, ad = oh.loadData(oh.file)  # load data file into yt
    oh.addFields()  # add all the derived fields defined in oh
    cut = oh.velocityCut(ad)

    # CALCULATE
    total = cut["o_total_number"]
    total = total[(~oh.np.isnan(total))]  # try to avoid dividing by zero
    ion_fraction = cut["OVI_number"] / total
    # log_ion_fraction = oh.np.log10(ion_fraction)

    # don't necessarily do this with max
    if_max = oh.np.max(ion_fraction)  # max value of O VI/O I

    # oxygen abundance
    proj_x = ds.proj("OVI_number", "x", data_source=cut)
    o_abundance = proj_x["o_neutral_number"] / proj_x["h_neutral_number"]
    o_abundance = o_abundance[(~oh.np.isnan(o_abundance))]
    mean_o = oh.np.mean(o_abundance) # mean value of O abundance
    o5cd = proj_x["OVI_number"]  # O VI column density
    o5cd_mean = oh.np.mean(o5cd)

    h2cd = o5cd_mean / (if_max * mean_o)

    print("N(H II)_(O VI) >= %f" % (h2cd))
