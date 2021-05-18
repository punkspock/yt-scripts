"""
Sydney Whilden
08/11/2020

Organize a script that does multiple things into a central file that loads
all the fields I need, and then separate files for each thing I need to do
with those fields.

If you add a YT field definition function, remember to add its corresponding
statement in the addFields() function as well.

"""

import yt
from yt.units.yt_array import YTQuantity
import numpy as np  # used in scripts that import this script
import sys



# CONSTANTS
# Myr75 = "../../Data/4.2.1.density_sap_hdf5_plt_cnt_0075"
# Myr100 = "../../Data/4.2.1.density_sap_hdf5_plt_cnt_0100"
# Myr200 = "../../Data/4.2.1.density_sap_hdf5_plt_cnt_0200"
#
# # TODO: change this to change plot titles in other scripts
# # TODO: change this to be from command line argument passed in scripts
# file = Myr200
# time = "t=200 Myr"

oxy_mol = YTQuantity(15.9994, 'g*mol**-1')  # oxygen molar mass
hydro_mol = YTQuantity(1.00794, 'g*mol**-1')  # correct value is NOT 2.016 g/mol
A = YTQuantity(6.0221413e23, 'mol**-1')  # Avogadro's number
M_sun = YTQuantity(2e33, 'g')  # solar mass
mHydro = YTQuantity(1.6735575e-24, 'g')  # mass of hydrogen atom
mOxy = YTQuantity(2.656e-23, 'g')  # mass of oxygen atom


# FUNCTIONS

def loadData(file):
    # LOAD DATA
    ds = yt.load(file)  # load data
    ad = ds.all_data()

    return ds, ad


def bulkSub(field, ad):
    """

    Set bulk velocity to 150 km/s and subtract bulk velocity from
    the data['flash', 'velz'] field.

    """
    bulk_vel = YTQuantity(150, 'km/s')  # set bulk velocity
    sub = ad['flash', 'velz'].in_units('km/s') - bulk_vel  # subtract bulk velocity
    # why velz and not velx or vely? How do the velocity fields work?

    return sub  # return velz field with bulk velocity subtracted

def cutRegion(ad):
    """

    Do all the cuts in one step.

    """
    cut = ad.cut_region(["(obj['bulk_subtracted'] <= -100) & (obj['product'] != 0)"])

    return cut

# def velocityCut(ad):
#     """
#
#     Perform velocity cut on data set. Exclude anything with a
#     z-direction velocity (I think) greater than -50 km/s.
#
#     """
#     cut = ad.cut_region(["obj['bulk_subtracted'] <= -100"])
#
#     return cut


def badField(field, ad):
    """

    Make a product of all the mass fractions of oxygen ions and hydrogen.

    """
    product = ad['o   '] * ad['o1  '] * ad['o2  '] * ad['o3  '] * ad['o4  '] * \
        ad['o5  '] * ad['o6  '] * ad['o7  '] * ad['o8  '] * ad['h   ']

    return product


# def excludeBads(ad):
#     """
#
#     Exclude cells for which total O = 0, O I = 0, or O II = 0, using a
#     cut region.
#
#     """
#     cut = ad.cut_region(["(obj['product'] != 0.00)"])
#
#     return cut


def oxyMassFraction(field, ad):
    """
    Returns fraction of total mass represented by all oxygen, neutral AND
    ionized at all available levels.
    """
    all = (ad['flash', 'o   '] + ad['flash', 'o1  '] + ad['flash', 'o2  ']
    	+ ad['flash', 'o3  '] + ad['flash', 'o4  '] + ad['flash', 'o5  ']
    	+ ad['flash', 'o6  '] + ad['flash', 'o7  '] + ad['flash', 'o8  ']
	)
    return all


def oxyIonMass(field, ad):
    """
    Returns total cell mass represented by all oxygen ions available.
    """
    all = (ad['flash', 'o1  '] + ad['flash', 'o5  '] + ad['flash', 'o2  ']
        + ad['flash', 'o3  '] + ad['flash', 'o4  '] + ad['flash', 'o6  ']
        + ad['flash', 'o7  '] + ad['flash', 'o8  ']  # a fraction
        )
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
    particles = mols * A / ad["cell_volume"]  # multiply by Avogadro's number

    return particles


