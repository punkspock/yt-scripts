"""
Sydney Whilden
08/10/2020

This one works better than ionizedratio.py. Will consolidate them.

NOTE: This script is a dependency for metallicity1.py
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


def oIonFraction(field, ad):
    fraction = ad["o_ion_number"] / ad["o_total_number"]

    return fraction


def oNeutralFraction(field, ad):
    fraction = ad["o_neutral_number"] / ad["o_total_number"]

    return fraction


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


def hIonNumber(field, ad):
    number = ad["h_total_number"] * ad["o_ion_fraction"]

    return number


def hIonMass(field, ad):
    mols = ad["h_ion_number"] / A  # divide by Avogadro's number
    grams = mols * hydro_mol  # multiply by grams/mole for hydrogen

    return grams


def hNeutralNumber(field, ad):
    number = ad["h_total_number"] * ad["o_neutral_fraction"]

    return number


def hNeutralMass(field, ad):
    mols = ad["h_neutral_number"] / A
    grams = mols * hydro_mol

    return grams


def add_fields():
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

    # add field for fraction of ionized oxygen (of total)
    yt.add_field(
        ("gas", "o_ion_fraction"), units='dimensionless',
        function=oIonFraction, force_override=True
    )

    # add field for fraction of total oxygen that is neutral
    yt.add_field(
        ("gas", "o_neutral_fraction"), units='dimensionless',
        function=oNeutralFraction, force_override=True
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

    yt.add_field(
        ("gas", "h_ion_number"), units='dimensionless',
        function=hIonNumber, force_override=True
    )

    yt.add_field(
        ("gas", "h_ion_mass"), units='g', function=hIonMass,
        force_override=True
    )

    yt.add_field(
        ("gas", "h_neutral_number"), units='dimensionless',
        function=hNeutralNumber, force_override=True
    )

    yt.add_field(
        ("gas", "h_neutral_mass"), units='g',
        function=hNeutralMass, force_override=True
    )

    return


if __name__ == "__main__":

        # LOAD DATA
        file = "../Data/4.2.1.density_sap_hdf5_plt_cnt_0200"  # file name
        ds = yt.load(file)  # load data

        ad = ds.all_data()

        # add all the fields at once
        add_fields()

        # VELOCITY CUT
        cut = ad.cut_region(["obj['bulk_subtracted'] <= -50"])

        hIonMass = sum(cut["h_ion_mass"]) / M_sun
        print("Mass of ionized hydrogen: ", hIonMass)

        hNeutralMass = sum(cut["h_neutral_mass"]) / M_sun
        print("Mass of neutral hydrogen: ", hNeutralMass)

        hTotalMass = sum(cut["h_total_mass"]) / M_sun
        print("Total hydrogen mass: ", hTotalMass)
