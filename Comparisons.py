# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 14:06:37 2021

@author: egoet
"""

import yt
from yt import YTQuantity
import numpy as np
import matplotlib.pyplot as plt
yt.funcs.mylog.setLevel(50)

ds = yt.load('../Data/4.2.1.density_sap_hdf5_plt_cnt_0100')
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
met_solar = -3.31

if1_gs = 2.6*10**(-1)
if2_gs = 9.61*10**(-1)
if3_gs = 7.95*10**(-1)
if4_gs = 7.27*10**(-1)
if5_gs = 5.06*10**(-1)
if6_gs = 1.96*10**(-1)
if7_gs = 9.94*10**(-1)
if8_gs = 4.51*10**(-1)
if9_gs = 9.04*10**(-1)


def cl_velz_150(field,data):
	bulk_vel = YTQuantity(150e5, 'cm/s')
	return data['flash','velz'].in_units('cm/s')-bulk_vel
yt.add_field(("gas", "cl_velz_150"), units="cm/s", function=cl_velz_150,force_override=True)

def total_oxygen(field,data):
    return data['flash','o   '] + data['flash','o1  '] + data['flash','o2  '] + data['flash', 'o3  '] + data['flash','o4  '] + data['flash','o5  '] + data['flash','o6  '] + data['flash','o7  '] + data['flash','o8  ']
yt.add_field(("gas", "t_o"), function=total_oxygen, force_override=True)

def neutral_h(field, data):
    return data['flash', 'o   ']*data['flash', 'h   ']/data['gas', 't_o']
yt.add_field(('gas', 'h1  '), function=neutral_h, force_override=True)

def ionized_h(field, data):
    return data['flash', 'h   '] - data['gas', 'h1  ']
yt.add_field(('gas', 'h2  '), function=ionized_h, force_override=True)

def h_numd(field, data):
    return data['h   ']*N_A/molm_h*data['density']
yt.add_field(('gas', 'h_numd'), units="cm**(-3)", function=h_numd, force_override=True)

def h1_numd(field, data):
    return data['h1  ']*N_A/molm_h*data['density']
yt.add_field(('gas', 'h1_numd'), units="cm**(-3)", function=h1_numd, force_override=True)

def h2_numd(field, data):
    return data['h2  ']*N_A/molm_h*data['density']
yt.add_field(('gas', 'h2_numd'), units="cm**(-3)", function=h2_numd, force_override=True)

def o1_numd(field, data):
    return data['o   ']*N_A/molm_oxy*data['density']
yt.add_field(('gas', 'o1_numd'), units="cm**(-3)", function=o1_numd, force_override=True)

def o2_numd(field, data):
    return data['o1  ']*N_A/molm_oxy*data['density']
yt.add_field(('gas', 'o2_numd'), units="cm**(-3)", function=o2_numd, force_override=True)

def o3_numd(field, data):
    return data['o2  ']*N_A/molm_oxy*data['density']
yt.add_field(('gas', 'o3_numd'), units="cm**(-3)", function=o3_numd, force_override=True)

def o4_numd(field, data):
    return data['o3  ']*N_A/molm_oxy*data['density']
yt.add_field(('gas', 'o4_numd'), units="cm**(-3)", function=o4_numd, force_override=True)

def o5_numd(field, data):
    return data['o4  ']*N_A/molm_oxy*data['density']
yt.add_field(('gas', 'o5_numd'), units="cm**(-3)", function=o5_numd, force_override=True)

def o6_numd(field, data):
    return data['o5  ']*N_A/molm_oxy*data['density']
yt.add_field(('gas', 'o6_numd'), units="cm**(-3)", function=o6_numd, force_override=True)

def o7_numd(field, data):
    return data['o6  ']*N_A/molm_oxy*data['density']
yt.add_field(('gas', 'o7_numd'), units="cm**(-3)", function=o7_numd, force_override=True)

def o8_numd(field, data):
    return data['o7  ']*N_A/molm_oxy*data['density']
yt.add_field(('gas', 'o8_numd'), units="cm**(-3)", function=o8_numd, force_override=True)

def o9_numd(field, data):
    return data['o8  ']*N_A/molm_oxy*data['density']
yt.add_field(('gas', 'o9_numd'), units="cm**(-3)", function=o9_numd, force_override=True)

def to_numd(field, data):
    return data['t_o']*N_A/molm_oxy*data['density']
yt.add_field(('gas', 'to_numd'), units="cm**(-3)", function=to_numd, force_override=True)

def h_cd(field, data):
    return data['h_numd']*data['dx']
yt.add_field(('gas', 'h_cd'), units="cm**(-2)", function=h_cd, force_override=True)

def h1_cd(field, data):
    return data['h1_numd']*data['dx']
yt.add_field(('gas', 'h1_cd'), units="cm**(-2)", function=h1_cd, force_override=True)

def h2_cd(field, data):
    return data['h2_numd']*data['dx']
yt.add_field(('gas', 'h2_cd'), units="cm**(-2)", function=h2_cd, force_override=True)

def o1_cd(field, data):
    return data['o1_numd']*data['dx']
yt.add_field(('gas', 'o1_cd'), units="cm**(-2)", function=o1_cd, force_override=True)

def o2_cd(field, data):
    return data['o2_numd']*data['dx']
yt.add_field(('gas', 'o2_cd'), units="cm**(-2)", function=o2_cd, force_override=True)

def o3_cd(field, data):
    return data['o3_numd']*data['dx']
yt.add_field(('gas', 'o3_cd'), units="cm**(-2)", function=o3_cd, force_override=True)

def o4_cd(field, data):
    return data['o4_numd']*data['dx']
yt.add_field(('gas', 'o4_cd'), units="cm**(-2)", function=o4_cd, force_override=True)

def o5_cd(field, data):
    return data['o5_numd']*data['dx']
yt.add_field(('gas', 'o5_cd'), units="cm**(-2)", function=o5_cd, force_override=True)

def o6_cd(field, data):
    return data['o6_numd']*data['dx']
yt.add_field(('gas', 'o6_cd'), units="cm**(-2)", function=o6_cd, force_override=True)

def o7_cd(field, data):
    return data['o7_numd']*data['dx']
yt.add_field(('gas', 'o7_cd'), units="cm**(-2)", function=o7_cd, force_override=True)

def o8_cd(field, data):
    return data['o8_numd']*data['dx']
yt.add_field(('gas', 'o8_cd'), units="cm**(-2)", function=o8_cd, force_override=True)

def o9_cd(field, data):
    return data['o9_numd']*data['dx']
yt.add_field(('gas', 'o9_cd'), units="cm**(-2)", function=o9_cd, force_override=True)

def to_cd(field, data):
    return data['to_numd']*data['dx']
yt.add_field(('gas', 'to_cd'), units="cm**(-2)", function=to_cd, force_override=True)

def h_num(field, data):
    return data['h   ']*N_A/molm_h*data['density']*data['cell_volume']
yt.add_field(('gas', 'h_num'), function=h_num, force_override=True)

def h1_num(field, data):
    return data['h1  ']*N_A/molm_h*data['density']*data['cell_volume']
yt.add_field(('gas', 'h1_num'), function=h1_num, force_override=True)

def h2_num(field, data):
    return data['h2  ']*N_A/molm_h*data['density']*data['cell_volume']
yt.add_field(('gas', 'h2_numd'), function=h2_num, force_override=True)

def o1_num(field, data):
    return data['o   ']*N_A/molm_oxy*data['density']*data['cell_volume']
yt.add_field(('gas', 'o1_num'), function=o1_num, force_override=True)

def o2_num(field, data):
    return data['o1  ']*N_A/molm_oxy*data['density']*data['cell_volume']
yt.add_field(('gas', 'o2_num'), function=o2_num, force_override=True)

def o3_num(field, data):
    return data['o2  ']*N_A/molm_oxy*data['density']*data['cell_volume']
yt.add_field(('gas', 'o3_num'), function=o3_num, force_override=True)

def o4_num(field, data):
    return data['o3  ']*N_A/molm_oxy*data['density']*data['cell_volume']
yt.add_field(('gas', 'o4_num'), function=o4_num, force_override=True)

def o5_num(field, data):
    return data['o4  ']*N_A/molm_oxy*data['density']*data['cell_volume']
yt.add_field(('gas', 'o5_num'), function=o5_num, force_override=True)

def o6_num(field, data):
    return data['o5  ']*N_A/molm_oxy*data['density']*data['cell_volume']
yt.add_field(('gas', 'o6_num'), function=o6_num, force_override=True)

def o7_num(field, data):
    return data['o6  ']*N_A/molm_oxy*data['density']*data['cell_volume']
yt.add_field(('gas', 'o7_num'), function=o7_num, force_override=True)

def o8_num(field, data):
    return data['o7  ']*N_A/molm_oxy*data['density']*data['cell_volume']
yt.add_field(('gas', 'o8_num'), function=o8_num, force_override=True)

def o9_num(field, data):
    return data['o8  ']*N_A/molm_oxy*data['density']*data['cell_volume']
yt.add_field(('gas', 'o9_num'), function=o9_num, force_override=True)

def to_num(field, data):
    return data['t_o']*N_A/molm_oxy*data['density']*data['cell_volume']
yt.add_field(('gas', 'to_num'), function=to_num, force_override=True)

def remove(field,data):
    return data['flash', 'o   '] * data['flash','o1  '] * data['flash','o2  '] * data['flash', 'o3  '] * data['flash','o4  '] * data['flash','o5  '] * data['flash','o6  '] * data['flash','o7  '] * data['flash','o8  ']
yt.add_field(("gas", "rm"), function=remove, force_override=True)

cut = ad.cut_region(["(obj['cl_velz_150'] <= -100e5) & (obj['rm'] != 0)"])

proj = ds.proj('o6_numd', 'x', data_source=cut)

proj2 = ds.proj('o6_numd', 'x', method='sum', data_source=cut)

#Single cell ionization fractions
if1_sc = cut['o1_num']/cut['to_num']
if2_sc = cut['o2_num']/cut['to_num']
if3_sc = cut['o3_num']/cut['to_num']
if4_sc = cut['o4_num']/cut['to_num']
if5_sc = cut['o5_num']/cut['to_num']
if6_sc = cut['o6_num']/cut['to_num']
if7_sc = cut['o7_num']/cut['to_num']
if8_sc = cut['o8_num']/cut['to_num']
if9_sc = cut['o9_num']/cut['to_num']

#Single cell metallicities
m_sc = cut['to_num']/cut['h_num']

#Sightline ionization fractions
h_sl = proj2['h_num']
h_sl = h_sl[h_sl != 0]

o_sl = proj2['to_num']
o_sl = o_sl[o_sl != 0]

o1_sl = proj2['o1_num']
o1_sl = o1_sl[o1_sl!= 0]

o2_sl = proj2['o2_num']
o2_sl = o2_sl[o2_sl != 0]

o3_sl = proj2['o3_num']
o3_sl = o3_sl[o3_sl != 0]

o4_sl = proj2['o4_num']
o4_sl = o4_sl[o4_sl != 0]

o5_sl = proj2['o5_num']
o5_sl = o5_sl[o5_sl != 0]

o6_sl = proj2['o6_num']
o6_sl = o6_sl[o6_sl != 0]

o7_sl = proj2['o7_num']
o7_sl = o7_sl[o7_sl != 0]

o8_sl = proj2['o8_num']
o8_sl = o8_sl[o8_sl != 0]

o9_sl = proj2['o9_num']
o9_sl = o9_sl[o9_sl != 0]

if1_sl = o1_sl/o_sl
if2_sl = o2_sl/o_sl
if3_sl = o3_sl/o_sl
if4_sl = o4_sl/o_sl
if5_sl = o5_sl/o_sl
if6_sl = o6_sl/o_sl
if7_sl = o7_sl/o_sl
if8_sl = o8_sl/o_sl
if9_sl = o9_sl/o_sl

#Sightline metallicities
m_sl = o_sl/h_sl


#Cloud ionization fractions
cloud_h = sum(cut['h_num'])
cloud_o = sum(cut['to_num'])

cloud_o1 = sum(cut['o1_num'])
cloud_o2 = sum(cut['o2_num'])
cloud_o3 = sum(cut['o3_num'])
cloud_o4 = sum(cut['o4_num'])
cloud_o5 = sum(cut['o5_num'])
cloud_o6 = sum(cut['o6_num'])
cloud_o7 = sum(cut['o7_num'])
cloud_o8 = sum(cut['o8_num'])
cloud_o9 = sum(cut['o9_num'])

if1_cl = cloud_o1/cloud_o
if2_cl = cloud_o2/cloud_o
if3_cl = cloud_o3/cloud_o
if4_cl = cloud_o4/cloud_o
if5_cl = cloud_o5/cloud_o
if6_cl = cloud_o6/cloud_o
if7_cl = cloud_o7/cloud_o
if8_cl = cloud_o8/cloud_o
if9_cl = cloud_o9/cloud_o

#Cloud metallicity
m_cl = cloud_o/cloud_h

#Single Cell Calculations
h_o1_sc1 = cut['o1_cd']/(if1_sc*m_sc)
h_o2_sc1 = cut['o2_cd']/(if2_sc*m_sc)
h_o3_sc1 = cut['o3_cd']/(if3_sc*m_sc)
h_o4_sc1 = cut['o4_cd']/(if4_sc*m_sc)
h_o5_sc1 = cut['o5_cd']/(if5_sc*m_sc)
h_o6_sc1 = cut['o6_cd']/(if6_sc*m_sc)
h_o7_sc1 = cut['o7_cd']/(if7_sc*m_sc)
h_o8_sc1 = cut['o8_cd']/(if8_sc*m_sc)
h_o9_sc1 = cut['o9_cd']/(if9_sc*m_sc)

h_o1_sc2 = cut['o1_cd']/(if1_cl*m_cl)
h_o2_sc2 = cut['o2_cd']/(if2_cl*m_cl)
h_o3_sc2 = cut['o3_cd']/(if3_cl*m_cl)
h_o4_sc2 = cut['o4_cd']/(if4_cl*m_cl)
h_o5_sc2 = cut['o5_cd']/(if5_cl*m_cl)
h_o6_sc2 = cut['o6_cd']/(if6_cl*m_cl)
h_o7_sc2 = cut['o7_cd']/(if7_cl*m_cl)
h_o8_sc2 = cut['o8_cd']/(if8_cl*m_cl)
h_o9_sc2 = cut['o9_cd']/(if9_cl*m_cl)

h_o1_sc3 = cut['o1_cd']/(if1_gs*m_sc)
h_o2_sc3 = cut['o2_cd']/(if2_gs*m_sc)
h_o3_sc3 = cut['o3_cd']/(if3_gs*m_sc)
h_o4_sc3 = cut['o4_cd']/(if4_gs*m_sc)
h_o5_sc3 = cut['o5_cd']/(if5_gs*m_sc)
h_o6_sc3 = cut['o6_cd']/(if6_gs*m_sc)
h_o7_sc3 = cut['o7_cd']/(if7_gs*m_sc)
h_o8_sc3 = cut['o8_cd']/(if8_gs*m_sc)
h_o9_sc3 = cut['o9_cd']/(if9_gs*m_sc)

#Sightline calculations
h_o1_sl1 = proj2['o1_cd'][proj2['o1_cd'] != 0]/(if1_sl*m_sl)
h_o2_sl1 = proj2['o2_cd'][proj2['o2_cd'] != 0]/(if2_sl*m_sl)
h_o3_sl1 = proj2['o3_cd'][proj2['o3_cd'] != 0]/(if3_sl*m_sl)
h_o4_sl1 = proj2['o4_cd'][proj2['o4_cd'] != 0]/(if4_sl*m_sl)
h_o5_sl1 = proj2['o5_cd'][proj2['o5_cd'] != 0]/(if5_sl*m_sl)
h_o6_sl1 = proj2['o6_cd'][proj2['o6_cd'] != 0]/(if6_sl*m_sl)
h_o7_sl1 = proj2['o7_cd'][proj2['o7_cd'] != 0]/(if7_sl*m_sl)
h_o8_sl1 = proj2['o8_cd'][proj2['o8_cd'] != 0]/(if8_sl*m_sl)
h_o9_sl1 = proj2['o9_cd'][proj2['o9_cd'] != 0]/(if9_sl*m_sl)

h_o1_sl2 = proj2['o1_cd'][proj2['o1_cd'] != 0]/(if1_cl*m_cl)
h_o2_sl2 = proj2['o2_cd'][proj2['o2_cd'] != 0]/(if2_cl*m_cl)
h_o3_sl2 = proj2['o3_cd'][proj2['o3_cd'] != 0]/(if3_cl*m_cl)
h_o4_sl2 = proj2['o4_cd'][proj2['o4_cd'] != 0]/(if4_cl*m_cl)
h_o5_sl2 = proj2['o5_cd'][proj2['o5_cd'] != 0]/(if5_cl*m_cl)
h_o6_sl2 = proj2['o6_cd'][proj2['o6_cd'] != 0]/(if6_cl*m_cl)
h_o7_sl2 = proj2['o7_cd'][proj2['o7_cd'] != 0]/(if7_cl*m_cl)
h_o8_sl2 = proj2['o8_cd'][proj2['o8_cd'] != 0]/(if8_cl*m_cl)
h_o9_sl2 = proj2['o9_cd'][proj2['o9_cd'] != 0]/(if9_cl*m_cl)

h_o1_sl3 = proj2['o1_cd'][proj2['o1_cd'] != 0]/(if1_gs*m_sl)
h_o2_sl3 = proj2['o2_cd'][proj2['o2_cd'] != 0]/(if2_gs*m_sl)
h_o3_sl3 = proj2['o3_cd'][proj2['o3_cd'] != 0]/(if3_gs*m_sl)
h_o4_sl3 = proj2['o4_cd'][proj2['o4_cd'] != 0]/(if4_gs*m_sl)
h_o5_sl3 = proj2['o5_cd'][proj2['o5_cd'] != 0]/(if5_gs*m_sl)
h_o6_sl3 = proj2['o6_cd'][proj2['o6_cd'] != 0]/(if6_gs*m_sl)
h_o7_sl3 = proj2['o7_cd'][proj2['o7_cd'] != 0]/(if7_gs*m_sl)
h_o8_sl3 = proj2['o8_cd'][proj2['o8_cd'] != 0]/(if8_gs*m_sl)
h_o9_sl3 = proj2['o9_cd'][proj2['o9_cd'] != 0]/(if9_gs*m_sl)

#Calculate column density of hydrogen in domain
hsl = proj['h_numd']
hsl = hsl[hsl != 0]


#Cloud Calculations
vol = sum(cut['cell_volume'])

depth = proj2['dx']
depth = depth[depth != 0]
ave_depth = np.mean(depth)

h_o1_cl1 = (cloud_o1*ave_depth)/(if1_cl*m_cl*vol)
h_o2_cl1 = (cloud_o2*ave_depth)/(if2_cl*m_cl*vol)
h_o3_cl1 = (cloud_o3*ave_depth)/(if3_cl*m_cl*vol)
h_o4_cl1 = (cloud_o4*ave_depth)/(if4_cl*m_cl*vol)
h_o5_cl1 = (cloud_o5*ave_depth)/(if5_cl*m_cl*vol)
h_o6_cl1 = (cloud_o6*ave_depth)/(if6_cl*m_cl*vol)
h_o7_cl1 = (cloud_o7*ave_depth)/(if7_cl*m_cl*vol)
h_o8_cl1 = (cloud_o8*ave_depth)/(if8_cl*m_cl*vol)
h_o9_cl1 = (cloud_o9*ave_depth)/(if9_cl*m_cl*vol)

h_o1_cl2 = (cloud_o1*ave_depth)/(if1_gs*m_cl*vol)
h_o2_cl2 = (cloud_o2*ave_depth)/(if2_gs*m_cl*vol)
h_o3_cl2 = (cloud_o3*ave_depth)/(if3_gs*m_cl*vol)
h_o4_cl2 = (cloud_o4*ave_depth)/(if4_gs*m_cl*vol)
h_o5_cl2 = (cloud_o5*ave_depth)/(if5_gs*m_cl*vol)
h_o6_cl2 = (cloud_o6*ave_depth)/(if6_gs*m_cl*vol)
h_o7_cl2 = (cloud_o7*ave_depth)/(if7_gs*m_cl*vol)
h_o8_cl2 = (cloud_o8*ave_depth)/(if8_gs*m_cl*vol)
h_o9_cl2 = (cloud_o9*ave_depth)/(if9_gs*m_cl*vol)
