# -*- coding: utf-8 -*-

import numpy as np
import yt

#Load data from file
ds = yt.load("../Data/4.2.1.density_sap_hdf5_plt_cnt_0075")

test = ds.proj("density", 0)
p = test["density"]

ds.print_stats()
#print(ds.field_list)
print(ds.derived_field_list)
#print(ds.domain_width)


#Find column density along x axis
def cdX():
    pr = ds.proj("density", 0)
    print(pr["density"])
    print(type(pr))
    print(type(pr["density"]))
    print('----------------------')



#Get maximum density along x axis
def maxDZ():
    maxD = ds.proj("density", 0, method = "mip")
    print(maxD["density"])
    print('----------------------')


#Find density weighted temperature along y axis
def tdY():
    pr2 = ds.proj("temperature", "y", weight_field = "density")
    print(pr2["temperature"])
    print('----------------------')


#Find emission measure
def emission():
    em = ds.proj("density", 0, weight_field = "density")
    emd = em["density"]
    print(emd)
    print('----------------------')
    emission_measure = np.multiply(p,emd)
    print(emission_measure)
    print('----------------------')


#Make projection plots
def pPlot():
    plt1 = yt.ProjectionPlot(ds, 0, "density")
    plt1.save()
    plt2 = yt.ProjectionPlot(ds, 1, "temperature", weight_field = "density")
    plt2.save()

#Find column density off axis
def cdOA():
    L = [1,1,1] #Normal vector
    N = 1024 #Resolution
    W = 3e21
    c = [1.2,0.6,10.8]
    c = [0,0,0]
    #c = [1e5, 1e5,1e5]
    pr3 = yt.off_axis_projection(ds, c, L, W, N, "density")
    print(type(pr3))
    print(pr3)
    print(pr3.shape)
    yt.write_image(pr3, "%s_offaxis_projection2.png" % ds)


#Make projection plot off axis
def pPlotOA():
    L2 = [1,0,1]
    plt3 = yt.OffAxisProjectionPlot(ds, L2, "density", width = (10, 'kpc'))
    plt3.save("OffAxisPlot1.png")

#Compare OffAxisProjectionPlot to ProjectionPlot when normal vector is in
# y direction
def test():
    t1 = yt.ProjectionPlot(ds, 1, "density")
    t1.save()
    t2 = yt.OffAxisProjectionPlot(ds, [0,1,0], "density", width = (10, 'kpc'))
    t2.save()


def vol():
    sc = yt.create_scene(ds, lens_type='perspective')
    source = sc[0]
    source.tfh.set_bounds((3e-28, 5e-23))
    source.tfh.set_log(True)
    source.tfh.grey_opacity = False
    source.tfh.plot('transfer_function.png', profile_field='density')
    sc.save('rendering.png', sigma_clip=6.0)
