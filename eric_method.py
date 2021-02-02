"""
Sydney Whilden
01/31/2021

This script is solely so I can get a grasp on exactly how Eric is getting hjis
results for column density of N(H II)_total along a sight line.
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

    # for use in method 3
    oh.yt.add_field(
        ('gas', 'h_num'), units='dimensionless', function=totalH,
        force_override=True
        )

    # do the projection
    # QUESTION: what does method='sum' do?
    proj_x = ds.proj('OI_number', 'x', data_source=cut)  # regular
    proj_x2 = ds.proj('OI_number', 'x', method='sum', data_source=cut)  # sum

    # calculate total hydrogen atoms
    cell_h = cut['h_total_number'] * cut['cell_volume']
    total_h = sum(cell_h)  # total number in a cell
    # wfile.write('\nTotal number of hydrogen atoms: {:.2e}'.format(total_h))
    print('\nTotal number of hydrogen atoms: {:.2e}'.format(total_h))

    # calculate average column density of hydrogen
    # sum of all atoms in a sight line * sightline_depth / sightline_volume
    all_h = proj_x2['h_num']  # all atoms in a sight line
    all_h = all_h[all_h != 0]  # exclude zero values
    depth = proj_x2['dx']  # depth of sight line
    depth = depth[depth != 0]  # exclude zero values
    sl_vol = proj_x2['cell_volume']  # volume of sight line
    sl_vol = sl_vol[sl_vol != 0]  # exclude zero values
    nh3 = all_h * depth / sl_vol
    mean_nh3 = oh.np.mean(nh3)
    # wfile.write('\nMean column density of hydrogen: {:.2e}'.format(mean_nh))
    print('\nMean column density of hydrogen: {:.2e}'.format(mean_nh3))

    # calculate total oxygen atoms
    cell_o = cut['o_total_number'] * cut['cell_volume']
    total_o = sum(cell_o)
    # wfile.write('\nTotal number of oxygen atoms: {:.2e}'.format(total_o))
    print('\nTotal number of oxygen atoms: {:.2e}'.format(total_o))

    # conclude
    wfile.close()
