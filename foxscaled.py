"""
Sydney Whilden
01/05/2021

Calculate the column density of ionized and neutral hydrogen associated with
each available O ion using the Fox method or our method with unscaled or
re-scaled metallicity.
"""

import OH_fields as oh
import scaleeverything as se
import sys
import matplotlib.pyplot as plt

def NHII(ion, nhydro, noxy, toxy, method):
    """
    Take in projected oxygen ion number density (scaled or unscaled), oxygen
    abundance, and fraction of total oxygen represented by the oxygen ion,
    and calculate associated column density of H II.

    Parameters:
        ion (arr): scaled or unscaled projected number density of a particular
            oxygen ion
        nhydro (arr): projected number density of neutral hydrogen
        noxy (arr): projected number density (scaled or unscaled) of neutral
            oxygen
    """

    o_abund = noxy / nhydro  # neutral oxygen / neutral hydrogen
    o_abund = o_abund[(~oh.np.isnan(o_abund)) & (
        ~oh.np.isinf(o_abund))]  # get rid of weird values
    o_abund_mean = oh.np.mean(o_abund)  # mean oxygen abundance

    ion_mean = oh.np.mean(ion)  # mean column density of oxygen ion

    ion_frac = ion / toxy  # fraction of O represented by that oxygen ion
    ion_frac = ion_frac[(~oh.np.isnan(ion_frac)) & (~oh.np.isinf(ion_frac))]
    mean_frac = oh.np.mean(ion_frac)  # mean ion fraction for 'us' method
    max_frac = oh.np.max(ion_frac)  # max ion fraction for 'fox' method
    # calculate using avg O VI/O value (that's meanFrac)

    if method == 'fox':
        NHII_mean = (ion_mean / o_abund_mean) * (1 / max_frac)  # max CD
    elif method == 'us':
        NHII_mean = (ion_mean / o_abund_mean) * (1 / mean_frac)  # mean CD
    else:
        NHII_mean = (ion_mean / o_abund_mean) * (1 / mean_frac)

    massHII = NHII_mean * oh.mHydro  # mass along sightline. not in solar masses

    # NHI_mean = oh.np.mean(nhydro)  # mean column density of H I
    # mass_HI = NHI_mean * oh.mHydro

    return NHII_mean  # more return values needed?


def graph(labels, values, scale_arg, method, time):
    """

    Graph N(HII)_mean associated with each ion of oxygen.

    """
    # colordict = {}
    # colordict["Average"] = (0, 0, 0, 1.0)

    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    # ax.bar(labels, values, color=[colordict[label] for label in labels])
    ax.bar(labels, values)
    ax.set_ylabel('Column Density of H II')
    ax.set_xlabel('Oxygen Ion')
    ax.set_title('N(H II) associated with O ions for {}, {} method, {}'.format(
        time, method, scale_arg
        ))
    plt.ylim(min(values) - 2)  # this line causes an error for scaled graphs
    # plt.ylim(min(values) * 0.6)  # this line causes the same error
    # not having either of the lines above results in a segmentation fault 11.
    # ax.set_ylim(min(values) - 2)  # attempt 3!

    plt.savefig(
        '../../Plots/nhii_all_ions_{}_{}_{}'.format(scale_arg, method, time)
        )
    # plt.close()
    plt.show()

    return


