"""

Sydney Whilden
01/26/21

Calculate the mass of the cloud as the 'magician', then use the tools of the
observer to get as close as you can to the REAL mass.

"""

import OH_fields as oh
import scaleeverything as se
import sys
import random


def magician(data):
    cell_mass = data['density'] * data['cell_volume']
    total_mass = sum(cell_mass)

    return total_mass


def nhiiSightlines(proj_ion, data):  # use projected data
    """

    Input projection data; output an array of N(H II) for different sightlines.
    A sightline is a cell of the projected data.

    """
    o_abund = proj_x['o_total_number'] / proj_x['h_total_number']
    o_abund_mean = oh.np.mean(o_abund)

    ion_frac = proj_ion / proj_x['o_total_number']
    ion_frac_mean = oh.np.mean(ion_frac)

    sightlines = proj_ion / (ion_frac_mean * o_abund_mean)

    return sightlines


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
    ions = ['OI', 'OII', 'OIII', 'OIV', 'OV', 'OVI', 'OVII', 'OVIII', 'OIX']

    # generate 5 random sightline numbers
    sightlist = []  # list of sightlines
    for i in range(0, 5):
        # each number can't exceed number of columns
        n = random.randint(0, len(proj_x['density']))  # random sightline
        sightlist.append(n)
    print(sightlist)

    # make sightlines for every ion
    for ion in ions:  # for every oxygen ion
        proj_ion = proj_x['{}_number'.format(ion)]  # projected ion num density
        proj_scaled = proj_x['{}_scaled'.format(ion)] # projected scaled ion nd

        all_sightlines = nhiiSightlines(proj_ion, proj_x)  # pass it ALL the data

        observations = []  # final 5 sightlines
        for sightline in sightlist:
            nhii = all_sightlines[sightline]
            observations.append(nhii)

        print('\n{}:'.format(ion))
        print(observations)


    # column = proj_x cell = sightline


    # conclude
    wfile.close()
