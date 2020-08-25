# 05/15/20
import yt

file = "4.2.1.density_sap_hdf5_cnt_0075"
ds = yt.load(file)
rho = ds.r["density"]
# i think this creates a region.
ds.r[(100, 'kpc'):(200, 'kpc'),:,:]
