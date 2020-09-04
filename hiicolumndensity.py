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
from decimal import Decimal

if __name__ == "__main__":
    ds, ad = oh.loadData(oh.file)  # load data file into yt
    oh.addFields()  # add all the derived fields defined in oh
    cut = oh.velocityCut(ad)

    # CALCULATE
    # (O VI/O) mean pulled from other script
    ionFraction = cut["OVI_number"] / cut["o_total_number"]
    logIonFraction = oh.np.log10(ionFraction)
    meanFrac = oh.np.mean(ionFraction) 

    temp = cut["temperature"]
    logTemp = oh.np.log10(temp)
    
    # relationship between logTemp and logIonFraction
    a, b, c, d, e, f = ifr.express5(logTemp, logIonFraction)  # get coefficients
    expr = a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f  # write expression out
    FT = 1 / expr 
    # der = diff(expr, x)  # use symbolic differentiation to take derivative

    # don't necessarily do this with max
    # if_max = oh.np.max(ion_fraction)  # max value of O VI/O I

    # oxygen abundance
    proj_x = ds.proj("OVI_number", "x", data_source=cut)
    o_abundance = proj_x["o_neutral_number"] / proj_x["h_neutral_number"]
    o_abundance = o_abundance[(~oh.np.isnan(o_abundance))]
    mean_o = oh.np.mean(o_abundance) # mean value of O abundance
    o5cd = proj_x["OVI_number"]  # O VI column density
    o5cd_mean = oh.np.mean(o5cd)

    

    # h2cd = o5cd_mean / (if_max * mean_o)
    h2cd = o5cd_mean / (meanFrac * mean_o)
    h2cd = h2cd / oh.M_sun

    # with the fancy expression
    C = (o5cd_mean / mean_o)  # treat like a constant
    formula = C * FT 
    der = diff(formula, x)

    print("Mass of H II associated with O VI: %.2E" % Decimal(h2cd))
