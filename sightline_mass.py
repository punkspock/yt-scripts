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
    h_mass = proj_x['h_total_number'][sightline] * oh.mHydro * mean_cell_area
    # print('Magic h_mass: {}'.format(h_mass))  # test
    # mass along sight line
    o_mass = proj_x['o_total_number'][sightline] * oh.mOxy * mean_cell_area
    # print('Magic o_mass: {}'.format(o_mass))  # test
    # total mass
    total_mass = h_mass + o_mass
    # print('Magic total_mass: {}'.format(total_mass))

    return total_mass


# method 1 of getting N(H II)
def nhiiSightline1(proj_x, ion, sightline):
    """

    Calculate N(H II) associated with O VI along a sight line.

    Parameters:
        proj_x (data object): All the projection data.
        ion (str): String name of the oxygen ion you want N(H II) assoc. w/
        sightline (int): Number of projection column/sight line you want the
            N(H II) for.

    """
    # column density of oxygen ion
    novi = proj_x['{}_number'.format(ion)][sightline]
    # metallicity along sight line
    met = proj_x['o_total_number'][sightline] / proj_x['h_total_number'][sightline]
    # ionization fraction along sight line
    ion_frac = novi / proj_x['o_total_number'][sightline]

    nhii = novi / (met * ion_frac)

    return nhii


# method 1 of getting sight line mass
def sightlineMass1(sightline, proj_x, nhii, mean_cell_area):
    """

    Calculate the total mass along a sight line using the total N(H II) and
    knowledge of column densities of all oxygen ions.

    """

    oxy_mass = proj_x['o_total_number'][sightline] * oh.mOxy * mean_cell_area
    # print('Calculated oxy_mass: {}'.format(oxy_mass))
    hydro_mass = nhii * oh.mHydro * mean_cell_area
    # print('Calculated hydro_mass: {}'.format(hydro_mass))
    total_mass = oxy_mass + hydro_mass
    # print('Calculated total_mass: {}'.format(total_mass))

    return total_mass


# method 2 of getting N(H II)
def nhiiSightline2(proj_x, ion, sightline):  # use projected data
    """

    Input projection data; output is N(H II) for a single sight line.
    A sight line is a cell of the projected data.

    """
    cd_ion = proj_x['{}_number'.format(ion)]  # projection column
    cd_sightline = cd_ion[sightline]  # column density for just this sight line

    # mean metallicity/oxygen abundance for whole cloud
    o_abund = proj_x['o_total_number'] / proj_x['h_total_number']
    # get rid of ~1000 weird values
    o_abund = o_abund[(~oh.np.isnan(o_abund)) & (~oh.np.isinf(o_abund))]
    o_abund_mean = oh.np.mean(o_abund)  # take avg value

    # mean ionization fraction for whole cloud
    ion_frac = cd_ion / proj_x['o_total_number']
    # get rid of ~1000 weird values
    ion_frac = ion_frac[(~oh.np.isnan(ion_frac)) & (~oh.np.isinf(ion_frac))]
    ion_frac_mean = oh.np.mean(ion_frac) # take avg value

    # N(H II)_ion along a particular sight line
    nhii_sightline = cd_sightline / (ion_frac_mean * o_abund_mean)

    return nhii_sightline


