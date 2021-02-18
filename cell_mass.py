"""
Sydney Whilden
02/10/2021

Find mass in a cell using different methods.

"""

# import statements
import OH_fields as oh
import scaleeverything as se
import sys
import random
import matplotlib.pyplot as plt
from datetime import datetime
oh.yt.funcs.mylog.setLevel(50)


# functions
def cellList(cells_wanted, total_cells):
    """

    Generate a desired number of random cells.

    Parameters:
        cells_wanted (int): Desired number of random cells, not to exceed total
            number of cells.
        total_cells (int): Number of cells, total.

    """
    cell_list = []

    for i in range(0, cells_wanted):
        n = random.randint(0, total_cells)
        cell_list.append(n)

    return cell_list


# "magic" method
def magicCell(data, cell):
    """

    Returns total combined mass of hydrogen and oxygen in a cell using
    the "magician's" knowledge of the content of the simulation. Only accounts
    for mass of hydrogen and oxygen.

    """
    # mass along sight line
    cell_volume = data['cell_volume'][cell]

    h_mass = data['h_total_number'][cell] * oh.mHydro * cell_volume
    # print('Magic h_mass: {}'.format(h_mass))  # test
    # mass along sight line
    o_mass = data['o_total_number'][cell] * oh.mOxy * cell_volume
    # print('Magic o_mass: {}'.format(o_mass))  # test
    # total mass
    total_mass = h_mass + o_mass
    # print('Magic total_mass: {}'.format(total_mass))

    return total_mass


# method  1 of calculating N(H II) for a single cell
def nhiiCell1(data, ion, cell, scale_arg):
    """

    Calculate N(H II) associated with O VI in a single cell.

    Parameters:
        data (data object): All the cut data.
        ion (str): String name of the oxygen ion you want N(H II) assoc. w/
        cell (int): Number of cell you want the N(H II) for.
        scale_arg : Whether the ion is to be scaled or unscaled. Passed in
            via command line.

    """
    cell_depth = data['dx'][cell]  # cm

    # number density of ion
    if scale_arg == 'unscaled':
        nd_ion = data['{}_number'.format(ion)][cell]  # cm^-3
        o_total = data['o_total_number']
    elif scale_arg == 'scaled':
        nd_ion = data['{}_scaled'.format(ion)][cell]
        o_total = data['o_total_scaled']
    else:
        # default to unscaled
        nd_ion = data['{}_number'.format(ion)][cell]
        o_total = data['o_total_number']

    # column density of oxygen ion
    noi = nd_ion * cell_depth  # cm^-2
    # metallicity in cell; dimensionless
    met = o_total[cell] / data['h_total_number'][cell]
    # ionization fraction along sight line
    ion_frac = nd_ion / o_total[cell]  #

    nhii = noi / (met * ion_frac)

    return nhii


# method 1 of getting sight line mass
def cellMass1(cell, data, nhii, scale_arg):
    """

    Calculate the total mass along a sight line using the total N(H II) and
    knowledge of column densities of all oxygen ions.

    """
    if scale_arg == 'unscaled':
        o_total = data['o_total_number']
    elif scale_arg == 'scaled':
        o_total = data['o_total_scaled']
    else:
        o_total = data['o_total_number']

    cell_volume = data['cell_volume'][cell]
    cell_area = data['dy'][cell] * data['dz'][cell]  # yz-plane

    oxy_mass = o_total[cell] * oh.mOxy * cell_volume
    # print('Calculated oxy_mass: {}'.format(oxy_mass))
    # N(H II) for just one cell should be all the H II in the cell.
    hydro_mass = nhii * cell_area * oh.mHydro
    # print('Calculated hydro_mass: {}'.format(hydro_mass))
    total_mass = oxy_mass + hydro_mass
    # print('Calculated total_mass: {}'.format(total_mass))

    return total_mass


# method 2 of getting N(H II)
def nhiiCell2(data, ion, cell, scale_arg):
    """

    Input data source; output is N(H II) for a single cell.

    Parameters:
        data (data obj): Probably cut or proj_x
        ion (str): Name of oxygen ion.
        cell (int): Number of cell to calculate for.
        scale_arg: Scale argument from command line.

    """
    cell_depth = data['dx'][cell]

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

    nd_cell = nd_cloud[cell]
    cd_cell = nd_cell * cell_depth  # can be scaled or unscaled
    # print('cd_cell: {}'.format(cd_cell))

    # mean metallicity/oxygen abundance for whole cloud
    all_o = sum(o_total * data['cell_volume'])
    all_h = sum(data['h_total_number'] * data['cell_volume'])

    met = all_o / all_h

    # get rid of ~1000 weird values
    # met = met[(~oh.np.isnan(met)) & (~oh.np.isinf(met))]
    # met_mean = oh.np.mean(met)  # take avg value
    # print('met_mean: {}'.format(met_mean))

    # mean ionization fraction for whole cloud
    all_ion = sum(nd_cloud * data['cell_volume'])
    ion_frac =  all_ion / all_o
    # get rid of ~1000 weird values
    # ion_frac = ion_frac[(~oh.np.isnan(ion_frac)) & (~oh.np.isinf(ion_frac))]
    # ion_frac_mean = oh.np.mean(ion_frac) # take avg value
    # print('ion_frac_mean: {}'.format(ion_frac_mean))

    # N(H II)_ion
    nhii_cell = cd_cell / (ion_frac * met)
    # print('nhii_cell: {}'.format(nhii_cell))

    return nhii_cell


