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

def o1Number(field, ad):
    mass = ad["flash", "o   "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


def o2Number(field, ad):
    mass = ad["flash", "o1  "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


def o3Number(field, ad):
    mass = ad["flash", "o2  "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


def o4Number(field, ad):
    mass = ad["flash", "o3  "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


def o5Number(field, ad):
    mass = ad["flash", "o4  "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


# OVI number already made in OH_fields.py


def o7Number(field, ad):
    mass = ad["flash", "o6  "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


def o8Number(field, ad):
    mass = ad["flash", "o7  "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


def o9Number(field, ad):
    mass = ad["flash", "o8  "] * ad["density"] * ad["cell_volume"]
    mols = mass / oxy_mol
    particles = mols * A / ad["cell_volume"]

    return particles


# scale them
def scaled_o1(field, ad):
    scaled = ad['OI_number'] * ad['scale']

    return scaled


def scaled_o2(field, ad):
    scaled = ad['OII_number'] * ad['scale']

    return scaled


def scaled_o3(field, ad):
    scaled = ad['OIII_number'] * ad['scale']

    return scaled


def scaled_o4(field, ad):
    scaled = ad['OIV_number'] * ad['scale']

    return scaled


def scaled_o5(field, ad):
    scaled = ad['OV_number'] * ad['scale']

    return scaled


def scaled_o6(field, ad):
    scaled = ad['OVI_number'] * ad['scale']

    return scaled


def scaled_o7(field, ad):
    scaled = ad['OVII_number'] * ad['scale']

    return scaled


def scaled_o8(field, ad):
    scaled = ad['OVIII_number'] * ad['scale']

    return scaled


def scaled_o9(field, ad):
    scaled = ad['OIX_number'] * ad['scale']

    return scaled


def addFields():

    oh.yt.add_field(
        ('gas', 'OI_number'), units='cm**-3', function=o1Number
    )

    oh.yt.add_field(
        ('gas', 'OII_number'), units='cm**-3', function=o2Number
    )

    oh.yt.add_field(
        ('gas', 'OIII_number'), units='cm**-3', function=o3Number
    )

    oh.yt.add_field(
        ('gas', 'OIV_number'), units='cm**-3', function=o3Number
    )

    oh.yt.add_field(
        ('gas', 'OV_number'), units='cm**-3', function=o3Number
    )

    oh.yt.add_field(
        ('gas', 'OVII_number'), units='cm**-3', function=o3Number
    )

    oh.yt.add_field(
        ('gas', 'OVIII_number'), units='cm**-3', function=o3Number
    )

    oh.yt.add_field(
        ('gas', 'OIX_number'), units='cm**-3', function=o3Number
    )

    oh.yt.add_field(
        ('gas', 'OI_scaled'), units='cm**-3', function=scaled_o1
    )

    oh.yt.add_field(
        ('gas', 'OII_scaled'), units='cm**-3', function=scaled_o2
    )

    oh.yt.add_field(
        ('gas', 'OIII_scaled'), units='cm**-3', function=scaled_o3
    )

    oh.yt.add_field(
        ('gas', 'OIV_scaled'), units='cm**-3', function=scaled_o4
    )

    oh.yt.add_field(
        ('gas', 'OV_scaled'), units='cm**-3', function=scaled_o5
    )

    oh.yt.add_field(
        ('gas', 'OVI_scaled'), units='cm**-3', function=scaled_o6
    )

    oh.yt.add_field(
        ('gas', 'OVII_scaled'), units='cm**-3', function=scaled_o7
    )

    oh.yt.add_field(
        ('gas', 'OVIII_scaled'), units='cm**-3', function=scaled_o8
    )

    oh.yt.add_field(
        ('gas', 'OIX_scaled'), units='cm**-3', function=scaled_o9
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
