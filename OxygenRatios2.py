# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 16:46:15 2020

@author: egoet
"""

import numpy as np
import yt
from yt import YTQuantity

#Load data from file
ds = yt.load("4.2.1.density_sap_hdf5_plt_cnt_0075", unit_system="cgs")
ad = ds.all_data()

#Define constants
N_A = 6.0221413e+23
molm_oxy = 15.9994
molm_oxy = YTQuantity(molm_oxy,'g/mol')
c_o = 1/molm_oxy

mass_h = 1.6735575e-24
mass_h = YTQuantity(mass_h, 'g')
molm_h = 1.00794
molm_h = YTQuantity(molm_h,'g/mol')
c_h = 1/molm_h

mass_he = 6.6464731e-24
mass_he = YTQuantity(mass_he, 'g')
molm_he = 4.002602
molm_he = YTQuantity(molm_he,'g/mol')
c_he = 1/molm_he

A_O_max = 8.51e-4


#Add velocity cut
def cl_velz_150(field,data):
	bulk_vel = YTQuantity(150e5, 'cm/s')
	return data['flash','velz'].in_units('cm/s')-bulk_vel
yt.add_field(("gas", "cl_velz_150"), units="cm/s", function=cl_velz_150,force_override=True)

#Add fields for metallicity calculations

#Fields for calculations in mols
def oxygen_mol(field,data):
    sum_xn = data['flash','o   '] + data['flash','o1  '] + data['flash','o2  '] + data['flash','o3  '] + data['flash','o4  '] + data['flash','o5  '] + data['flash','o6  '] + data['flash','o7  '] + data['flash','o8  ']
    return c_o*sum_xn*data['flash','dens'].in_units('g/cm**3')*N_A*data['gas','cell_volume'].in_units('cm**3')
yt.add_field(("gas", "O_mols"), units="mol", function=oxygen_mol, force_override=True)

def oxygen1_mol(field, data):
    return c_o*data['flash', 'o1  ']*data['flash','dens'].in_units('g/cm**3')*N_A*data['gas','cell_volume'].in_units('cm**3')
yt.add_field(("gas", "O1_mols"), units="mol", function=oxygen1_mol, force_override=True)

def oxygen2_mol(field, data):
    return c_o*data['flash', 'o2  ']*data['flash','dens'].in_units('g/cm**3')*N_A*data['gas','cell_volume'].in_units('cm**3')
yt.add_field(("gas", "O2_mols"), units="mol", function=oxygen2_mol, force_override=True)

def oxygen3_mol(field, data):
    return c_o*data['flash', 'o3  ']*data['flash','dens'].in_units('g/cm**3')*N_A*data['gas','cell_volume'].in_units('cm**3')
yt.add_field(("gas", "O3_mols"), units="mol", function=oxygen3_mol, force_override=True)

def oxygen4_mol(field, data):
    return c_o*data['flash', 'o4  ']*data['flash','dens'].in_units('g/cm**3')*N_A*data['gas','cell_volume'].in_units('cm**3')
yt.add_field(("gas", "O4_mols"), units="mol", function=oxygen4_mol, force_override=True)

def oxygen5_mol(field, data):
    return c_o*data['flash', 'o5  ']*data['flash','dens'].in_units('g/cm**3')*N_A*data['gas','cell_volume'].in_units('cm**3')
yt.add_field(("gas", "O5_mols"), units="mol", function=oxygen5_mol, force_override=True)

def oxygen6_mol(field, data):
    return c_o*data['flash', 'o6  ']*data['flash','dens'].in_units('g/cm**3')*N_A*data['gas','cell_volume'].in_units('cm**3')
yt.add_field(("gas", "O6_mols"), units="mol", function=oxygen6_mol, force_override=True)

def oxygen7_mol(field, data):
    return c_o*data['flash', 'o7  ']*data['flash','dens'].in_units('g/cm**3')*N_A*data['gas','cell_volume'].in_units('cm**3')
yt.add_field(("gas", "O7_mols"), units="mol", function=oxygen7_mol, force_override=True)

def hydrogen_mol(field,data):
    return data['gas', 'H_nuclei_density']*data['gas', 'cell_volume']*mass_h*c_h*N_A
yt.add_field(('gas', 'H_mols'), units="mol", function=hydrogen_mol, force_override=True)

def helium_mol(field, data):
    return data['gas', 'He_nuclei_density']*data['gas', 'cell_volume']*mass_h*c_h*N_A
yt.add_field(('gas', 'He_mols'), units="mol", function=helium_mol,force_override=True)

def stuff_mol(field, data):
    return data['gas', 'H_mols'] + data['gas', 'He_mols']
yt.add_field(('gas', 'stuff_mols'), units="mol", function=stuff_mol,force_override=True)

def metallicity_mol(field, data):
    return data['gas', 'O_mols']/data['gas', 'stuff_mols']
yt.add_field(('gas', 'metallicity_mol'), function=metallicity_mol, force_override=True)

def metallicity_O7_mol(field, data):
    return data['gas', 'O7_mols']/data['gas', 'stuff_mols']
yt.add_field(('gas', 'metallicity_O7_mol'), function=metallicity_O7_mol, force_override=True)


#Fields for calculations with grams
def oxygen_g(field, data):
    return data['gas', 'O_mols']*molm_oxy
yt.add_field(('gas', 'O_g'), units="g", function=oxygen_g, force_override=True)

def oxygen1_g(field, data):
    return data['gas', 'O1_mols']*molm_oxy
yt.add_field(('gas', 'O1_g'), units="g", function=oxygen1_g, force_override=True)

def oxygen2_g(field, data):
    return data['gas', 'O2_mols']*molm_oxy
yt.add_field(('gas', 'O2_g'), units="g", function=oxygen2_g, force_override=True)

def oxygen3_g(field, data):
    return data['gas', 'O3_mols']*molm_oxy
yt.add_field(('gas', 'O3_g'), units="g", function=oxygen3_g, force_override=True)

def oxygen4_g(field, data):
    return data['gas', 'O4_mols']*molm_oxy
yt.add_field(('gas', 'O4_g'), units="g", function=oxygen4_g, force_override=True)

def oxygen5_g(field, data):
    return data['gas', 'O5_mols']*molm_oxy
yt.add_field(('gas', 'O5_g'), units="g", function=oxygen5_g, force_override=True)

def oxygen6_g(field, data):
    return data['gas', 'O6_mols']*molm_oxy
yt.add_field(('gas', 'O6_g'), units="g", function=oxygen6_g, force_override=True)

def oxygen7_g(field, data):
    return data['gas', 'O7_mols']*molm_oxy
yt.add_field(('gas', 'O7_g'), units="g", function=oxygen7_g, force_override=True)

def hydrogen_g(field, data):
    return data['gas', 'H_mols']*molm_h
yt.add_field(('gas', 'H_g'), units="g", function=hydrogen_g, force_override=True)

def helium_g(field, data):
    return data['gas', 'He_mols']*molm_he
yt.add_field(('gas', 'He_g'), units="g", function=helium_g, force_override=True)

def stuff_g(field, data):
    return data['gas', 'H_g'] + data['gas', 'He_g']
yt.add_field(('gas', 'stuff_g'), units="g", function=stuff_g, force_override=True)

def metallicity_g(field, data):
    return data['gas', 'O_g']/data['gas', 'stuff_g']
yt.add_field(('gas', 'metallicity_g'), function=metallicity_g, force_override=True)

def metallicity_O1_g(field, data):
    return data['gas', 'O1_g']/data['gas', 'stuff_g']
yt.add_field(('gas', 'metallicity_O1_g'), function=metallicity_O1_g, force_override=True)

def metallicity_O2_g(field, data):
    return data['gas', 'O2_g']/data['gas', 'stuff_g']
yt.add_field(('gas', 'metallicity_O2_g'), function=metallicity_O2_g, force_override=True)

def metallicity_O3_g(field, data):
    return data['gas', 'O3_g']/data['gas', 'stuff_g']
yt.add_field(('gas', 'metallicity_O3_g'), function=metallicity_O3_g, force_override=True)

def metallicity_O4_g(field, data):
    return data['gas', 'O4_g']/data['gas', 'stuff_g']
yt.add_field(('gas', 'metallicity_O4_g'), function=metallicity_O4_g, force_override=True)

def metallicity_O5_g(field, data):
    return data['gas', 'O5_g']/data['gas', 'stuff_g']
yt.add_field(('gas', 'metallicity_O5_g'), function=metallicity_O5_g, force_override=True)

def metallicity_O6_g(field, data):
    return data['gas', 'O6_g']/data['gas', 'stuff_g']
yt.add_field(('gas', 'metallicity_O6_g'), function=metallicity_O6_g, force_override=True)

def metallicity_O7_g(field, data):
    return data['gas', 'O7_g']/data['gas', 'stuff_g']
yt.add_field(('gas', 'metallicity_O7_g'), function=metallicity_O7_g, force_override=True)

#Check fields
#print(ds.field_list)
#print(ds.derived_field_list)


#Apply velocity cut
cut = ad.cut_region(["(obj['cl_velz_150'] <= -100e5)"])

#Sum all ions of oxygen
sum_xn = cut['flash','o   '] + cut['flash','o1  '] + cut['flash','o2  '] + cut['flash','o3  '] + cut['flash','o4  '] + cut['flash','o5  '] + cut['flash','o6  '] + cut['flash','o7  '] + cut['flash','o8  ']


#For each oxygen ion, determine the abundance of that ion per cell
#Then, divide by the abundance of hydrogen
metallicity = []
for k in range(9):
    if k == 0:
        fieldstr = 'o   '
    else:
        fieldstr = 'o' + str(k) + '  '
    metallicity.append(cut['flash', fieldstr])
metallicity.append(sum_xn)

h = cut['flash', 'h   ']

metallicity = metallicity/h

#For each oxygen ion, determine the number of mols of that ion per cell
#Then, divide by the number of mols of hydrogen + helium

#Not needed because everything has been defined as a field
'''
N_oxy = []
for i in range(9):
    if i == 0:
      fieldstr = 'o   '
    else:
      fieldstr = 'o' + str(i) + '  '
    N_oxy.append(c_o*cut['flash',fieldstr]*cut['flash','dens'].in_units('g/cm**3')*N_A*cut['gas','cell_volume'].in_units('cm**3'))

N_oxy.append(c_o*sum_xn*cut['flash','dens'].in_units('g/cm**3')*N_A*cut['gas','cell_volume'].in_units('cm**3'))

#N_h_1 = c_h*cut['flash','h   ']*cut['flash','dens'].in_units('g/cm**3')*N_A*cut['gas','cell_volume'].in_units('cm**3')
#print(N_h_1)

N_h_2 = cut['gas', 'H_nuclei_density']*cut['gas', 'cell_volume']*mass_h*c_h*N_A
#print(N_h_2)

N_he = cut['gas', 'He_nuclei_density']*cut['gas', 'cell_volume']*mass_he*c_he*N_A
#print(N_h_2)

N_stuff = N_h_2 + N_he

metallicity_mols = N_oxy/N_stuff

'''
#For each oxygen ion, determine the number of grams of that ion per cell
#Then, divide by the number of grams of hydrogen + helium
#Not needed because everything has been defined as a field
'''
N_oxy_g = N_oxy*molm_oxy
N_h_g = N_h_2*molm_h
N_he_g = N_he*molm_he

N_stuff_g = N_h_g + N_he_g

metallicity_mass = N_oxy_g/N_stuff_g
'''

#Make plots

#Projection plots

#Projections in x direction with velocity cut
'''
proj_cut = yt.ProjectionPlot(ds, 'x', "metallicity_g", data_source=cut)
proj_cut.save("Projection_Metallicity_g.png")

proj_cut5 = yt.ProjectionPlot(ds, 'x', "metallicity_O5_g", data_source=cut)
proj_cut5.save("Projection_Metallicity_O5_g.png")
'''
#Projection in x direction without velocity cut
proj_nocut3 = yt.ProjectionPlot(ds, 'x', "metallicity_O3_g")
proj_nocut3.save("Projection_Metallicity_O3_g_nocut.png")

proj_nocut5 = yt.ProjectionPlot(ds, 'x', "metallicity_O5_g")
proj_nocut5.save("Projection_Metallicity_O5_g_nocut.png")

proj_nocut7 = yt.ProjectionPlot(ds, 'x', "metallicity_O7_g")
proj_nocut7.save("Projection_Metallicity_O7_g_nocut.png")

#Slice plots
'''
#Slices in x with velocity cut
slice_cutx = yt.SlicePlot(ds, 'x', "metallicity_g", center="m", data_source=cut)
slice_cutx.save("Slice_Metallicity_g.png")

slice_cutx3 = yt.SlicePlot(ds, 'x', "metallicity_O3_g", center="m", data_source=cut)
slice_cutx3.save("Slice_Metallicity_O3_g.png")

slice_cutx7 = yt.SlicePlot(ds, 'x', "metallicity_O7_g", center="m", data_source=cut)
slice_cutx7.save("Slice_Metallicity_O7_g.png")

#Slices in y with velocity cut
slice_cuty = yt.SlicePlot(ds, 'y', "metallicity_g", center="m", data_source=cut)
slice_cuty.save("Slice_Metallicity_g_y.png")

slice_cuty3 = yt.SlicePlot(ds, 'y', "metallicity_O3_g", center="m", data_source=cut)
slice_cuty3.save("Slice_Metallicity_O3_g_y.png")

slice_cuty7 = yt.SlicePlot(ds, 'y', "metallicity_O7_g", center="m", data_source=cut)
slice_cuty7.save("Slice_Metallicity_O7_g_y.png")


#Slices in x without velocity cut
slice_nocut = yt.SlicePlot(ds, 'x', "metallicity_g", center="m")
slice_nocut.save("Slice_Metallicity_g_x_nocut.png")

slice_nocut1 = yt.SlicePlot(ds, 'x', "metallicity_O1_g", center="m")
slice_nocut1.save("Slice_Metallicity_O1_g_x_nocut.png")

slice_nocut2 = yt.SlicePlot(ds, 'x', "metallicity_O2_g", center="m")
slice_nocut2.save("Slice_Metallicity_O2_g_x_nocut.png")

slice_nocut3 = yt.SlicePlot(ds, 'x', "metallicity_O3_g", center="m")
slice_nocut3.save("Slice_Metallicity_O3_g_x_nocut.png")

slice_nocut4 = yt.SlicePlot(ds, 'x', "metallicity_O4_g", center="m")
slice_nocut4.save("Slice_Metallicity_O4_g_x_nocut.png")

slice_nocut5 = yt.SlicePlot(ds, 'x', "metallicity_O5_g", center="m")
slice_nocut5.save("Slice_Metallicity_O5_g_x_nocut.png")

slice_nocut6 = yt.SlicePlot(ds, 'x', "metallicity_O6_g", center="m")
slice_nocut6.save("Slice_Metallicity_O6_g_x_nocut.png")

slice_nocut7 = yt.SlicePlot(ds, 'x', "metallicity_O7_g", center="m")
slice_nocut7.save("Slice_Metallicity_O7_g_x_nocut.png")

'''