def nhiiCell3(data, ion, cell, scale_arg):
    """
    *** UNWEIGHTED AVERAGE METALLICITY ***

    Input data source; output is N(H II) for a single cell.

    Parameters:
        data (data obj): Probably cut or proj_x
        ion (str): Tells which ion to calculate for. No spaces in ion names.
        cell (int): Number of cell to calculate for.
        scale_arg: Whether or not to scale. Passed in from command line.

    """
    cell_depth = data['dx'][cell]

    # column density of oxygen ion in cell
    if scale_arg == 'unscaled':
        nd_ion = data['{}_number'.format(ion)][cell]
        o_total = data['o_total_number']
    elif scale_arg == 'scaled':
        # to scale, multiply all instances of oxygen by scale factor
        nd_ion = data['{}_scaled'.format(ion)][cell]
        o_total = data['o_total_scaled']
    else:
        nd_ion = data['{}_number'.format(ion)][cell]
        o_total = data['o_total_number']

    cd_ion = nd_ion * cell_depth  # can be scaled or unscaled

    # mean metallicity/oxygen abundance for whole cloud
    o_abund = o_total / data['h_total_number']
    # get rid of ~1000 weird values
    o_abund = o_abund[(~oh.np.isnan(o_abund)) & (~oh.np.isinf(o_abund))]
    o_abund_mean = oh.np.mean(o_abund)  # take avg value

    # mean ionization fraction for whole cloud
    ion_frac =  nd_ion / o_total
    # get rid of ~1000 weird values
    ion_frac = ion_frac[(~oh.np.isnan(ion_frac)) & (~oh.np.isinf(ion_frac))]
    ion_frac_mean = oh.np.max(ion_frac) # take max value

    # N(H II)_ion along a particular sight line
    nhii_cell = cd_ion / (ion_frac_mean * o_abund_mean)

    return nhii_cell


