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

def NHII(ion, nhydro, noxy):
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

    ion_frac = ion / noxy  # fraction of O represented by that oxygen ion
    ion_frac = ion_frac[(~oh.np.isnan(ion_frac))]  # get rid of weird values
    mean_frac = oh.np.mean(ion_frac)  # mean ion fraction

    # calculate using avg O VI/O value (that's meanFrac)
    NHII_mean = (ion_mean / o_abund_mean) * (1 / mean_frac)  # mean CD
    massHII = NHII_mean * oh.mHydro  # mass along sightline. not in solar masses

    NHI_mean = oh.np.mean(nhydro)  # mean column density of H I

    IItoI = NHII_mean / NHI_mean  # ratio of ionized to neutral

    return NHII_mean  # more return values needed?


if __name__ == "__main__":

    epoch = ""  # initialize

    if len(sys.argv[1]) > 1:  # take command line argument
        epoch = sys.argv[1]

    if len(sys.argv[2]) > 1:  # command line argument for scaling
        scale_arg = sys.argv[2]

    # if len(sys.argv[3]) > 1:
    #    fox_arg = sys.argv[3]  # arg about whether to use fox method or ours

    # run main function from OH_fields.py
    file, time, ds, ad, cut = oh.main(epoch)
    se.main()  # add all the scaled fields
    wfile = open("../../Plots/%s.txt" % (time), 'a')

    # calculate HII associated with OVI
    proj_x = ds.proj("OVI_scaled", 'x', data_source=cut)  # do projection
    scaled_noxy = proj_x['OI_scaled']
    unscaled_noxy = proj_x['OI_number']
    nhydro = proj_x['h_neutral_number']  # abundance

    ions = ['OI', 'OII', 'OIII', 'OIV', 'OV', 'OVI', 'OVII', 'OVIII', 'OIX']

    for ion in ions:  # calculation should happen in here
        scaled_ion = proj_x["%s_scaled" % ion]
        unscaled_ion = proj_x["%s_number" % ion]

        if str(scale_arg) == 'scaled':
            NHII_mean = NHII(scaled_ion, nhydro, scaled_noxy)
            wfile.write(
                '\nMean scaled column density of H II {:.2e}'.format(NHII_mean)
                )
        elif str(scale_arg) == 'unscaled':
            NHII_mean = NHII(unscaled_ion, nhydro, unscaled_noxy)
            wfile.write(
                '\nMean unscaled column density of H II {:.2e}'.format(NHII_mean)
                )
        else:  # TODO: Fill this out to deal with invalid arg
            wfile.write('Unscaled:')

    # conclude
    wfile.close()
