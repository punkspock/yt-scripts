"""
Sydney Whilden
02/02/2021

Calculating the mass along a sight line using only the knowledge of H I, O II,
O IV, O VI, and O VIII.

Notes:

- Can only 'see' O II, O IV, O VI, and O VIII.
- Assumes knowledge of metallicity and ionization fraction averaged over the
whole cloud.
- Calculates H II for multiple ionization levels.


"""

import OH_fields as oh
import scaleeverything as se
import sys
import random
import matplotlib.pyplot as plt


def magician(data):
    cell_mass = data['density'] * data['cell_volume']
    total_mass = sum(cell_mass)

    return total_mass


def nhiiSightline(cd_ion, data):  # use projected data
    """

    Input projection data; output is N(H II) for a single sight line.
    A sight line is a cell of the projected data.

    """
    # metallicity/oxygen abundance
    o_abund = proj_x['o_total_number'] / proj_x['h_total_number']
    # get rid of ~1000 weird values
    o_abund = o_abund[(~oh.np.isnan(o_abund)) & (~oh.np.isinf(o_abund))]
    o_abund_mean = oh.np.mean(o_abund)  # take avg value

    # ionization fraction
    ion_frac = cd_ion / proj_x['o_total_number']
    # get rid of ~1000 weird values
    ion_frac = ion_frac[(~oh.np.isnan(ion_frac)) & (~oh.np.isinf(ion_frac))]
    ion_frac_mean = oh.np.mean(ion_frac) # take avg value

    sightline = cd_ion / (ion_frac_mean * o_abund_mean)

    return sightline


def sightlineMass(n_oi, nh_oi, mean_cell_area):  # calculate mass along a sightline
    """
    Input: array of column densities of all oxygen ions (including O I), array
        of column density of H II associated with each oxygen ion
    Output: mass along the sightline

    Parameters:
        n_oi (arr): Column density of each oxygen ion.
        nhii_oi (arr): Column density of H II associated with each oxygen ion.
            This actually includes H I associated with O I.
    """

    no = sum(n_oi)  # total column density of all oxygen ions
    nh = sum(nh_oi)  # total column density of all H II assoc. w/ O ions

    oxy_mass = no * oh.mOxy
    # print('oxy_mass: {}'.format(oxy_mass))  # test
    hydro_mass = nh * oh.mHydro
    # print('hydro_mass: {}'.format(hydro_mass))  # test

    mass = (oxy_mass + hydro_mass) * mean_cell_area


    return mass


def magicSightline(proj_x, sightline, cell_area):
    """

    Returns total combined mass of hydrogen and oxygen along a sightline using
    the "magician's" knowledge of the content of the simulation. Only accounts
    for mass of hydrogen and oxygen.

    """
    # mass density along sight line
    h_mass = proj_x['h_total_number'][sightline] * oh.mHydro
    # mass density along sight line
    o_mass = proj_x['o_total_number'][sightline] * oh.mOxy
    total_mass = (h_mass + o_mass) * mean_cell_area

    return total_mass


def plot(sightline_list, data):
    """

    data is a 2D array of 'magic' vs. observer-calculated mass.

    """

    fig = plt.figure(figsize=(15, 15))
    X = oh.np.arange(5)
    ax = fig.add_axes([0,0,1,1])
    ax.bar(X + 0.00, data[0], color = 'b', width = 0.25)
    ax.bar(X + 0.25, data[1], color = 'g', width = 0.25)
    ax.set_ylabel('Mass (g)')
    ax.set_xlabel('Sightline')
    ax.legend(labels=['Magic', 'Observer'])
    ax.set_xticks(X)
    ax.set_xticklabels(sightline_list)


    plt.savefig('../../Plots/magic_vs_calc_mass_{}.png'.format(str(epoch)))

    return


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
    ions = ['OII', 'OIV', 'OVI', 'OVIII']
    # ions = ['OVI']

    # generate 5 random sightline numbers
    sightlist = []  # list of sightlines
    for i in range(0, 5):
        # each number can't exceed number of columns
        n = random.randint(0, len(proj_x['density']))  # random sightline
        sightlist.append(n)
    print(sightlist)

    # calculate amount of Oi and amount of H on a sightline
    cd_2d = []  # 2d array of column densities of oxygen ions for each sightline
    nh_2d = []  # 2d array of all N(H II)_Oi for each sightline

    for sightline in sightlist:
        # print('\nSightline: {}'.format(sightline))
        cds = []  # for column densities
        nh = []  # for N(H II) associated with various ions
        for ion in ions:
            cd_ion = proj_x['{}_number'.format(ion)][sightline] # ion col. dens.
            if ion == 'OI':
                line = proj_x['h_neutral_number'][sightline]
                # ^ N(H I)_OI along sight line
            else:
                line = nhiiSightline(cd_ion, proj_x)
                # ^ N(H II)_Oi along sight line
            cds.append(cd_ion)
            nh.append(line)
        cd_2d.append(cds)
        nh_2d.append(nh)

    # calculate mass along each of the 5 sightlines
    cell_area = cut['dy'] * cut['dz']  # bc projection is in x-direction.
    mean_cell_area = oh.np.mean(cell_area)

    masses = []
    magic_mass = []
    for i in range(len(nh_2d)):
        sightline = sightlist[i]
        mass = sightlineMass(cd_2d[i], nh_2d[i], mean_cell_area)
        masses.append(mass)

        # test against simulation
        magic_sightline = magicSightline(proj_x, sightline, mean_cell_area)
        magic_mass.append(magic_sightline)

        print(
            'Magic mass along sightline {}: {:.2e}'.format(
            sightline, magic_sightline))
        print('Mass along sightline {}: {:.2e}'.format(sightline, mass))

    data = [magic_mass, masses]
    altPlot(sightlist, data, epoch)

    difference = []
    for i in range(len(magic_mass)):
        diff = magic_mass[i] - masses[i]
        diff = oh.np.abs(diff)
        difference.append(diff)

    mean_difference = oh.np.mean(difference)
    print('Mean difference: {}'.format(mean_difference))

    # conclude
    wfile.close()
