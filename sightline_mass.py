"""
Sydney Whilden
02/04/2021

Calculating the mass along a sight line using several different methodologies.
Aims to combine scripts cloud_mass.py, cloud_mass2.py, and cloud_mass3.py.

Purpose is to compare the methodologies, so do them all at once.

"""

# import statements
import OH_fields as oh
import scaleeverything as se
import sys
import random
import matplotlib.pyplot as plt
from datetime import datetime
oh.yt.funcs.mylog.setLevel(50)


# make a desired number of sight lines
def sightlineList(line_number, column_number):
    """

    Generate a desired number of random sight lines.

    Parameters:
        line_number (int): Desired number of sight lines, not to exceed number
            of projection columns.
        column_number (int): Number of projection columns.

    """
    sightlist = []

    for i in range(0, line_number):
        n = random.randint(0, column_number)
        sightlist.append(n)

    return sightlist


# "magic" method
def magicSightline(proj_x, sightline, mean_cell_area):
    """

    Returns total combined mass of hydrogen and oxygen along a sightline using
    the "magician's" knowledge of the content of the simulation. Only accounts
    for mass of hydrogen and oxygen.

    """
    # mass along sight line
    # exclude zeroes!
    h_cd = proj_x['h_total_number']
    h_cd = h_cd[h_cd != 0]
    h_mass = h_cd[sightline] * oh.mHydro * mean_cell_area
    # print('Magic h_mass: {}'.format(h_mass))  # test
    # mass along sight line
    o_cd = proj_x['o_total_number']
    o_cd = o_cd[o_cd != 0]  # exclude zeroes
    o_mass = o_cd[sightline] * oh.mOxy * mean_cell_area
    # print('Magic o_mass: {}'.format(o_mass))  # test
    # total mass
    total_mass = h_mass + o_mass
    # print('Magic total_mass: {}'.format(total_mass))

    return total_mass


# method 1 of getting N(H II)
def nhiiSightline1(proj_x, ion, sightline, scale_arg):
    """

    Calculate N(H II) associated with O VI along a sight line.

    Parameters:
        proj_x (data object): All the projection data.
        ion (str): String name of the oxygen ion you want N(H II) assoc. w/
        sightline (int): Number of projection column/sight line you want the
            N(H II) for.

    """
    if scale_arg == 'unscaled':
        cd_ion = proj_x['{}_number'.format(ion)]
        o_total = proj_x['o_total_number']
    elif scale_arg == 'scaled':
        cd_ion = proj_x['{}_scaled'.format(ion)]
        o_total = proj_x['o_total_scaled']
    else:
        cd_ion = proj_x['{}_number'.format(ion)]
        o_total = proj_x['o_total_number']

    # exclude zeroes
    cd_ion = cd_ion[cd_ion != 0]
    o_total = o_total[o_total != 0]
    h_cd = proj_x['h_total_number']
    h_cd = h_cd[h_cd != 0]

    # column density of oxygen ion
    cd_line = cd_ion[sightline]
    # metallicity along sight line

    met = o_total[sightline] / h_cd[sightline]
    # ionization fraction along sight line
    ion_frac = cd_line / o_total[sightline]

    nhii_line = cd_line / (met * ion_frac)

    return nhii_line


# method 1 of getting sight line mass
def sightlineMass1(sightline, proj_x, nhii, mean_cell_area, scale_arg):
    """

    Calculate the total mass along a sight line using the total N(H II) and
    knowledge of column densities of all oxygen ions.

    """
    if scale_arg == 'unscaled':
        o_total = proj_x['o_total_number']
    elif scale_arg == 'scaled':
        o_total = proj_x['o_total_scaled']
    else:
        o_total = proj_x['o_total_number']

    o_total = o_total[o_total != 0]  # exclude zeroes

    oxy_mass = o_total[sightline] * oh.mOxy * mean_cell_area
    print('Calculated oxy_mass: {}'.format(oxy_mass))
    hydro_mass = nhii * oh.mHydro * mean_cell_area
    print('Calculated hydro_mass: {}'.format(hydro_mass))
    total_mass = oxy_mass + hydro_mass
    print('Calculated total_mass: {}'.format(total_mass))

    return total_mass


