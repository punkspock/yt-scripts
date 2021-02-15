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
def nhiiCell1(data, ion, cell):
    """

    Calculate N(H II) associated with O VI in a single cell.

    Parameters:
        data (data object): All the cut data.
        ion (str): String name of the oxygen ion you want N(H II) assoc. w/
        cell (int): Number of cell you want the N(H II) for.

    """
    cell_depth = data['dx'][cell]  # cm

    # number density of ion
    nd_ion = data['{}_number'.format(ion)][cell]  # cm^-3
    # column density of oxygen ion
    noi = nd_ion * cell_depth  # cm^-2
    # metallicity in cell; dimensionless
    met = data['o_total_number'][cell] / data['h_total_number'][cell]
    # ionization fraction along sight line
    ion_frac = nd_ion / data['o_total_number'][cell]  # 

    nhii = noi / (met * ion_frac)

    return nhii


# method 1 of getting sight line mass
def cellMass1(cell, data, nhii):
    """

    Calculate the total mass along a sight line using the total N(H II) and
    knowledge of column densities of all oxygen ions.

    """
    cell_volume = data['cell_volume'][cell]
    cell_area = data['dy'][cell] * data['dz'][cell]  # yz-plane

    oxy_mass = data['o_total_number'][cell] * oh.mOxy * cell_volume
    # print('Calculated oxy_mass: {}'.format(oxy_mass))
    # N(H II) for just one cell should be all the H II in the cell.
    hydro_mass = nhii * cell_area * oh.mHydro
    # print('Calculated hydro_mass: {}'.format(hydro_mass))
    total_mass = oxy_mass + hydro_mass
    # print('Calculated total_mass: {}'.format(total_mass))

    return total_mass


# method 2 of getting N(H II)
def nhiiCell2(data, ion, cell):
    """

    Input data source; output is N(H II) for a single cell.

    """
    cell_depth = data['dx'][cell]

    # column density of oxygen ion in cell
    nd_ion = data['{}_number'.format(ion)][cell]
    cd_ion = nd_ion * cell_depth

    # mean metallicity/oxygen abundance for whole cloud
    o_abund = data['o_total_number'] / data['h_total_number']
    # get rid of ~1000 weird values
    o_abund = o_abund[(~oh.np.isnan(o_abund)) & (~oh.np.isinf(o_abund))]
    o_abund_mean = oh.np.mean(o_abund)  # take avg value

    # mean ionization fraction for whole cloud
    ion_frac =  nd_ion / data['o_total_number']
    # get rid of ~1000 weird values
    ion_frac = ion_frac[(~oh.np.isnan(ion_frac)) & (~oh.np.isinf(ion_frac))]
    ion_frac_mean = oh.np.mean(ion_frac) # take avg value

    # N(H II)_ion along a particular sight line
    nhii_cell = cd_ion / (ion_frac_mean * o_abund_mean)

    return nhii_cell


def nhiiCell3(data, ion, cell):
    """

    Input data source; output is N(H II) for a single cell.

    """
    cell_depth = data['dx'][cell]

    # column density of oxygen ion in cell
    nd_ion = data['{}_number'.format(ion)][cell]
    cd_ion = nd_ion * cell_depth

    # mean metallicity/oxygen abundance for whole cloud
    o_abund = data['o_total_number'] / data['h_total_number']
    # get rid of ~1000 weird values
    o_abund = o_abund[(~oh.np.isnan(o_abund)) & (~oh.np.isinf(o_abund))]
    o_abund_mean = oh.np.mean(o_abund)  # take avg value

    # mean ionization fraction for whole cloud
    ion_frac =  nd_ion / data['o_total_number']
    # get rid of ~1000 weird values
    ion_frac = ion_frac[(~oh.np.isnan(ion_frac)) & (~oh.np.isinf(ion_frac))]
    ion_frac_mean = oh.np.max(ion_frac) # take max value

    # N(H II)_ion along a particular sight line
    nhii_cell = cd_ion / (ion_frac_mean * o_abund_mean)

    return nhii_cell


# main program

if __name__ == "__main__":

    # get epoch from command line
    if len(sys.argv[1]) > 1:  # take command line argument
        epoch = sys.argv[1]
    else:
        epoch = 75  # default to 75 Myr

    # get all the regular stuff in there; load data, log file
    file, time, ds, ad, cut = oh.main(epoch)
    se.main()  # add all the scaled fields
    wfile = open("../../Plots/%s.txt" % (time), 'a')
    wfile.write("\n\n{}".format(datetime.today().ctime()))

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

    # do actual calculations
    for cell in cell_list:
        wfile.write('\n\nCell: {}'.format(cell))

        # magic
        cell_depth = cut['dx'][cell]
        magic_nh = cut['h_total_number'][cell] * cell_depth
        magic_mass = magicCell(cut, cell)
        magic_masses.append(magic_mass)
        wfile.write('\n\"Magic\" N(H): {}'.format(magic_nh))
        wfile.write('\n\"Magic\" cell mass: {}'.format(magic_mass))

        # method 1: the Eric Method
        ion = 'OVI'
        nh1 = nhiiCell1(cut, ion, cell)
        mass1 = cellMass1(cell, cut, nh1)
        method1_masses.append(mass1)
        wfile.write('\nMethod 1 N(H): {}'.format(nh1))
        wfile.write('\nMethod 1 cell mass: {}'.format(mass1))

        # method 2: 'us' method
        # can 'see' all ions
        ions = ['OI', 'OII', 'OIII', 'OIV', 'OV', 'OVI', 'OVII', 'OVIII', 'OIX']
        nh_list2 = []
        for ion in ions:
            nh2 = nhiiCell2(cut, ion, cell)
            nh_list2.append(nh2)
        nh2 = sum(nh_list2)
        mass2 = cellMass1(cell, cut, nh2)
        method2_masses.append(mass2)
        wfile.write('\nMethod 2 N(H): {}'.format(nh2))
        wfile.write('\nMethod 2 cell mass: {}'.format(mass2))

        # method 2.1: 'fox' method
        nh_list2_1 = []
        for ion in ions:
            nh2_1 = nhiiCell3(cut, ion, cell)
            nh_list2_1.append(nh2_1)
        nh2_1 = sum(nh_list2_1)
        mass2_1 = cellMass1(cell, cut, nh2_1)
        method2_1_masses.append(mass2_1)
        wfile.write('\nMethod 2.1 N(H): {}'.format(nh2_1))
        wfile.write('\nMethod 2.1 cell mass: {}'.format(mass2_1))

        # method 3: limited ion access
        ions = ['OII', 'OIV', 'OVI', 'OVIII']
        nh_list3 = []
        for ion in ions:
            nh3 = nhiiCell2(cut, ion, cell)
            nh_list3.append(nh3)
        nh3 = sum(nh_list3)
        mass3 = cellMass1(cell, cut, nh3)
        method3_masses.append(mass3)
        wfile.write('\nMethod 3 N(H): {}'.format(nh3))
        wfile.write('\nMethod 3 cell mass: {}'.format(mass3))




    # conclude
    wfile.close()
