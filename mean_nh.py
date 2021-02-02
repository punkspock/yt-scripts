"""
Sydney Whilden
01/31/2021

Testing three different methods of measuring mean column density of hydrogen.
"""

import OH_fields as oh
import scaleeverything as se
import sys


def totalH(field, ad):
    """
    Calculate total H atoms in a single cell.
    """
    totalH = ad['h_total_number'] * ad['cell_volume']

    return totalH


def nhCell(field, ad):  # column density of H for one cell
    nh_cell = ad['h_total_number'] * ad['dx']

    return nh_cell


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

    # for use in method 2
    oh.yt.add_field(
        ('gas', 'nh_cell'), units='cm**-2', function=nhCell, force_override=True
        )

    # for use in method 3
    oh.yt.add_field(
        ('gas', 'h_num'), units='dimensionless', function=totalH,
        force_override=True
        )

    # METHOD 1
    # projection of number density.
    proj_x = ds.proj('OI_number', 'x', data_source=cut)
    nh = proj_x['h_total_number']
    mean_nh = oh.np.mean(nh)
    print("Method 1 (projecting number density): {:.2e}".format(mean_nh))

    # METHOD 2
    # sum of column density field
    # difference is this projection uses method='sum'
    proj_x2 = ds.proj('OI_number', 'x', method='sum', data_source=cut)
    nh2 = proj_x2['nh_cell']  # sum column density for each cell down the x-dir.
    mean_nh2 = oh.np.mean(nh2)
    print("\nMethod 2 (summing column density field): {:.2e}".format(mean_nh2))

    # METHOD 3
    # sum of all atoms in a sight line * sightline_depth / sightline_volume
    all_h = proj_x2['h_num']  # all atoms in a sight line
    all_h = all_h[all_h != 0]  # exclude zero values
    depth = proj_x2['dx']  # depth of sight line
    depth = depth[depth != 0]  # exclude zero values
    sl_vol = proj_x2['cell_volume']  # volume of sight line
    sl_vol = sl_vol[sl_vol != 0]  # exclude zero values
    nh3 = all_h * depth / sl_vol
    mean_nh3 = oh.np.mean(nh3)
    print(
        "\nMethod 3 (sum of all atoms * depth / volume): {:.2e}".format(
        mean_nh3)
        )

    # conclude
    wfile.close()
