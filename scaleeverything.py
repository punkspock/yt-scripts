"""
Get the number density of all available O ions and then scale them all for
export to other script.
"""

import OH_fields as oh
import sys

# get number densities

# the one for neutral oxygen is in OH_fields.py
oxy_mol = oh.oxy_mol  # taking care of a bug
A = oh.A

def o1Number(field, ad):  # OI
    mass = ad["flash", "o   "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


def o2Number(field, ad):  # OII
    mass = ad["flash", "o1  "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


def o3Number(field, ad):  # OIII
    mass = ad['flash', 'o2  '] * ad['density'] * ad['cell_volume']
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


def o4Number(field, ad):  # OIV
    mass = ad["flash", "o3  "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


def o5Number(field, ad):  # OV
    mass = ad["flash", "o4  "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


# OVI number already made in OH_fields.py


def o7Number(field, ad):  # OVII
    mass = ad["flash", "o6  "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


def o8Number(field, ad):  # OVIII
    mass = ad["flash", "o7  "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


def o9Number(field, ad):  # OIX
    mass = ad["flash", "o8  "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


# scale them
def scaledO1(field, ad):
    scaled = ad['OI_number'] * ad['scale']

    return scaled


def scaledO2(field, ad):
    scaled = ad['OII_number'] * ad['scale']

    return scaled


def scaledO3(field, ad):
    scaled = ad['OIII_number'] * ad['scale']

    return scaled


def scaledO4(field, ad):
    scaled = ad['OIV_number'] * ad['scale']

    return scaled


def scaledO5(field, ad):
    scaled = ad['OV_number'] * ad['scale']

    return scaled


def scaledO6(field, ad):
    scaled = ad['OVI_number'] * ad['scale']

    return scaled


def scaledO7(field, ad):
    scaled = ad['OVII_number'] * ad['scale']

    return scaled


def scaledO8(field, ad):
    scaled = ad['OVIII_number'] * ad['scale']

    return scaled


def scaledO9(field, ad):
    scaled = ad['OIX_number'] * ad['scale']

    return scaled


def scaledAllO(field, ad):
    scaled = ad['o_total_number'] * ad['scale']

    return scaled


def addFields():

    oh.yt.add_field(
        ('gas', 'OI_number'), units='cm**-3', function=o1Number,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OII_number'), units='cm**-3', function=o2Number,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OIII_number'), units='cm**-3', function=o3Number,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OIV_number'), units='cm**-3', function=o4Number,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OV_number'), units='cm**-3', function=o5Number,
        force_override=True
        )

    # O VI number already exists in OH_fields.py

    oh.yt.add_field(
        ('gas', 'OVII_number'), units='cm**-3', function=o7Number,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OVIII_number'), units='cm**-3', function=o8Number,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OIX_number'), units='cm**-3', function=o9Number,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OI_scaled'), units='cm**-3', function=scaledO1,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OII_scaled'), units='cm**-3', function=scaledO2,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OIII_scaled'), units='cm**-3', function=scaledO3,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OIV_scaled'), units='cm**-3', function=scaledO4,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OV_scaled'), units='cm**-3', function=scaledO5,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OVI_scaled'), units='cm**-3', function=scaledO6,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OVII_scaled'), units='cm**-3', function=scaledO7,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OVIII_scaled'), units='cm**-3', function=scaledO8,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'OIX_scaled'), units='cm**-3', function=scaledO9,
        force_override=True
        )

    oh.yt.add_field(
        ('gas', 'o_total_scaled'), units='cm**-3', function=scaledAllO,
        force_override=True
        )

    return


def main():
    addFields()
    return


if __name__ == "__main__":
        epoch = ""  # initialize

        if len(sys.argv[1]) > 1:  # take command line argument
            epoch = sys.argv[1]

        # run main function from OH_fields.py
        file, time, ds, ad, cut = oh.main(epoch)

        main()
