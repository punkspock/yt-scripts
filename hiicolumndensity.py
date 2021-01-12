"""
Sydney Whilden
08/13/2020

Put a lower bound on column density of H II in Fox's high ion phases.
See page 1058 of Fox (2010)

"""

import OH_fields as oh
import sys
# import OHmetallicity as om
# import ionfraction as ifr
# from sympy import diff, exp
# from sympy.abc import x, y

if __name__ == "__main__":

    if len(sys.argv[1]) > 1:
        epoch = str(sys.argv[1])
    else:
        print("Running with default epoch.")
        epoch = '75'

    file, time, ds, ad, cut = oh.main(epoch)
    # Myr100 = "../../Data/4.2.1.density_sap_hdf5_plt_cnt_0100"
    # ds, ad = oh.loadData(Myr100)
    # oh.addFields()
    # cut = oh.velocityCut(ad)

    # wfile = open("../../Plots/%s.txt" % ("t=100Myr"), 'a')
    wfile = open("../../Plots/%s.txt" % (time), 'a')

    # CALCULATE

    # OVI column density
    proj_x = ds.proj("OVI_number", "x", data_source=cut)  # make projection
    o6cd = proj_x["OVI_number"]  # O VI column density
    o6cdMean = oh.np.mean(o6cd)  # mean O VI column density

    # oxygen abundance
    oAbundance = proj_x["o_neutral_number"] / proj_x["h_neutral_number"]
    # oAbundance = proj_x["o_total_number"] / proj_x["h_total_number"]
    oAbundance = oAbundance[(~oh.np.isnan(oAbundance)) & (
        ~oh.np.isinf(oAbundance))]  # get rid of weird values
    oAbundMean = oh.np.mean(oAbundance)  # mean oxygen abundance
    # oAbundMean = 0.00004  # test

    # constant = o5cd / oAbundMean
    constant = o6cdMean / oAbundMean  # constant values in the function

    # (O VI/O) mean pulled from other script
    ionFraction = proj_x["OVI_number"] / proj_x["o_total_number"]  # O VI/O
    ionFraction = ionFraction[(~oh.np.isnan(ionFraction))]
    meanFrac = oh.np.mean(ionFraction)  # average value of O VI/O
    # maxFrac = oh.np.max(ionFraction)  # test

    # calculate using avg O VI/O value (that's meanFrac)
    NHII_mean = constant * (1 / meanFrac)
    # NHII_mean = constant * (1 / maxFrac)  # test
    # massHII = (NHII / oh.A) * oh.hydro_mol / oh.M_sun  # in solar masses
    massHII = NHII_mean * oh.mHydro  # along a sightline.
    # N(H II) / N(H I)
    NHI = proj_x["h_neutral_number"]
    NHI_mean = oh.np.mean(NHI)

    IItoI = NHII_mean / NHI_mean

    # record the findings.
    wfile.write("\nH II mean column density: {:.2e}".format(NHII_mean))
    wfile.write("\nH I mean column density: {:.2e}".format(NHI_mean))
    wfile.write("\nH II mass using average O VI/O: {:.2e}".format(massHII))
    wfile.write("\nN(H II)/N(H I): {:.2e}".format(IItoI))
    wfile.close()

    # # calculate using cAlCuLuS
    # temp = cut["temperature"]
    # logTemp = oh.np.log10(temp)
    # logIonFraction = oh.np.log10(ionFraction)
    #
    # # necessary for polyfit but BAD FOR PLOT
    # # stopgap solution
    # lT = logTemp[(~oh.np.isnan(logTemp)) & (~oh.np.isinf(logTemp))]
    # lIF = logIonFraction[0:len(lT)]

    # # relationship between logTemp and logIonFraction
    # a, b, c, d, e, f = ifr.express5(lT, lIF)  # get coefficients
    # expr = a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f  # write expression out
    # FT = 1 / expr
    # der = diff(expr, x)  # use symbolic differentiation to take derivative

    # # This gives wrong results.
    # f = open("coefficients_%s.txt" % (oh.time), 'r')
    # arr = f.readlines()  # array containing 1 string
    # strings = arr[0].split(',')  # arr[0] is the string. array contents.
    # coeffs = []  # initialize
    # for i in strings[0:len(strings)-1]:  # let the f go. it's no longer usable
    #     i = oh.np.float(i)
    #     coeffs.append(i)
    # a, b, c, d, e, = coeffs  # gonna try to get the f back later
    # f.close()

    # don't necessarily do this with max
    # if_max = oh.np.max(ion_fraction)  # max value of O VI/O I



    # print("Mass of H II associated with O VI: {a.2e}".format(h2cd))
