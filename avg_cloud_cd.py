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


def nhMagic(data, avg_depth):  # don't use projected data, please.
    """

    The average number density of hydrogen from the domain multiplied by the
    average depth of the cloud to get an average column density of hydrogen
    over the whole cloud.

    """
    cell_volume = data['cell_volume']
    h_nd = oh.np.mean(data['h_total_number'])  # total number density

    avg_nh = h_nd * avg_depth

    return avg_nh


def nhCloud1(data, ion, scale_arg, avg_depth):
    """

    Input data source; output is average N(H) for whole cloud associated with
    a particular oxygen ion.

    Parameters:
        data (data obj): Probably cut or proj_x
        ion (str): Name of oxygen ion.
        scale_arg: Scale argument from command line.
        avg_depth: Average depth of the cloud, obtained using the 'sum' method
            in a projection.

    """

    # column density of oxygen ion in cell
    if scale_arg == 'unscaled':
        nd_ion = data['{}_number'.format(ion)]  # number density
        o_total = data['o_total_number']  # number density
    elif scale_arg == 'scaled':
        nd_ion = data['{}_scaled'.format(ion)]
        o_total = data['o_total_scaled']
    else:
        nd_ion = data['{}_number'.format(ion)]
        o_total = data['o_total_number']

    cell_volume = data['cell_volume']
    cloud_volume = sum(data['cell_volume'])
    h_nd = data['h_total_number']  # number density

    # average column density of that ion over the whole cloud
    avg_nd_ion = oh.np.mean(nd_ion)  # mean number density of that oxygen ion
    avg_cd_ion = avg_nd_ion * avg_depth  # avg number density * avg cloud depth

    # metallicity for whole cloud
    all_o = sum(o_total * cell_volume)  # total number of oxygen atoms
    all_h = sum(h_nd * cell_volume)  # total number hydrogen atoms
    met = all_o / all_h  # ratio of the two

    # ionization fraction for the whole cloud
    all_ion = sum(nd_ion * cell_volume)
    ion_frac = all_ion / all_o

    nh = avg_cd_ion / (met * ion_frac)

    return nh


def nhCloud4(data, ion, gs_frac, scale_arg):
    """

    Uses maximum ionization fraction from Gnat and Sternberg curves.

    """
    # column density of oxygen ion in cell
    if scale_arg == 'unscaled':
        nd_ion = data['{}_number'.format(ion)]  # number density
        o_total = data['o_total_number']  # number density
    elif scale_arg == 'scaled':
        nd_ion = data['{}_scaled'.format(ion)]
        o_total = data['o_total_scaled']
    else:
        nd_ion = data['{}_number'.format(ion)]
        o_total = data['o_total_number']

    cell_volume = data['cell_volume']
    cloud_volume = sum(data['cell_volume'])
    h_nd = data['h_total_number']  # number density

    # average column density of that ion over the whole cloud
    avg_nd_ion = oh.np.mean(nd_ion)  # mean number density of that oxygen ion
    avg_cd_ion = avg_nd_ion * avg_depth  # avg number density * avg cloud depth

    # metallicity for whole cloud
    all_o = sum(o_total * cell_volume)  # total number of oxygen atoms
    all_h = sum(h_nd * cell_volume)  # total number hydrogen atoms
    met = all_o / all_h  # ratio of the two

    # ionization fraction is gs_fracs

    nh = avg_cd_ion / (met * gs_frac)

    return nh


def method1(data, scale_arg, avg_depth):
    ions = ['OVI']
    nh_list = []
    for ion in ions:
        nh_ion = nhCloud1(data, ion, scale_arg, avg_depth)
        nh_list.append(nh_ion)
    nh = sum(nh_list)

    return nh


def method4(data, scale_arg):
    # method 4: Gnat & Sternberg
    ions = ['OI', 'OII', 'OIII', 'OIV', 'OV', 'OVI', 'OVII', 'OVIII', 'OIX']
    gs_fracs = [  # direct from G&S
        2.6e-1, 9.61e-1, 7.95e-1, 7.27e-1, 5.06e-1, 1.96e-1, 9.94e-1,
        4.51e-1, 9.04e-1
        ]
    wfile.write('\n\n\tMethod 4:')
    nh_list4 = []
    for ion, frac in zip(ions, gs_fracs):
        nh4 = nhCloud4(data, ion, frac, scale_arg)
        wfile.write('\n\t\t{}, {}'.format(ion, nh4))
        nh_list4.append(nh4)
    nh4 = sum(nh_list4)
    wfile.write('\n\tMethod 4 N(H): {}'.format(nh4))

    return nh4


if __name__ == "__main__":
    # get epoch from command line
    if len(sys.argv[1]) > 1:  # take command line argument
        epoch = sys.argv[1]
    else:
        epoch = 75  # default to 75 Myr

    if len(sys.argv[2]) > 1:
        method = sys.argv[2]
    else:
        method == 'all'

    # find out whether to scale
    if len(sys.argv[3]) > 1:  # command line argument for scaling
        scale_arg = sys.argv[3]
    else:
        scale_arg = 'unscaled'

    # get all the regular stuff in there; load data, log file
    file, time, ds, ad, cut = oh.main(epoch)
    se.main()  # add all the scaled fields
    wfile = open("../../Plots/%s.txt" % (time), 'a')
    wfile.write("\n\n{}".format(datetime.today().ctime()))
    wfile.write("\n{}".format(scale_arg))

    # get the average depth of the cloud; project using sum method
    proj_x2 = ds.proj('OI_number', 'x', method='sum', data_source=cut)
    depth = proj_x2['dx']
    depth = depth[depth != 0]  # exclude zeroes; very important
    avg_depth = oh.np.mean(depth)

    if method == 'magic':
        wfile.write('\nWhole cloud:')
        magic_nh = nhMagic(cut, avg_depth)
        wfile.write('\n\t\"Magic\" average N(H): {}'.format(magic_nh))
    elif method == 'method1':
        wfile.write('\nWhole cloud:')
        nh1 = method1(cut, scale_arg, avg_depth)
        wfile.write('\n\tMethod 1 N(H): {}'.format(nh1))
    elif method == 'method4':
        wfile.write('\nWhole cloud:')
        nh4 = method4(cut, scale_arg)
        wfile.write('\n\tMethod 4 N(H): {}'.format(nh4))
    elif method == 'all':
        wfile.write('\nWhole cloud:')
        magic_nh = nhMagic(cut, avg_depth)
        nh1 = method1(cut, scale_arg, avg_depth)
        nh4 = method4(cut, scale_arg)
        wfile.write('\n\t\"Magic\" average N(H): {}'.format(magic_nh))
        wfile.write('\n\tMethod 1 N(H): {}'.format(nh1))
        wfile.write('\n\tMethod 4 N(H): {}'.format(nh4))
    else:
        print('Invalid method.')

# conclude
wfile.close()