# method 2 of getting N(H II)
def nhiiSightline2(proj_x, ion, sightline, scale_arg, mean_cell_area):
    """

    Input projection data; output is N(H II) for a single sight line.
    A sight line is a cell of the projected data.

    """

    if scale_arg == 'unscaled':
        cd_ion = proj_x['{}_number'.format(ion)]
        o_total = proj_x['o_total_number']
    elif scale_arg == 'scaled':
        cd_ion = proj_x['{}_scaled'.format(ion)]
        o_total = proj_x['o_total_scaled']
    else:
        cd_ion = proj_x['{}_number'.format(ion)]
        o_total = proj_x['o_total_number']  # projection column

    # exclude zeroes
    cd_ion = cd_ion[cd_ion != 0]
    o_total = o_total[o_total != 0]  # this is a column density
    h_cd = proj_x['h_total_number']
    h_cd = h_cd[h_cd != 0]

    cd_line = cd_ion[sightline]  # column density for just this sight line

    all_o = sum(o_total * mean_cell_area)
    all_h = sum(h_cd * mean_cell_area)
    # mean metallicity/oxygen abundance for whole cloud
    met = all_o / all_h
    # get rid of ~1000 weird values
    met = met[(~oh.np.isnan(met)) & (~oh.np.isinf(met))]
    met_mean = oh.np.mean(met)  # take avg value

    # mean ionization fraction for whole cloud
    all_ion = sum(cd_ion * mean_cell_area)
    ion_frac = all_ion / all_o
    # get rid of ~1000 weird values
    ion_frac = ion_frac[(~oh.np.isnan(ion_frac)) & (~oh.np.isinf(ion_frac))]
    ion_frac_mean = oh.np.mean(ion_frac) # take avg value

    # N(H II)_ion along a particular sight line
    nhii_line = cd_line / (ion_frac_mean * met_mean)

    return nhii_line


# method 2 of getting N(H II)
def nhiiSightline3(proj_x, ion, sightline, scale_arg, mean_cell_area):
    """

    Input projection data; output is N(H II) for a single sight line.
    A sight line is a cell of the projected data.

    """

    if scale_arg == 'unscaled':
        cd_ion = proj_x['{}_number'.format(ion)]
        o_total = proj_x['o_total_number']
    elif scale_arg == 'scaled':
        cd_ion = proj_x['{}_scaled'.format(ion)]
        o_total = proj_x['o_total_scaled']
    else:
        cd_ion = proj_x['{}_number'.format(ion)]
        o_total = proj_x['o_total_number']

    cd_ion = cd_ion[cd_ion != 0]
    o_total = o_total[o_total != 0]
    h_cd = proj_x['h_total_number']
    h_cd = h_cd[h_cd != 0]

    cd_line = cd_ion[sightline]  # column density for just this sight line

    all_o = sum(o_total * mean_cell_area)
    all_h = sum(h_cd * mean_cell_area)

    # mean metallicity/oxygen abundance for whole cloud
    met = all_o / all_h
    # get rid of ~1000 weird values
    met = met[(~oh.np.isnan(met)) & (~oh.np.isinf(met))]
    met_mean = oh.np.mean(met)  # take avg value

    all_ion = sum(cd_ion * mean_cell_area)
    # mean ionization fraction for whole cloud
    ion_frac = all_ion / all_o
    # get rid of ~1000 weird values
    ion_frac = ion_frac[(~oh.np.isnan(ion_frac)) & (~oh.np.isinf(ion_frac))]
    ion_frac_mean = oh.np.max(ion_frac) # take max value

    # N(H II)_ion along a particular sight line
    nhii_line = cd_line / (ion_frac_mean * met_mean)

    return nhii_line


def nhiiSightline4(proj_x, ion, sightline, gs_frac, scale_arg):
    """

    Uses maximum ionization fraction from Gnat & Sternberg curves.

    """
    if scale_arg == 'unscaled':
        cd_ion = proj_x['{}_number'.format(ion)]
        o_total = proj_x['o_total_number']
    elif scale_arg == 'scaled':
        cd_ion = proj_x['{}_scaled'.format(ion)]
        o_total = proj_x['o_total_scaled']
    else:
        cd_ion = proj_x['{}_number'.format(ion)]
        o_total = proj_x['o_total_number']

    cd_ion = cd_ion[cd_ion != 0]
    o_total = o_total[o_total != 0]
    h_cd = proj_x['h_total_number']
    h_cd = h_cd[h_cd != 0]

    cd_line = cd_ion[sightline]

    # metallicity from column
    met = o_total[sightline] / h_cd[sightline]

    nhii = cd_line / (gs_frac * met)

    return nhii


def magicMethod(data, sightline, mean_cell_area, wfile):
    wfile.write('\n\nSightline: {}'.format(sightline))
    magic_mass = magicSightline(data, sightline, mean_cell_area)
    h_cd = data['h_total_number']
    h_cd = h_cd[h_cd != 0]
    magic_nh = h_cd[sightline]
    wfile.write('\n\t\"Magic\" N(H): {}'.format(magic_nh))
    wfile.write('\n\t\"Magic\" mass: {}'.format(magic_mass))

    return magic_nh, magic_mass


