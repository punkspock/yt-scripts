# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:28:47 2020

@author: egoet
"""


import numpy as np
import yt
import matplotlib
matplotlib.use('Agg')
from yt import YTQuantity
import matplotlib.pyplot as plt

#Load data from file
ds = yt.load("4.2.1.density_sap_hdf5_plt_cnt_0200", unit_system="cgs")
ad = ds.all_data()

#Define constants
N_A = 6.0221413e+23
N_A = YTQuantity(N_A, '1/mol')
molm_oxy = 15.9994
molm_oxy = YTQuantity(molm_oxy,'g/mol')
c_o = 1/molm_oxy

mass_h = 1.6735575e-24
mass_h = YTQuantity(mass_h, 'g')
molm_h = 1.00794
molm_h = YTQuantity(molm_h,'g/mol')
c_h = 1/molm_h

mass_sun = YTQuantity(1.989e33, 'g')


def cl_velz_150(field,data):
	bulk_vel = YTQuantity(150e5, 'cm/s')
	return data['flash','velz'].in_units('cm/s')-bulk_vel
yt.add_field(("gas", "cl_velz_150"), units="cm/s", function=cl_velz_150,force_override=True)

def oxygen_ions(field,data):
    return data['flash','o1  '] + data['flash','o2  '] + data['flash', 'o3  '] + data['flash','o4  '] + data['flash','o5  '] + data['flash','o6  '] + data['flash','o7  '] + data['flash','o8  ']
yt.add_field(("gas", "o_ions"), function=oxygen_ions, force_override=True)

def total_oxygen(field,data):
    return data['flash','o   '] + data['flash','o1  '] + data['flash','o2  '] + data['flash', 'o3  '] + data['flash','o4  '] + data['flash','o5  '] + data['flash','o6  '] + data['flash','o7  '] + data['flash','o8  ']
yt.add_field(("gas", "t_o"), function=total_oxygen, force_override=True)

def neutral_h(field, data):
    return data['flash', 'o   ']*data['flash', 'h   ']/data['gas', 't_o']
yt.add_field(('gas', 'h1  '), function=neutral_h, force_override=True)

def ionized_h(field, data):
    return data['flash', 'h   '] - data['gas', 'h1  ']
yt.add_field(('gas', 'h2  '), function=ionized_h, force_override=True)

def h_mass(field, data):
    return data['h   ']*data['density']*data['cell_volume']
yt.add_field(('gas', 'h_mass'), units='g', function=h_mass, force_override=True)

def h1_mass(field, data):
    return data['h1  ']*data['density']*data['cell_volume']
yt.add_field(('gas', 'h1_mass'), units='g', function=h1_mass, force_override=True)

def h2_mass(field, data):
    return data['h2  ']*data['density']*data['cell_volume']
yt.add_field(('gas', 'h2_mass'), units='g', function=h2_mass, force_override=True)

#Apply velocity cut

cut2 = ad.cut_region(["(obj['cl_velz_150'] <= -100e5)"])

cut_temp = ad.cut_region(["(obj['cl_velz_150'] <= -100e5) & (obj['temperature'] <= 1e4)"])

cut_temp2 = ad.cut_region(["(obj['cl_velz_150'] <= -100e5) & (obj['temperature'] >= 1e4)"])


#Calculate mass of neutral and ionized hydrogen in solar masses
#Using temperature cut
h1_mass = sum(cut_temp['h_mass'])/mass_sun
h2_mass = sum(cut_temp2['h_mass'])/mass_sun
h_tot = h1_mass + h2_mass

#Calculate mass of neutral and ionized hydrogen in solar masses
#Using ratio of ionized oxygen to distinguish hydrogen
h1_mass_r = sum(cut2['h1_mass'])/mass_sun
h2_mass_r = sum(cut2['h1_mass'])/mass_sun
h_tot_r = h1_mass_r + h2_mass_r