if __name__ == "__main__":

    epoch = ""  # initialize

    if len(sys.argv[1]) > 1:  # take command line argument
        epoch = sys.argv[1]
    else:
        epoch = 75

    if len(sys.argv[2]) > 1:  # command line argument for scaling
        scale_arg = sys.argv[2]
    else:
        scale_arg = 'unscaled'

    if len(sys.argv[3]) > 1:
        method = sys.argv[3]  # arg about whether to use fox method or ours
    else:
        method = 'us'

    # run main function from OH_fields.py
    file, time, ds, ad, cut = oh.main(epoch)
    se.main()  # add all the scaled fields
    wfile = open("../../Plots/%s.txt" % (time), 'a')

    # calculate HII associated with OVI
    proj_x = ds.proj("OVI_scaled", 'x', data_source=cut)  # do projection
    scaled_noxy = proj_x['OI_scaled']
    unscaled_noxy = proj_x['OI_number']
    scaled_toxy = proj_x['o_total_scaled']
    unscaled_toxy = proj_x['o_total_number']
    # unscaled_noxy = proj_x['o_neutral_number']  # test
    nhydro = proj_x['h_neutral_number']  # abundance

    # also use as labels for plot
    ions = ['OII', 'OIII', 'OIV', 'OV', 'OVI', 'OVII', 'OVIII', 'OIX']
    nhii_mean = []  # initialize for plotting

    # TEST
    # unscaled_ion = proj_x["OVI_number"]
    # NHII_mean = NHII(unscaled_ion, nhydro, unscaled_noxy, unscaled_toxy)
    # wfile.write(
    #     '\nMean unscaled column density of HII {:.2e}'.format(NHII_mean)
    #     )

    if method == 'fox' or method == 'us':
        wfile.write('\n\nUsing {}'.format(method))
    else:
        wfile.write('\n\nUsing default "us" method: ')


    # Doing calculations just for N(H I)_O I
    if str(scale_arg) == 'scaled':
        nhi = NHII(
            proj_x["OI_number"], nhydro, scaled_noxy, scaled_toxy, method
            )
        wfile.write('\nScaled N(HI)_OI {:.2e} 1/cm**3'.format(nhi))
    elif str(scale_arg) == 'unscaled':
        nhi = NHII(
            proj_x["OI_number"], nhydro, unscaled_noxy, unscaled_toxy, method
            )
        wfile.write('\nUnscaled N(HI)_OI {:.2e} 1/cm**3'.format(nhi))
    else:
        nhi = NHII(
            proj_x["OI_number"], nhydro, unscaled_noxy, unscaled_toxy, method
            )
        wfile.write('\nUnscaled N(HI)_OI {:.2e} 1/cm**3'.format(nhi))
    # nhi is the total average column density of H I.

    # Calculate for the rest of the ions
    for ion in ions:  # calculation should happen in here
        scaled_ion = proj_x["%s_scaled" % ion]
        unscaled_ion = proj_x["%s_number" % ion]

        if str(scale_arg) == 'scaled':
            NHII_mean = NHII(
                scaled_ion, nhydro, scaled_noxy, scaled_toxy, method
                )
            # do the same calculation but for neutral oxygen.
            # this gives the column density of H I, not H II
            wfile.write(  # record the results
                '\nMean scaled N(HII)_{} {:.2e} 1/cm**3'.format(ion, NHII_mean),
                )
        elif str(scale_arg) == 'unscaled':
            NHII_mean = NHII(
                unscaled_ion, nhydro, unscaled_noxy, unscaled_toxy, method
                )
            wfile.write(
                '\nMean unscaled N(HII)_{} {:.2e} 1/cm**3'.format(
                ion, NHII_mean),
                )
        else:  # TODO: Fill this out to deal with invalid arg

            # defaults to unscaled.
            NHII_mean = NHII(
                unscaled_ion, nhydro, unscaled_noxy, unscaled_toxy, method
                )

            wfile.write(
                '\nMean unscaled N(HII)_{} {:.2e} 1/cm**3'.format(
                ion, NHII_mean),
                )

        nhii_mean.append(NHII_mean)  # append one value per ion
        # the above must be summed to get total mean N(H II)
        # nhii_mean is not a typical array -- it's an array of YTQuantities.
        # will not graph properly on the x-axis for the scaled runs

    nhii_total = sum(nhii_mean)  # total average column density of H II
    nh = nhi + nhii_total  # total average column density of all hydrogen
    # for comparison
    nh_grid = oh.np.mean(proj_x['h_total_number'])  # calculated from the grid

    wfile.write("\nTotal average N(H I) + N(H II): {:.2e}".format(nh))
    wfile.write("\nTotal average N(H) from the grid: {:.2e}".format(nh_grid))

    # graph of N(H II)_Oi
    log_nhii = oh.np.log10(nhii_mean)
    graph(ions, nhii_mean, scale_arg, method, time)

    # conclude
    wfile.close()
