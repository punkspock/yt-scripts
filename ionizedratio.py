"""

07/22/2020
Sydney Whilden
Determine the ratio of ionized to neutral material.

"""

import yt
from yt.units.yt_array import YTQuantity
import numpy as np

# CONSTANTS
oxy_mol = YTQuantity(15.9994, 'g/mol')  # oxygen mole mass
hydro_mol = YTQuantity(2.016, 'g/mol')
A = YTQuantity(6.023e23, 'mol**-1')  # Avogadro's number
M_sun = YTQuantity(2e33, 'g')


# FUNCTIONS
def bulkSub(field, ad):
    bulk_vel = YTQuantity(150, 'km/s')  # set bulk velocity
    sub = ad['flash', 'velz'] - bulk_vel  # subtract bulk velocity
    # why velz and not velx or vely? How do the velocity fields work?
    return sub  # return velz field with bulk velocity subtracted


def oxyIonMass(field, ad):
    """
    Returns total cell mass represented by all oxygen ions available.
    """
    all = ad['flash', 'o1  '] + ad['flash', 'o5  '] + ad['flash', 'o2  ']
    + ad['flash', 'o3  '] + ad['flash', 'o4  '] + ad['flash', 'o6  ']
    + ad['flash', 'o7  '] + ad['flash', 'o8  ']  # a fraction

    mass = all * ad["density"] * ad["cell_volume"]  # result in g

    return mass


def oxyNeutralMass(field, ad):
    """
    Returns total mass of neutral oxygen in cell.
    """
    mass = ad["flash", "o   "] * ad["density"] * ad["cell_volume"]

    return mass


def oxyIonNumber(field, ad):
    """
    Returns number density of all oxygen ions in a cell
    """
    mols = ad["o_ion_mass"] / oxy_mol  # divide by grams in a mole of O
    particles = mols * A  # multiply by Avogadro's number

    return particles


def oxyNeutralNumber(field, ad):
    """
    Returns number density of neutral oxygen in cell
    """
    mols = ad["o_neutral_mass"] / oxy_mol  # divide by grams in a mole of O
    particles = mols * A  # multiply by Avogadro's number

    return particles


def oxyNumber(field, ad):
    number = ad["o_ion_number"] + ad["o_neutral_number"]

    return number


# may want to change this to be a ratio of column densities
def ionRatio(field, ad):
    """
    Return ratio of ionized oxygen to neutral oxygen.
    """
    ratio = ad["o_ion_number"] / ad["o_neutral_number"]
    # ratio = ratio[(~np.isnan(ratio)) & (~np.isinf(ratio))]

    return ratio


def hMass(field, ad):
    """
    Return mass of all hydrogen, ionized and neutral, in a cell.
    """
    # mass = ad["h_ion_mass"] + ad["h_neutral_mass"]
    # correction:
    mass = ad["h   "] * ad["density"] * ad["cell_volume"]

    return mass


def hNumber(field, ad):
    """
    Calculate number density of all hydrogen in a cell.
    """
    mols = ad["h_total_mass"] / hydro_mol
    particles = mols * A

    return particles


def metallicity(field, ad):
    """
    Calculate the ratio of total oxygen to total hydrogen, which we assume
    is equal to O I/ H I.
    THIS IS NOT A MASS RATIO. THIS IS A RATIO OF NUMBER DENSITIES.
    """
    # correction

    ratio = ad["o_total_number"] / ad["h_total_number"]
    # ratio = ratio[(~np.isnan(ratio)) & (~np.isinf(ratio))]

    # original
    # ratio = ad["o_neutral_number"] / ad["h_neutral_number"]

    return ratio


def hNeutralNumber(field, ad):
    """
    Return number density of neutral hydrogen in a cell
    THIS IS THE ONE THAT HAS TO CHANGE
    """
    # original
    # mols = ad["h_neutral_mass"] / hydro_mol
    # particles = mols * A

    # correction
    particles = ad["o_neutral_number"] / ad["O/H_metallicity"]

    return particles


def hNeutralMass(field, ad):
    """
    Calculate mass of neutral hydrogen in a cell using number density.
    """
    mols = ad["h_neutral_number"] / A  # number of moles
    grams = mols * hydro_mol

    return grams

