"""
05/08/2020
Load a file and access information about specific data points.

"""

import yt  # see theytproject.com's Cookbook section for instructions
import numpy as np  # need this for np.where() command

file = "../4.2.1.density_sap_hdf5_plt_cnt_0075"  # specify data file
ds = yt.load(file)  # load in your file

g = ds.index.grids[1043]  # no idea what the 1043 is for.

density = g["density"]  # array of density for every point in the dataset

from yt.units import kpc  # need kpc for units

# choose a point in the dataset by specifying its location; make it an object
# point_obj = ds.point([0.5, 0.5, 0.5]*kpc) # point_obj is a YTArray

# what if you want points in the density data that satisfy a condition?
value = 1.77801737e-27  # dummy value
meets = np.where(density <= value)   # meets is an array

print(meets)  # show the array of values that met the condition

"""
This is all using dummy data just to show the process!

"""
