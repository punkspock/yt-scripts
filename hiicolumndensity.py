"""
Sydney Whilden
08/13/2020

Put a lower bound on column density of H II in Fox's high ion phases.
See page 1058 of Fox (2010)

"""

import OH_fields as oh
import OHmetallicity as om
import ionfraction as ifr
from sympy import diff, exp
from sympy.abc import x, y

if __name__ == "__main__":
    ds, ad = oh.loadData(oh.file)  # load data file into yt
    oh.addFields()  # add all the derived fields defined in oh
    cut = oh.velocityCut(ad)

    # CALCULATE

    # OVI column density
    proj_x = ds.proj("OVI_number", "x", data_source=cut)  # make projection
    o5cd = proj_x["OVI_number"]  # O VI column density
    o5cdMean = oh.np.mean(o5cd)  # mean O VI column density

    # oxygen abundance
    oAbundance = proj_x["o_neutral_number"] / proj_x["h_neutral_number"]
    # oAbundance = proj_x["o_total_number"] / proj_x["h_total_number"]
    oAbundance = oAbundance[(~oh.np.isnan(oAbundance)) & (
        ~oh.np.isinf(oAbundance))]  # get rid of weird values
    oAbundMean = oh.np.mean(oAbundance)  # mean oxygen abundance
    # oAbundMean = 0.00004  # test

    # constant = o5cd / oAbundMean
    constant = o5cdMean / oAbundMean  # constant values in the function

    # (O VI/O) mean pulled from other script
    ionFraction = proj_x["OVI_number"] / proj_x["o_total_number"]  # O VI/O
    ionFraction = ionFraction[(~oh.np.isnan(ionFraction))]
    meanFrac = oh.np.max(ionFraction)  # average value of O VI/O

    # calculate using avg O VI/O value (that's meanFrac)
    NHII_mean = constant * (1 / meanFrac)
    # massHII = (NHII / oh.A) * oh.hydro_mol / oh.M_sun  # in solar masses
    massHII = NHII_mean * oh.mHydro  # along a sightline.

    print(
        "H II column density: {:.2e}\n".format(NHII_mean),
        "H II mass using average O VI/O: {:.2e}".format(massHII)
        )

    # N(H II) / N(H I)
    NHI = proj_x["h_neutral_number"]
    NHI_mean = oh.np.mean(NHI)

    IItoI = NHII_mean / NHI_mean

    print("N(H II)/N(H I): {:.2e}".format(IItoI))

    # # calculate using cAlCuLuS
    # temp = cut["temperature"]
    # logTemp = oh.np.log10(temp)
    # logIonFraction = oh.np.log10(ionFraction)
    #
    # # necessary for polyfit but BAD FOR PLOT
    # # stopgap solution
    # lT = logTemp[(~oh.np.isnan(logTemp)) & (~oh.np.isinf(logTemp))]
    # lIF = logIonFraction[0:len(lT)]

    # relationship between logTemp and logIonFraction
    # a, b, c, d, e, f = ifr.express5(lT, lIF)  # get coefficients
    # expr = a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f  # write expression out
    # FT = 1 / expr
    # der = diff(expr, x)  # use symbolic differentiation to take derivative

    # don't necessarily do this with max
    # if_max = oh.np.max(ion_fraction)  # max value of O VI/O I



    # print("Mass of H II associated with O VI: {a.2e}".format(h2cd))