# this is where the problem keeps coming up.
# def hIonNumber(field, ad):
#     """
#     Calculate number density of ionized H based on O/H metallicity.
#     GIVES A NUMBER OF PARTICLES, NOT A MASS.
#     """
#     ratio = ad["ion_ratio"]
#     ratio = ratio[(~np.isnan(ratio))]
#     particles = ad["h_neutral_number"] * ratio
#     # particles = particles[(~np.isnan(particles)) & (~np.isinf(particles))]
#
#     return particles
#
#
# def hIonMass(field, ad):
#     """
#     Return mass of all ionized hydrogen.
#     For oxygen, I had to get the mass then the number density; here I can get
#     the number density first, then from that find the mass.
#     """
#     mols = ad["h_ion_number"] / A  # find number of moles
#     grams = mols * hydro_mol  # multiply by number of grams in a mole, get mass
#
#     return grams


if __name__ == "__main__":

        # LOAD DATA
        file = "../Data/4.2.1.density_sap_hdf5_plt_cnt_0200"  # file name
        ds = yt.load(file)  # load data

        ad = ds.all_data()

        # ADD FIELDS
        # add bulk-subtracted velz field
        yt.add_field(
            ("gas", "bulk_subtracted"), units='km/s', function=bulkSub,
            force_override=True)

        # add field for amount (not mass) of ionized oxygen in a cell
        yt.add_field(
            ("gas", "o_ion_mass"), units='g', function=oxyIonMass,
            force_override=True
        )

        yt.add_field(
            ("gas", "o_neutral_mass"), units='g', function=oxyNeutralMass,
            force_override=True
        )

        yt.add_field(
            ("gas", "o_ion_number"), units='dimensionless',
            function=oxyIonNumber, force_override=True
        )

        yt.add_field(
            ("gas", "o_neutral_number"), units='dimensionless',
            function=oxyNeutralNumber, force_override=True
        )

        # add field for total number density of oxygen
        yt.add_field(
            ("gas", "o_total_number"), units='dimensionless',
            function=oxyNumber, force_override=True
        )

        # add field for ratio of ionized to neutral oxygen
        yt.add_field(
            ("gas", "ion_ratio"), units='dimensionless', function=ionRatio,
            force_override=True
        )

        # add field for total mass of hydrogen in a cell
        yt.add_field(
            ("gas", "h_total_mass"), units='g', function=hMass,
            force_override=True
        )

        # add field for total number density of hydrogen
        yt.add_field(
            ("gas", "h_total_number"), units='dimensionless', function=hNumber,
            force_override=True
        )

        # add field for O/H metallicity
        yt.add_field(
            ("gas", "O/H_metallicity"), units='dimensionless',
            function=metallicity, force_override=True
        )

        yt.add_field(
            ("gas", "h_neutral_number"), units='dimensionless',
            function=hNeutralNumber, force_override=True
        )

        # add field for mass of neutral hydrogen
        yt.add_field(
            ("gas", "h_neutral_mass"), units='g', function=hNeutralMass,
            force_override=True
        )

        # # add field for amount (not mass) of ionized hydrogen
        # yt.add_field(
        #     ("gas", "h_ion_number"), units='dimensionless',
        #     function=hIonNumber, force_override=True
        # )

        # # add field for mass of ionized hydrogen
        # yt.add_field(
        #     ("gas", "h_ion_mass"), units='g', function=hIonMass,
        #     force_override=True
        # )

        # VELOCITY CUT
        cut = ad.cut_region(["obj['bulk_subtracted'] <= -50"])
        # unsure of numbers used for this cut.

        # CALCULATIONS
        # this will be dimensionless because it's in solar masses.
        print("Total mass of hydrogen, in solar masses:")
        hMass = sum(cut["h_total_mass"]) / M_sun
        print(hMass, "\n")

        print("Mass of neutral hydrogen, in solar masses:")
        hNeutralMass = sum(cut["h_neutral_mass"]) / M_sun
        print(hNeutralMass, "\n")


        # hIonMass = sum(cut["h_ion_mass"]) / M_sun

        # This gets me a number that doesn't make sense.
        ratio = ad["ion_ratio"]
        ratio = ratio[(~np.isnan(ratio))]
        hneu = ad["h_neutral_number"]  # test
        # hneu = hneu[(~np.isnan(hneu))]  # test
        particles = hneu * ratio
        particles = particles[(~np.isnan(particles))]
        hIonNumber = sum(particles)
        hIonMoles = hIonNumber / A  # divide by Avogadro's number
        hIonMass = hIonMoles * hydro_mol
        hIonMass = hIonMass / M_sun

        print("Mass of ionized hydrogen, in solar masses:")
        print(hIonMass, "\n")

        # # PLOTS
        # plot1 = yt.SlicePlot(
        #     ds, "x", "O/H_metallicity", center="m", data_source=cut
        #     )
        # plot1.save("../Plots/IonizedRatio/OH_metallicity.png")
