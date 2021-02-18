"""
Sydney Whilden
01/31/2021

Do all the same things as single_cell.py, but along a single sight line.


Calculate for a single sight line:

    - Total number of hydrogen atoms (NOT number density)
    - Column density of hydrogen N(H)
    - N(H II) associated with each ion of oxygen Oi

To show that:
    - All H II is associated with every O ion.
    - The total mass of H II can be recovered from the column density of H II
        that is associated with each O ion.
    - The total mass of the H and O in the sight line can be calculated from this.

"""

import OH_fields as oh
import scaleeverything as se
import sys
import random
import matplotlib.pyplot as plt
oh.yt.funcs.mylog.setLevel(50)


def hNum(field, ad):
    h_num = ad['h_total_number'] * ad['cell_volume']

    return h_num


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

    oh.yt.add_field(
        ('gas', 'h_num'), units='dimensionless', function=hNum,
        force_override=True
        )

    # project to get sight lines
    proj_x = ds.proj('OI_number', 'x', data_source=cut)
    proj_x2 = ds.proj('OI_number', 'x', method='sum', data_source=cut)

    # pick random sight line
    # n = random.randint(0, len(proj_x['density']))
    n = 1220

    # total number of hydrogen atoms
    total_h = proj_x2['h_num'][n]
    print('Total hydrogen atoms on sight line: {:.2e}'.format(total_h))

    cell_area = cut['dy'] * cut['dz']  # test
    mean_cell_area = oh.np.mean(cell_area)

    # total column density of of hydrogen atoms
    cd_h = proj_x['h_total_number'][n]
    print('Total number density of hydrogen on sight line: {}'.format(cd_h))
    cd_h_mass = cd_h * oh.mHydro * mean_cell_area  # test
    print(cd_h_mass)

    # H II along the sight line associated with O VI
    cd_o6 = proj_x['OVI_number'][n]
    metallicity = proj_x['o_total_number'][n] / proj_x['h_total_number'][n]
    ion_frac = proj_x['OVI_number'][n] / proj_x['o_total_number'][n]

    nhii = cd_o6 / (metallicity * ion_frac)
    print(
        'Column density of hydrogen associated with O VI: {}'.format(nhii)
        )
    nhii_mass = nhii * oh.mHydro * mean_cell_area  # test
    print(nhii_mass)

    # conclude
    wfile.close()
