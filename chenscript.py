"""
06/05/2020

This is Chen's script! I'm cleaning it up so I can run it in my terminal

Calculates electron number density right now.

"""


import yt
# import math  # use this later
# import numpy as np  # use this later

ds = yt.load('../Data/4.2.1.density_sap_hdf5_plt_cnt_0075', unit_system="cgs")
# print(ds.field_list)
# print(ds.derived_field_list)

ad = ds.all_data()


def _nelec(field, ad):  # define the function
    eND = ad['H_nuclei_density'] + 2*ad['He_nuclei_density']
    return eND


# add electron number density as field
yt.add_field(
    ("gas", "electron_number_density"), function=_nelec, units="cm**(-3)",
    force_override=True
    )

# print(ds.derived_field_list)

# make projection plot
plot = yt.ProjectionPlot(ds, 0, "electron_number_density")
plot.save("../Plots/chenplot.png")