def oxyNeutralNumber(field, ad):
    """
    Returns number density of neutral oxygen in cell
    """
    mols = ad["o_neutral_mass"] / oxy_mol  # divide by grams in a mole of O
    particles = mols * A / ad["cell_volume"] # multiply by Avogadro's number

    return particles


def oxyNumber(field, ad):
    """
    Returns number density of oxygen in a cell by adding the respective
    number densities of neutral and ionized oxygen.
    """
    number = ad["o_ion_number"] + ad["o_neutral_number"]

    return number


def o6mass(field, ad):
    """

    Returns the mass of O VI in a cell by multiplying the fraction of that
    cell's mass represented by O VI by the density and volume of the cell.

    """
    mass = ad["flash", "o5  "] * ad["density"] * ad["cell_volume"]

    return mass


def o6number(field, ad):
    """

    Returns number density of O VI in a cell by dividing the mass by
    molar weight of oxygen and then multiplying by Avogadro's number.

    """
    mols = ad["OVI_mass"] / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


def oIonFraction(field, ad):
    """

    Returns the ratio of the numbers of ionized to neutral oxygen.

    """
    fraction = ad["o_ion_number"] / ad["o_total_number"]

    return fraction


def oNeutralFraction(field, ad):
    """
    Returns the ratio of number densities of neutral oxygen to total oxygen.

    """
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
    # mols = ad["h_total_mass"] / hydro_mol
    # particles = mols * A / ad["cell_volume"]
    particles = ad['h   '] * ad['density'] * A / hydro_mol  # test

    return particles


def hIonNumber(field, ad):
    """

    Returns the number density of neutral hydrogen atoms in a cell. g cm**-3

    """

    number = (ad["h_total_number"] * ad["o_ion_fraction"])

    return number


def hIonMass(field, ad):
    """

    Returns mass of ionized hydrogen by dividing number density of
    ionized hydrogen by Avogadro's number to get number of moles and then
    multiplying by the molar mass of hydrogen to get a mass.

    """
    mols = ad["h_ion_number"] * ad["cell_volume"] / A
    grams = mols * hydro_mol  # multiply by grams/mole for hydrogen

    return grams


def hNeutralNumber(field, ad):
    """

    Returns number density of H I by multiplying total number density of
    hydrogen by the fraction of oxygen that is ionized. g cm**-3

    """
    # don't need to divide by cell volume because already did in making of
    number = ad["h_total_number"] * ad["o_neutral_fraction"]

    return number


def hNeutralMass(field, ad):
    """

    Returns mass of H I by dividing number density by Avogadro's
    number to get # of moles and then multiplying that by molar
    mass of hydrogen.

    """
    mols = ad["h_neutral_number"] * ad["cell_volume"] / A
    grams = mols * hydro_mol

    return grams


def h1MassFraction(field, ad):
    """

    Return fraction of total cell mass represented by H I.

    """
    cell_mass = ad["density"] * ad["cell_volume"]
    fraction = ad["h_neutral_mass"] / cell_mass

    return fraction


def ionFraction(field, ad):  # don't think this is used anywhere
    """

    Return fraction of O VI over O.

    """
    frac = ad["OVI_number"] / ad["o_total_number"]

    return frac


def testField(field, ad):
    # testing something out
    particles = ad['h   '] * A / hydro_mol * ad['density']

    return particles


def hCell(field, ad):
    """

    Calculate total number of hydrogen atoms in a cell.

    """
    atoms = ad['h_total_number'] * ad['cell_volume']

    return atoms


# def fracAmbient(field, ad):
#     """
#
#     Calculates fraction of material in a given cell post-mixing
#     that initially came from ambient material.
#
#     """
#     A = ad["o_total_number"] / ad["h_total_number"]  # abundance
#     Ac = 0.001  # initial setting for abundance of cloud material
#     Aa = 1.00  # initial setting for abundance of ambient material
#     fa = (Ac - A) / (Ac - Aa)  # ambient fraction
#
#     return fa
#
#
# def fracCloud(field, ad):
#     """
#
#     Based on fact that fraction ambient and fraction cloud
#     must sum to one.
#
#     """
#     fc = 1 - ad["ambient_fraction"]
#
#     return fc
#
#
# def newAbundance(field, ad):
#     """
#
#     Set new abundance parameters
#
#     """
#     AcNew = 0.5  # dummy value
#     AaNew = 0.5  # dummy value
#
#     ANew = AcNew*ad["ambient_fraction"] + AaNew*ad["cloud_fraction"]
#
#     return ANew
#
#
# def changeFactor(field, ad):
#     """
#
#     A'/A
#
#     """
#     A = ad["o_total_number"] / ad["h_total_number"]
#     factor = ad["new_abundance"] / A
#
#     return factor


