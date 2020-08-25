# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:15:58 2020

@author: egoet
"""


import numpy as np
import yt
import matplotlib
from yt import YTQuantity

#Load data from file
ds = yt.load("4.2.1.density_sap_hdf5_plt_cnt_0200", unit_system="cgs")
ad = ds.all_data()

#Define constants
N_A = 6.023e+23
N_A = YTQuantity(N_A, '1/mol')
molm_oxy = 15.9994
molm_oxy = YTQuantity(molm_oxy,'g/mol')
c_o = 1/molm_oxy

mass_h = 1.6735575e-24
mass_h = YTQuantity(mass_h, 'g')
molm_h = 1.00784  # THIS ISN'T RIGHT
molm_h = YTQuantity(molm_h,'g/mol')
c_h = 1/molm_h

mass_sun = YTQuantity(1.989e33, 'g')
met_solar = -3.31


def cl_velz_150(field,data):
	bulk_vel = YTQuantity(150e5, 'cm/s')
	return data['flash','velz'].in_units('cm/s')-bulk_vel
yt.add_field(("gas", "cl_velz_150"), units="cm/s", function=cl_velz_150,force_override=True)

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

def h1_num(field, data):
    return data['h1_mass']*N_A/molm_h
yt.add_field(('gas', 'h1_num'), function=h1_num, force_override=True)

def h2_num(field, data):
    return data['h2_mass']*N_A/molm_h
yt.add_field(('gas', 'h2_num'), function=h2_num, force_override=True)

def o_num(field, data):
    return data['o   ']*N_A/molm_oxy*data['density']*data['cell_volume']
yt.add_field(('gas', 'o_num'), function=o_num, force_override=True)

cut3 = ad.cut_region(["(obj['cl_velz_150'] <= -100e5)"])

cut = ad.cut_region(["(obj['cl_velz_150'] <= -50e5)"])

proj = ds.proj('h   ', 'x', data_source=cut)

met = proj['o_num']/proj['h1_num']
met = np.log10(met)
met = met[(~np.isnan(met)) & (~np.isinf(met))]

print('Metallicity of cloud:', np.mean(met) - met_solar)

m_o1_h1 = proj['o   ']/proj['h1  ']*molm_h/molm_oxy
m_o1_h1 = np.log10(m_o1_h1)
m_o1_h1 = m_o1_h1[(~np.isnan(m_o1_h1)) & (~np.isinf(m_o1_h1))]

print('Metallicity2 of cloud:', np.mean(m_o1_h1) - met_solar)