def method1(data, sightline, scale_arg, mean_cell_area, wfile):
    wfile.write('\n\nSightline: {}'.format(sightline))
    # method 1
    ion = 'OVI'  # only use one ion
    nh1 = nhiiSightline1(data, ion, sightline, scale_arg)
    wfile.write('\n\tMethod 1 N(H): {}'.format(nh1))
    mass1 = sightlineMass1(sightline, data, nh1, mean_cell_area, scale_arg)
    wfile.write('\n\tMethod 1 mass: {}'.format(mass1))

    return nh1, mass1


def method2(data, sightline, scale_arg, mean_cell_area, wfile):
    wfile.write('\n\nSightline: {}'.format(sightline))
    # method 2: "us" method
    ions = ['OI', 'OII', 'OIII', 'OIV', 'OV', 'OVI', 'OVII', 'OVIII', 'OIX']
    nhii_list2 = []
    wfile.write('\n\n\tMethod 2 (values from cloud): ')
    for ion in ions:
        nhii2 = nhiiSightline2(data, ion, sightline, scale_arg, mean_cell_area)
        wfile.write('\n\t\t{}, {}'.format(ion, nhii2))
        nhii_list2.append(nhii2)
    # print('nhii_list2: {}'.format(nhii_list2))  # test
    nhii2 = sum(nhii_list2)
    wfile.write('\n\tMethod 2 N(H): {}'.format(nhii2))  # test
    mass2 = sightlineMass1(sightline, data, nhii2, mean_cell_area, scale_arg)
    wfile.write('\n\tMethod 2 mass: {}'.format(mass2))

    return nhii2, mass2


def method2_1(data, sightline, scale_arg, mean_cell_area, wfile):
    wfile.write('\n\nSightline: {}'.format(sightline))
    # method 2.1: 'fox' method
    nh_list2_1 = []
    for ion in ions:
        nh2_1 = nhiiSightline3(data, ion, sightline, scale_arg, mean_cell_area)
        nh_list2_1.append(nh2_1)
    nh2_1 = sum(nh_list2_1)
    mass2_1 = sightlineMass1(sightline, data, nh2_1, mean_cell_area, scale_arg)
    wfile.write('\n\tMethod 2.1 N(H): {}'.format(nh2_1))
    wfile.write('\n\tMethod 2.1 mass: {}'.format(mass2_1))

    return nh2_1, mass2_1


def method3(data, sightline, scale_arg, mean_cell_area, wfile):
    wfile.write('\n\nSightline: {}'.format(sightline))
    # method 3
    ions = ['OII', 'OIV', 'OVI', 'OVIII']
    nhii_list3 = []
    for ion in ions:
        nhii3 = nhiiSightline2(data, ion, sightline, scale_arg, mean_cell_area)
        nhii_list3.append(nhii3)
    # print('nhii_list3: {}'.format(nhii_list3))  # test
    nhii3 = sum(nhii_list3)
    wfile.write('\n\n\tMethod 3 N(H): {}'.format(nhii3))  # test
    mass3 = sightlineMass1(sightline, data, nhii3, mean_cell_area, scale_arg)
    wfile.write('\n\tMethod 3 mass: {}'.format(mass3))

    return nhii3, mass3


def method4(data, sightline, scale_arg, mean_cell_area, wfile):
    wfile.write('\n\nSightline: {}'.format(sightline))
    # method 4: Gnat & Sternberg
    ions = ['OI', 'OII', 'OIII', 'OIV', 'OV', 'OVI', 'OVII', 'OVIII', 'OIX']
    gs_fracs = [  # direct from G&S
        2.6e-1, 9.61e-1, 7.95e-1, 7.27e-1, 5.06e-1, 1.96e-1, 9.94e-1,
        4.51e-1, 9.04e-1
        ]
    wfile.write('\n\n\tMethod 4:')
    nh_list4 = []
    for ion, frac in zip(ions, gs_fracs):
        nh4 = nhiiSightline4(data, ion, sightline, frac, scale_arg)
        wfile.write('\n\t\t{}, {}'.format(ion, nh4))
        nh_list4.append(nh4)
    nh4 = sum(nh_list4)
    mass4 = sightlineMass1(sightline, data, nh4, mean_cell_area, scale_arg)
    wfile.write('\n\tMethod 4 N(H): {}'.format(nh4))
    wfile.write('\n\tMethod 4 mass: {}'.format(mass4))

    return nh4, mass4


