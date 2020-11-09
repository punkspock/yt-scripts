"""
Sydney Whilden
08/11/2020

Import OH_fields fields and use them to calculate metallicity using
oxygen abundance [O/H], from [O I/ H I]

"""

import OH_fields as oh


if __name__ == "__main__":
    ds, ad = oh.loadData(oh.file)
    oh.addFields()
    cut = oh.velocityCut(ad)
    wfile = open("../../Plots/%s.txt" % (oh.time), 'a')

    # COLUMN DENSITY CALCULATIONS
    # Should probably change these to neutral numbers. Check on that.

    # projections in each direction
    proj_x = ds.proj("o_total_number", "x", data_source=cut)
    proj_y = ds.proj("o_total_number", "y", data_source=cut)
    proj_z = ds.proj("o_total_number", "z", data_source=cut)

    # oxygen column densities
    ocd_x = proj_x["o_neutral_number"]
    ocd_y = proj_y["o_neutral_number"]
    ocd_z = proj_z["o_neutral_number"]

    # hydrogen column densities
    hcd_x = proj_x["h_neutral_number"]
    hcd_y = proj_y["h_neutral_number"]
    hcd_z = proj_z["h_neutral_number"]

    # METALLICITY CALCULATIONS
    # log(O I/H I) solar = -3.31
    log_sun = -3.31  # from Fox 2010

    # x direction
    mcy_x = ocd_x / hcd_x
    mcy_x = mcy_x[(~oh.np.isnan(mcy_x))]
    mcy_x = oh.np.log10(mcy_x) - log_sun
    mean_mx = oh.np.mean(mcy_x)

    # y direction
    mcy_y = ocd_y / hcd_y
    mcy_y = mcy_y[(~oh.np.isnan(mcy_y))]
    mcy_y = oh.np.log10(mcy_y) - log_sun
    mean_my = oh.np.mean(mcy_y)

    # z direction
    mcy_z = ocd_z / hcd_z
    mcy_z = mcy_z[(~oh.np.isnan(mcy_z))]
    mcy_z = oh.np.log10(mcy_z) - log_sun
    mean_mz = oh.np.mean(mcy_z)

    print("Method 1: Using column densities of O I and H I\n")
    print("Metallicity in X, Y, Z directions: ", mean_mx, mean_my, mean_mz)
    # there's a divide by zero happening somewhere in here and i don't like it

    wfile.write("\nMetallicity: %f" % (mean_mx))
    wfile.close()

    # METHOD 2: Trying to reproduce Eric's results
    factor = oh.hydro_mol / oh.oxy_mol
    mcy_x2 = proj_x["o   "] / proj_x["h1  "] * factor
    mcy_x2 = mcy_x2[(~oh.np.isnan(mcy_x2))]
    mcy_x2 = oh.np.log10(mcy_x2) - log_sun
    mcy_x2 = oh.np.mean(mcy_x2)

    print("Method 2: Using Eric's method\n", mcy_x2)
