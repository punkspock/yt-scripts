"""
Sydney Whilden
02/16/2021

Average column density of hydrogen throughout whole cloud.

"""

import OH_fields as oh
import scaleeverything as se
import sys
import random
import matplotlib.pyplot as plt
from datetime import datetime
oh.yt.funcs.mylog.setLevel(50)


def nhMagic(data, ion):
    """

    Average N(H) across whole cloud.

    """

    if scale_arg == 'unscaled':
        nd_ion = data['{}_number'.format(ion)]
        o_total = data['o_total_number']
    elif scale_arg == 'scaled':
        nd_ion = data['{}_scaled'.format(ion)]
        o_total = data['o_total_scaled']
    else:
        nd_ion = data['{}_number'.format(ion)]
        o_total = data['o_total_number']

    # oxygen atoms of a particular ion * average depth of cloud / cloud volume
    # 1. Total number of that oxygen ion in cloud.
    cell_number = nd_ion * data['cell_volume']  # total number in each cell
    cloud_number = sum(cell_number)  # total # of that ion in the cloud

    # 2. Average depth in number of cells
    proj_x2 = ds.proj('OI_number', 'x', method='sum', data_source=data)
    avg_depth = oh.np.mean(proj_x2['dx'])

    

    return


def nhMean(data, ion, scale_arg):
    """

    Input data source; output is average N(H) for whole cloud.

    Parameters:
        data (data obj): Probably cut or proj_x
        ion (str): Name of oxygen ion.
        cell (int): Number of cell to calculate for.
        scale_arg: Scale argument from command line.

    """

    # column density of oxygen ion in cell
    if scale_arg == 'unscaled':
        nd_cloud = data['{}_number'.format(ion)]
        o_total = data['o_total_number']
    elif scale_arg == 'scaled':
        nd_cloud = data['{}_scaled'.format(ion)]
        o_total = data['o_total_scaled']
    else:
        nd_cloud = data['{}_number'.format(ion)]
        o_total = data['o_total_number']

    # average column density of ion for whole cloud
    depth = cut['dx']
    cd_ion = nd_ion * depth # can be scaled or unscaled
    cd_ion_mean = oh.np.mean(cd_ion)
    # ^ this is an array

    cd_mean = oh.np.mean(cd_cloud)
    # print('cd_cell: {}'.format(cd_cell))

    # mean metallicity/oxygen abundance for whole cloud
    met = o_total / data['h_total_number']
    # get rid of ~1000 weird values
    met = met[(~oh.np.isnan(met)) & (~oh.np.isinf(met))]
    met_mean = oh.np.mean(met)  # take avg value
    # print('met_mean: {}'.format(met_mean))

    # mean ionization fraction for whole cloud
    ion_frac =  nd_cloud / o_total
    # get rid of ~1000 weird values
    ion_frac = ion_frac[(~oh.np.isnan(ion_frac)) & (~oh.np.isinf(ion_frac))]
    ion_frac_mean = oh.np.mean(ion_frac) # take avg value
    # print('ion_frac_mean: {}'.format(ion_frac_mean))

    # N(H II)_ion
    nhii_cell = cd_mean / (ion_frac_mean * met_mean)
    # print('nhii_cell: {}'.format(nhii_cell))

    return nhii


if __name__ == "__main__":
    # get epoch from command line
    if len(sys.argv[1]) > 1:  # take command line argument
        epoch = sys.argv[1]
    else:
        epoch = 75  # default to 75 Myr

    # find out whether to scale
    if len(sys.argv[2]) > 1:  # command line argument for scaling
        scale_arg = sys.argv[2]
    else:
        scale_arg = 'unscaled'

    # get all the regular stuff in there; load data, log file
    file, time, ds, ad, cut = oh.main(epoch)
    se.main()  # add all the scaled fields
    wfile = open("../../Plots/%s.txt" % (time), 'a')
    wfile.write("\n\n{}".format(datetime.today().ctime()))
    wfile.write("\n{}".format(scale_arg))

    # FROM DOMAIN ("magic" method)
    mean_h = oh.np.mean(cut['h_total_number'])  # average number density
    mean_dx = oh.np.mean(cut['dx'])  # average cell depth
    cloud_vol = sum(cut['cell_volume'])  # total cloud volume
    magic_nh = mean_h * mean_dx / cloud_vol
    wfile.write('Average N(H) from domain: {}'.format(magic_nh))

    # METHOD 1
    ions = ['OI', 'OII', 'OIII', 'OIV', 'OV', 'OVI', 'OVII', 'OVIII', 'OIX']
    for ion in ions:
        nh = nhMean(cut, ion, scale_arg)
