"""
Sydney Whilden
01/31/21

Calculate for a single cell:

    - Total number of hydrogen atoms (NOT number density)
    - Column density of hydrogen N(H)
    - N(H II) associated with each ion of oxygen Oi

To show that:
    - All H II is associated with every O ion.
    - The total mass of H II can be recovered from the column density of H II
        that is associated with each O ion.
    - The total mass of the H and O in the cell can be calculated from this.

"""

import OH_fields as oh
import scaleeverything as se
import sys
import random
import matplotlib.pyplot as plt


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

    # choose random cell.
    # n = random.randint(0, len(cut['density']))  # the cell is called n
    n = 273

    # total number of hydrogen atoms
    total_h = cut['h_total_number'][n] * cut['cell_volume'][n]

    # hydrogen column density
    h_cd = cut['h_total_number'][n] * cut['dx'][n]
    print('H II column density from domain: {}'.format(h_cd))

    # hydrogen associated with one oxygen ion
    o6_cd = cut['OVI_number'][n] * cut['dx'][n]
    metallicity = cut['o_total_number'][n] / cut['h_total_number'][n]
    ion_frac = cut['OVI_number'][n] / cut['o_total_number'][n]

    nhii = o6_cd / (metallicity * ion_frac)

    print('H II column density associated with O VI: {}'.format(nhii))


    # conclude
    wfile.close()