def scale(field, ad):
    """
    Returns scaling factor as an array.
    """
    metal = ad["o_total_number"] / ad["h_total_number"]
    A = (1 / metal) * (10**-4.31)  # divide theirs by ours

    return A


def addFields():
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
        ("gas", "o_ion_number"), units='cm**-3',
        function=oxyIonNumber, force_override=True
    )

    yt.add_field(
        ("gas", "o_neutral_number"), units='cm**-3',
        function=oxyNeutralNumber, force_override=True
    )

    # add field for total number density of oxygen
    yt.add_field(
        ("gas", "o_total_number"), units='cm**-3',
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
        ("gas", "h_total_number"), units='cm**-3', function=hNumber,
        force_override=True
    )

    yt.add_field(
        ("gas", "h_ion_number"), units='cm**-3',
        function=hIonNumber, force_override=True
    )

    yt.add_field(
        ("gas", "h_ion_mass"), units='g', function=hIonMass,
        force_override=True
    )

    yt.add_field(
        ("gas", "h_neutral_number"), units='cm**-3',
        function=hNeutralNumber, force_override=True
    )

    yt.add_field(
        ("gas", "h_neutral_mass"), units='g',
        function=hNeutralMass, force_override=True
    )

    yt.add_field(
        ("gas", "OVI_mass"), units='g', function=o6mass,
        force_override=True
    )

    yt.add_field(
        ("gas", "OVI_number"), units='cm**-3', function=o6number,
        force_override=True
    )

    yt.add_field(
        ("gas", "h1  "), units='dimensionless', function=h1MassFraction,
        force_override=True
    )

    yt.add_field(
        ("gas", "t_o"), units='dimensionless', function=oxyMassFraction,
        force_override=True
    )

    yt.add_field(
        ("gas", "OVI/O"), units='dimensionless', function=ionFraction,
        force_override=True
    )

    # yt.add_field(
    #     ("ambient_fraction"), units="dimensionless", function=fracAmbient,
    #     force_override=True
    # )
    #
    # yt.add_field(
    #     ("cloud_fraction"), units="dimensionless", function=fracCloud,
    #     force_override=True
    # )
    #
    # yt.add_field(
    #     ("new_abundance"), units="dimensionless", function=newAbundance,
    #     force_override=True
    # )
    #
    # yt.add_field(
    #     ("change_factor"), units="dimensionless", function=changeFactor,
    #     force_override=True
    # )

    # add field to scale the metallicity
    yt.add_field(
        ("gas", "scale"), units='dimensionless', function=scale,
        force_override=True
    )

    yt.add_field(
        ("gas", "product"), units='dimensionless', function=badField,
        force_override=True
    )

    yt.add_field(
        ("gas", "test_field"), units="cm**-3", function=testField,
        force_override=True
    )

    yt.add_field(
        ("gas", "h_cell_number"), units="dimensionless", function=hCell,
        force_override=True
    )

    return


def main(epoch):

    file = ""  # initialize

    if epoch == '75':
        file = "../../Data/4.2.1.density_sap_hdf5_plt_cnt_0075"
    elif epoch == '100':
        file = "../../Data/4.2.1.density_sap_hdf5_plt_cnt_0100"
    elif epoch == '200':
        file = "../../Data/4.2.1.density_sap_hdf5_plt_cnt_0200"
    else:
        print("Invalid argument for epoch.")

    time = "t=%s Myr" % epoch

    ds, ad = loadData(file)  # load the file in YT
    addFields()  # add all the fields
    # cut = velocityCut(ad)  # do velocity cut
    # cut = excludeBads(cut)  # get rid of bad cells in the domain
    cut = cutRegion(ad)

    return file, time, ds, ad, cut


if __name__ == "__main__":

    epoch = ""  # initialize

    if len(sys.argv[1]) > 1:
        epoch = str(sys.argv[1])
    else:
        epoch = '75'
        print("Running with default epoch.")
    # get epoch as command line argument

    file, time, ds, ad, cut = main(epoch)