# method 2 of getting N(H II)
def nhiiSightline3(proj_x, ion, sightline):  # use projected data
    """

    Input projection data; output is N(H II) for a single sight line.
    A sight line is a cell of the projected data.

    """
    cd_ion = proj_x['{}_number'.format(ion)]  # projection column
    cd_sightline = cd_ion[sightline]  # column density for just this sight line

    # mean metallicity/oxygen abundance for whole cloud
    o_abund = proj_x['o_total_number'] / proj_x['h_total_number']
    # get rid of ~1000 weird values
    o_abund = o_abund[(~oh.np.isnan(o_abund)) & (~oh.np.isinf(o_abund))]
    o_abund_mean = oh.np.mean(o_abund)  # take avg value

    # mean ionization fraction for whole cloud
    ion_frac = cd_ion / proj_x['o_total_number']
    # get rid of ~1000 weird values
    ion_frac = ion_frac[(~oh.np.isnan(ion_frac)) & (~oh.np.isinf(ion_frac))]
    ion_frac_mean = oh.np.max(ion_frac) # take max value

    # N(H II)_ion along a particular sight line
    nhii_sightline = cd_sightline / (ion_frac_mean * o_abund_mean)

    return nhii_sightline


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

    # get all the regular stuff in there; load data, log file
    file, time, ds, ad, cut = oh.main(epoch)
    se.main()  # add all the scaled fields
    wfile = open("../../Plots/%s.txt" % (time), 'a')
    wfile.write("\n\n{}".format(datetime.today().ctime()))

    # do projection
    proj_x = ds.proj('OI_number', 'x', data_source=cut)

    # get mean cell area in yz-plane
    cell_area = cut['dy'] * cut['dz']
    mean_cell_area = oh.np.mean(cell_area)

    # generate 5 random sight lines
    sightlist = sightlineList(5, len(proj_x['density']))

    # put it all in one loop!
    magic_masses = []
    method1_masses = []
    method2_masses = []
    method2_1_masses = []
    method3_masses = []

    for line in sightlist:
        wfile.write('\n\nSightline: {}'.format(line))

        # magic method
        magic_mass = magicSightline(proj_x, line, mean_cell_area)
        magic_masses.append(magic_mass)
        magic_nh = proj_x['h_total_number'][line]
        wfile.write('\n\"Magic\" N(H): {}'.format(magic_nh))
        wfile.write('\n\"Magic\" mass: {}'.format(magic_mass))

        # method 1
        ion = 'OVI'  # only use one ion
        nhii1 = nhiiSightline1(proj_x, ion, line)
        wfile.write('\nMethod 1 N(H): {}'.format(nhii1))
        mass1 = sightlineMass1(line, proj_x, nhii1, mean_cell_area)
        method1_masses.append(mass1)
        wfile.write('\nMethod 1 mass: {}'.format(mass1))

        # method 2: "us" method
        ions = ['OI', 'OII', 'OIII', 'OIV', 'OV', 'OVI', 'OVII', 'OVIII', 'OIX']
        nhii_list2 = []
        for ion in ions:
            if ion == 'OI':
                nhii2 = proj_x['h_neutral_number'][line]
            else:
                nhii2 = nhiiSightline2(proj_x, ion, line)
            nhii_list2.append(nhii2)
        # print('nhii_list2: {}'.format(nhii_list2))  # test
        nhii2 = sum(nhii_list2)
        wfile.write('\nMethod 2 N(H): {}'.format(nhii2))  # test
        mass2 = sightlineMass1(line, proj_x, nhii2, mean_cell_area)
        method2_masses.append(mass2)
        wfile.write('\nMethod 2 mass: {}'.format(mass2))

        # method 2.1: 'fox' method
        nh_list2_1 = []
        for ion in ions:
            nh2_1 = nhiiSightline3(proj_x, ion, line)
            nh_list2_1.append(nh2_1)
        nh2_1 = sum(nh_list2_1)
        mass2_1 = sightlineMass1(line, proj_x, nh2_1, mean_cell_area)
        method2_1_masses.append(mass2_1)
        wfile.write('\nMethod 2.1 N(H): {}'.format(nh2_1))
        wfile.write('\nMethod 2.1 mass: {}'.format(mass2_1))

        # method 3
        ions = ['OII', 'OIV', 'OVI', 'OVIII']
        nhii_list3 = []
        for ion in ions:
            nhii3 = nhiiSightline2(proj_x, ion, line)
            nhii_list3.append(nhii3)
        # print('nhii_list3: {}'.format(nhii_list3))  # test
        nhii3 = sum(nhii_list3)
        wfile.write('\nMethod 3 N(H): {}'.format(nhii3))  # test
        mass3 = sightlineMass1(line, proj_x, nhii3, mean_cell_area)
        method3_masses.append(mass3)
        wfile.write('\nMethod 3 mass: {}'.format(mass3))

    # plot it.
    data = [magic_masses, method1_masses, method2_masses, method2_1_masses,\
        method3_masses]
    plot(sightlist, data, epoch)  # this function doesn't work yet

    # conclude
    wfile.close()