# plot results of all methods
def plot(sightlines, data, epoch):
    """

    Parameters:
        sightlines (arr of int): List of numbers corresponding to projection
            columns.
        data (big data object thing): All the y-axis data you want to plot.
        epoch (int): Which epoch you're graphing. Command line argument.

        *** DOESN'T WORK ***
    """
    sightlines = sightlines  # cut it down to 1 sight lines :(

    labels = []
    for line in sightlines:
        labels.append(str(line))

    N = len(sightlines)  # number of sight lines
    # N = 5
    magic = data[0]
    method1 = data[1]
    method2 = data[2]
    method2_1 = data[3]
    method3 = data[4]

    ind = oh.np.arange(N)
    # ind = 1
    width = 0.15
    # width2 = 2 * width
    # width3 = 3 * width
    plt.bar(ind, magic, width, label='Magic')
    plt.bar(ind + width, method1, width, label='Method 1')
    # plt.bar(ind + width2, method2, width, label='Method 2')
    plt.bar(ind + width * 2, method2, width, label='Method 2')
    plt.bar(ind + width * 3, method2_1, width, label='Method 2.1')
    # plt.bar(ind + width3, method3, width, label='Method 3')
    plt.bar(ind + width * 4, method3, width, label='Method 3')

    plt.ylabel('Mass (g)')
    plt.yscale('log')
    plt.title('\"Magic\" vs. observer-calculated mass')

    # plt.xticks(ind + width / 2, (
    #     labels[0], labels[1], labels[2], labels[3], labels[4]))
    plt.xticks(ind + width / 2, labels)
    plt.legend(loc='best')
    plt.savefig('../../Plots/magic_vs_calc_mass_{}.png'.format(str(epoch)))

    return


if __name__ == "__main__":

    # get epoch from command line
    if len(sys.argv[1]) > 1:  # take command line argument
        epoch = sys.argv[1]
    else:
        epoch = 75  # default to 75 Myr

    # select a method
    if len(sys.argv[2]) > 1:
        method = sys.argv[2]
    else:
        method = 'all'

    # to scale or not to scale?
    if len(sys.argv[3]) > 1:
        scale_arg = sys.argv[2]
    else:
        scale_arg = 'unscaled'

    # get all the regular stuff in there; load data, log file
    file, time, ds, ad, cut = oh.main(epoch)
    se.main()  # add all the scaled fields
    wfile = open("../../Plots/%s.txt" % (time), 'a')
    wfile.write("\n\n{}".format(datetime.today().ctime()))
    wfile.write('\n{}'.format(scale_arg))

    # do projection
    proj_x = ds.proj('OI_number', 'x', data_source=cut)

    # get mean cell area in yz-plane
    cell_area = cut['dy'] * cut['dz']
    mean_cell_area = oh.np.mean(cell_area)

    # generate 5 random sight lines
    # sightlist = sightlineList(5, len(proj_x['density']))
    sightlist = [2479, 3752, 3753]

    # put it all in one loop!
    magic_masses = []
    method1_masses = []
    method2_masses = []
    method2_1_masses = []
    method3_masses = []
    method4_masses = []

    if method == 'magic':
        for line in sightlist:
            magic_nh, magic_mass = magicMethod(
                proj_x, line, mean_cell_area, wfile)
    elif method == 'method1':
        for line in sightlist:
            nh1, mass1 = method1(
                proj_x, line, scale_arg, mean_cell_area, wfile
            )
    elif method == 'method2':
        for line in sightlist:
            nh2, mass2 = method2(
                proj_x, line, scale_arg, mean_cell_area, wfile
            )
    elif method == 'method2.1':
        for line in sightlist:
            nh2_1, mass2_1 = method2_1(
                proj_x, line, scale_arg, mean_cell_area, wfile
            )
    elif method == 'method3':
        for line in sightlist:
            nh3, mass3 = method3(
                proj_x, line, scale_arg, mean_cell_area, wfile
            )
    elif method == 'method4':
        for line in sightlist:
            nh4, mass4 = method4(
                proj_x, line, scale_arg, mean_cell_area, wfile
            )
    elif method == 'all':
        for line in sightlist:
            magic_nh, magic_mass = magicMethod(
                proj_x, line, mean_cell_area, wfile)
            magic_masses.append(magic_mass)
            nh1, mass1 = method1(
                proj_x, line, scale_arg, mean_cell_area, wfile
            )
            method1_masses.append(mass1)
            nh2, mass2 = method2(
                proj_x, line, scale_arg, mean_cell_area, wfile
            )
            method2_masses.append(mass2)
            nh2_1, mass2_1 = method2_1(
                proj_x, line, scale_arg, mean_cell_area, wfile
            )
            method2_1_masses.append(mass2_1)
            nh3, mass3 = method3(
                proj_x, line, scale_arg, mean_cell_area, wfile
            )
            method3_masses.append(mass3)
            nh4, mass4 = method4(
                proj_x, line, scale_arg, mean_cell_area, wfile
            )
            method4_masses.append(mass4)

            # plot it.
            data = [magic_masses, method1_masses, method2_masses, \
                method2_1_masses, method3_masses, method4_masses]
            # plot(sightlist, data, epoch)  # this function doesn't work yet

    # conclude
    wfile.close()