def nhiiCell4(data, ion, cell, gs_frac, scale_arg):
    """

    Uses maximum ionization fraction from Gnat & Sternberg curves. Uses
    metallicity from a single cell.

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

    cd_ion = nd_ion * cut['dx']
    cd_cell = cd_ion[cell]

    # metallicity from cell
    met = o_total[cell] / data['h_total_number'][cell]

    nhii = cd_cell / (gs_frac * met)

    return nhii


def magicMethod(data, cell, wfile):
    wfile.write('\n\nCell: {}'.format(cell))
    # magic
    cell_depth = data['dx'][cell]
    magic_nh = data['h_total_number'][cell] * cell_depth
    magic_mass = magicCell(data, cell)
    wfile.write('\n\t\"Magic\" N(H): {}'.format(magic_nh))
    wfile.write('\n\t\"Magic\" cell mass: {}'.format(magic_mass))

    return magic_nh, magic_mass


def method1(data, cell, scale_arg, wfile):
    wfile.write('\n\nCell: {}'.format(cell))
    # method 1: the Eric Method
    ion = 'OVI'
    nh1 = nhiiCell1(data, ion, cell, scale_arg)
    mass1 = cellMass1(cell, data, nh1, scale_arg)
    wfile.write('\n\tMethod 1 N(H): {}'.format(nh1))
    wfile.write('\n\tMethod 1 cell mass: {}'.format(mass1))

    return nh1, mass1


def method2(data, cell, scale_arg, wfile):
    wfile.write('\n\nCell: {}'.format(cell))
    # method 2: 'us' method
    # can 'see' all ions
    ions = ['OI', 'OII', 'OIII', 'OIV', 'OV', 'OVI', 'OVII', 'OVIII', 'OIX']
    nh_list2 = []
    wfile.write('\n\n\tMethod 2: ')
    for ion in ions:
        nh2 = nhiiCell2(data, ion, cell, scale_arg)
        wfile.write('\n\t\t{}, {}'.format(ion, nh2))  # temporary
        nh_list2.append(nh2)
    nh2 = sum(nh_list2)
    mass2 = cellMass1(cell, data, nh2, scale_arg)
    wfile.write('\n\tMethod 2 N(H): {}'.format(nh2))
    wfile.write('\n\tMethod 2 cell mass: {}'.format(mass2))

    return nh2, mass2


def method2_1(data, cell, scale_arg, wfile):
    wfile.write('\n\nCell: {}'.format(cell))
    # method 2.1: 'fox' method
    nh_list2_1 = []
    wfile.write('\n\n\tMethod 2.1: ')
    for ion in ions:
        nh2_1 = nhiiCell3(cut, ion, cell, scale_arg)
        wfile.write('\n\t\t{}, {}'.format(ion, nh2_1))
        nh_list2_1.append(nh2_1)
    nh2_1 = sum(nh_list2_1)
    mass2_1 = cellMass1(cell, cut, nh2_1, scale_arg)
    wfile.write('\n\tMethod 2.1 N(H): {}'.format(nh2_1))
    wfile.write('\n\tMethod 2.1 cell mass: {}'.format(mass2_1))

    return nh2_1, mass2_1


def method3(data, cell, scale_arg, wfile):
    wfile.write('\n\nCell: {}'.format(cell))
    # method 3: limited ion access
    ions = ['OII', 'OIV', 'OVI', 'OVIII']
    nh_list3 = []
    for ion in ions:
        nh3 = nhiiCell2(data, ion, cell, scale_arg)
        nh_list3.append(nh3)
    nh3 = sum(nh_list3)
    mass3 = cellMass1(cell, data, nh3, scale_arg)
    wfile.write('\n\tMethod 3 N(H): {}'.format(nh3))
    wfile.write('\n\tMethod 3 cell mass: {}'.format(mass3))

    return nh3, mass3


def method4(data, cell, scale_arg, wfile):
    wfile.write('\n\nCell: {}'.format(cell))
    # method 4: Gnat and Sternberg
    ions = ['OI', 'OII', 'OIII', 'OIV', 'OV', 'OVI', 'OVII', 'OVIII', 'OIX']
    gs_fracs = [  # direct from G&S
        2.6e-1, 9.61e-1, 7.95e-1, 7.27e-1, 5.06e-1, 1.96e-1, 9.94e-1,
        4.51e-1, 9.04e-1
        ]
    wfile.write('\n\n\tMethod 4:')
    nh_list4 = []
    for ion, frac in zip(ions, gs_fracs):
        nh4 = nhiiCell4(data, ion, cell, frac, scale_arg)
        wfile.write('\n\t\t{}, {}'.format(ion, nh4))
        nh_list4.append(nh4)
    nh4 = sum(nh_list4)
    mass4 = cellMass1(cell, data, nh4, scale_arg)
    wfile.write('\n\tMethod 4 N(H): {}'.format(nh4))
    wfile.write('\n\tMethod 4 mass: {}'.format(mass4))

    return nh4, mass4


# main program

if __name__ == "__main__":

    # get epoch from command line
    if len(sys.argv[1]) > 1:  # take command line argument
        epoch = sys.argv[1]
    else:
        epoch = 75  # default to 75 Myr

    if len(sys.argv[2]) > 1:
        method = sys.argv[2]
    else:
        method = 'all'

    # find out whether to scale
    if len(sys.argv[3]) > 1:  # command line argument for scaling
        scale_arg = sys.argv[2]
    else:
        scale_arg = 'unscaled'

    # get all the regular stuff in there; load data, log file
    file, time, ds, ad, cut = oh.main(epoch)
    se.main()  # add all the scaled fields
    wfile = open("../../Plots/%s.txt" % (time), 'a')
    wfile.write("\n\n{}".format(datetime.today().ctime()))
    wfile.write("\n{}".format(scale_arg))

    # generate 5 random cells
    # cell_list = cellList(5, len(cut['density']))
    cell_list = [273, 123922, 336714]

    # initialize arrays
    magic_masses = []
    method1_masses = []
    method2_masses = []
    method2_1_masses = []
    method3_masses = []
    method4_masses = []

    if method == 'magic':
        for cell in cell_list:
            magic_nh, magic_mass = magicMethod(cut, cell, wfile)
    elif method == 'method1':
        for cell in cell_list:
            nh1, mass1 = method1(cut, cell, scale_arg, wfile)
    elif method == 'method2':
        for cell in cell_list:
            nh2, mass2 = method2(cut, cell, scale_arg, wfile)
    elif method == 'method2.1':
        for cell in cell_list:
            nh2_1, mass2_1 = method2_1(cut, cell, scale_arg, wfile)
    elif method == 'method3':
        for cell in cell_list:
            nh3, mass3 = method3(cut, cell, scale_arg, wfile)
    elif method == 'method4':
        for cell in cell_list:
            nh4, mass4 = method4(cut, cell, scale_arg, wfile)
    elif method == 'all':
        for cell in cell_list:
            magic_nh, magic_mass = magicMethod(cut, cell, wfile)
            nh1, mass1 = method1(cut, cell, scale_arg, wfile)
            nh2, mass2 = method2(cut, cell, scale_arg, wfile)
            nh2_1, mass2_1 = method2_1(cut, cell, scale_arg, wfile)
            nh3, mass3 = method3(cut, cell, scale_arg, wfile)
            nh4, mass4 = method4(cut, cell, scale_arg, wfile)
    else:
        for cell in cell_list:
            magic_nh, magic_mass = magicMethod(cut, cell, wfile)
            nh1, mass1 = method1(cut, cell, scale_arg, wfile)
            nh2, mass2 = method2(cut, cell, scale_arg, wfile)
            nh2_1, mass2_1 = method2_1(cut, cell, scale_arg, wfile)
            nh3, mass3 = method3(cut, cell, scale_arg, wfile)
            nh4, mass4 = method4(cut, cell, scale_arg, wfile)


    # conclude
    wfile.close()
