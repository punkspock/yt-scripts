"""
Sydney Whilden
02/01/2021

Method 1 for observer measuring cloud mass.

Notes:
- Can 'see' all ions of oxygen.
- Uses ionization fraction and metallicity for a single sight line at a time.
- Calculates H II for one ionization level -- O VI.
"""

import OH_fields as oh
import scaleeverything as se
import sys
import random
import matplotlib.pyplot as plt


def magician(data):  # helium included here
    cell_mass = data['density'] * data['cell_volume']
    total_mass = sum(cell_mass)

    return total_mass


def sightlineNHII(proj_x, ion, sightline):
    """

    Calculate N(H II) along a sight line associated with O VI.

    """
    # column density of oxygen ion
    novi = proj_x['{}_number'.format(ion)][sightline]
    # metallicity along sight line
    met = proj_x['OI_number'][sightline] / proj_x['h_neutral_number'][sightline]
    # ionization fraction along sight line
    ion_frac = novi / proj_x['o_total_number'][sightline]

    nhii = novi / (met * ion_frac)

    return nhii


def sightlineMass(sightline, proj_x, nhii, mean_cell_area):
    """

    Calculate the total mass along a sight line using the total N(H II) and
    knowledge of column densities of all oxygen ions.

    """

    oxy_mass = proj_x['o_total_number'][sightline] * oh.mOxy  # in cm^-2
    print('oxy_mass: {}'.format(oxy_mass))
    hydro_mass = nhii * oh.mHydro  # in cm^-2
    print('hydro_mass: {}'.format(hydro_mass))
    unit_area_mass = oxy_mass + hydro_mass  # mass / cm**2
    total_mass = unit_area_mass * mean_cell_area

    return total_mass


def magicSightline(proj_x, sightline, cell_area):
    """

    Returns total combined mass of hydrogen and oxygen along a sightline using
    the "magician's" knowledge of the content of the simulation. Only accounts
    for mass of hydrogen and oxygen.

    """
    # mass density along sight line
    h_mass = proj_x['h_total_number'][sightline] * oh.mHydro
    print('h_mass: {}'.format(h_mass))  # test
    # mass density along sight line
    o_mass = proj_x['o_total_number'][sightline] * oh.mOxy
    print('o_mass: {}'.format(o_mass))  # test
    total_mass = (h_mass + o_mass) * mean_cell_area

    return total_mass

def altPlot(sightlines, data, epoch):
    """

    In case the other plotting function doesn't work.

    """
    labels = []
    for line in sightlines:
        labels.append(str(line))

    N = 5  # number of sight lines
    magic = data[0]
    observer = data[1]

    ind = oh.np.arange(N)
    width = 0.35
    plt.bar(ind, magic, width, label='Magic')
    plt.bar(ind + width, observer, width,
        label='Observer')

    plt.ylabel('Mass (g)')
    plt.yscale('log')
    plt.title('\"Magic\" vs. observer-calculated mass')

    plt.xticks(ind + width / 2, (
        labels[0], labels[1], labels[2], labels[3], labels[4]))
    plt.legend(loc='best')
    plt.savefig('../../Plots/magic_vs_calc_mass_{}.png'.format(str(epoch)))

    return


if __name__ == "__main__":

    # get epoch from command line
    if len(sys.argv[1]) > 1:  # take command line argument
        epoch = sys.argv[1]
    else:
        epoch = 75  # default to 75 Myr

    # run main function from OH_fields.py to load data, log file
    file, time, ds, ad, cut = oh.main(epoch)
    se.main()  # add all the scaled fields
    wfile = open("../../Plots/%s.txt" % (time), 'a')

    # calculate the cloud mass using full knowledge of the simulation
    magic_mass = magician(cut)
    wfile.write("\n\nMagic mass of cloud: {:.2e}".format(magic_mass))

    # compute observer mass using sightlines
    proj_x = ds.proj('OI_number', 'x', data_source=cut)
    # ions = ['OI', 'OII', 'OIII', 'OIV', 'OV', 'OVI', 'OVII', 'OVIII', 'OIX']
    ion = 'OVI'

    # generate 5 random sight line numbers
    sightlist = []  # list of sight lines
    for i in range(0, 5):
        # each number can't exceed number of columns
        n = random.randint(0, len(proj_x['density']))  # random sightline
        sightlist.append(n)
    print(sightlist)

    cell_area = cut['dy'] * cut['dz']  # bc projection is in x-direction.
    mean_cell_area = oh.np.mean(cell_area)

    # for each sight line, calculate N(H II)_OVI and mass
    nhii_list = []
    masses = []
    magic_masses = []
    for sightline in sightlist:
        wfile.write('\n\nSight line: {}'.format(sightline))
        # calculate N(H II)
        nhii = sightlineNHII(proj_x, ion, sightline)
        nhii_list.append(nhii)
        # calculate mass along each sight line (includes H and O)
        mass = sightlineMass(sightline, proj_x, nhii, mean_cell_area)
        masses.append(mass)
        # calculate mass along sight line from the domain
        magic_mass = magicSightline(proj_x, sightline, mean_cell_area)
        magic_masses.append(magic_mass)
        # print results
        wfile.write('\nN(H II)_OVI: {:.2e}'.format(nhii))
        wfile.write(
            '\nMass along sight line from calculated N(H II): {:.2e}'.format(
            mass))
        wfile.write(
            '\n\"Magic\" mass along sight line: {:.2e}'.format(magic_mass)
            )

    data = [magic_masses, masses]
    altPlot(sightlist, data, epoch)

    # conclude
    wfile.close()
