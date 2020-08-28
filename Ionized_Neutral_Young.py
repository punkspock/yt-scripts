# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:28:47 2020

@author: egoet
"""


import numpy as np
import yt
import matplotlib
from yt import YTQuantity
import matplotlib.pyplot as plt

#Load data from file
ds = yt.load("../../Data/4.2.1.density_sap_hdf5_plt_cnt_0075", unit_system="cgs")
ad = ds.all_data()
# print(ds.field_list)
# print(ds.derived_field_list)

#Define constants
N_A = 6.0221413e+23
N_A = YTQuantity(N_A, '1/mol')
molm_oxy = 15.9994
molm_oxy = YTQuantity(molm_oxy,'g/mol')
c_o = 1/molm_oxy
R = YTQuantity(8.3145, 'J/(mol*K)')
f = YTQuantity(7.24e+22, 'K/J')

mass_h = 1.6735575e-24
mass_h = YTQuantity(mass_h, 'g')
molm_h = 1.00794
molm_h = YTQuantity(molm_h,'g/mol')
c_h = 1/molm_h

mass_sun = YTQuantity(1.989e33, 'g')
met_solar = -3.31


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

cut3 = ad.cut_region(["(obj['cl_velz_150'] <= -100e5)"])

# cut = ad.cut_region(["(obj['cl_velz_150'] <= -50e5)"])


# ifh = cut3['h2  ']/cut3['h   ']
# print('Ionization fraction of hydrogen:', np.mean(ifh))



# cut_temp = ad.cut_region(["(obj['cl_velz_150'] <= -100e5) & (obj['temperature'] <= 1e4)"])
#
# cut_temp2 = ad.cut_region(["(obj['cl_velz_150'] <= -100e5) & (obj['temperature'] >= 1e4)"])
#
# # mw = (molm_h*cut3['h   '] + molm_oxy*cut3['t_o'])/(cut3['h   ']+cut3['t_o'])
#
# print(mw)
#
# pressure = R*cut3['density']*cut3['temperature']*f/mw
#
# print(pressure)
#
#
# #Calculate mass of neutral and ionized hydrogen in solar masses
# #Using temperature cut
# h1_mass = sum(cut_temp['h_mass'])/mass_sun
# h2_mass = sum(cut_temp2['h_mass'])/mass_sun
# h_tot = h1_mass + h2_mass
#
# #Calculate mass of neutral and ionized hydrogen in solar masses
# #Using ratio of ionized oxygen to distinguish hydrogen
# h1_mass_r = sum(cut3['h1_mass'])/mass_sun
# h2_mass_r = sum(cut3['h2_mass'])/mass_sun
# h_tot_r = h1_mass_r + h2_mass_r
#
# print('Total mass of neutral hydrogen:', h1_mass_r)
# print('Total mass of ionized hydrogen:', h2_mass_r)
# print('Total mass of hydrogen gas:', h_tot_r)


# proj = ds.proj('h   ', 'x', data_source=cut3)
#
#
# r_h1_h = proj['h1  ']/proj['h   ']
# r_h1_h = np.log10(r_h1_h)
# r_h1_h = r_h1_h[(~np.isnan(r_h1_h)) & (~np.isinf(r_h1_h))]

# #Compare temperature to ionization fraction of hydrogen
# x = np.log10(cut3['temperature'])
# y = cut3['h2  ']/cut3['h   ']
# plt.figure()
# plt.scatter(x,y,s=4)
# plt.xlabel('Log(Temperature) K')
# plt.ylabel('Ionization Fraction')
# plt.savefig('Scatter_Young.png')
# plt.show()
# plt.close()
#
# m_o_ions = proj['o_ions']/proj['o   ']
# m_o_ions = np.log10(m_o_ions)
# m_o_ions = m_o_ions[(~np.isnan(m_o_ions)) & (~np.isinf(m_o_ions))]
#
# m_o6 = proj['o5  ']/proj['o   ']
# m_o6 = np.log10(m_o6)
# m_o6 = m_o6[(~np.isnan(m_o6)) & (~np.isinf(m_o6))]

# print('ratio of OVI to OI', np.mean(m_o6))
#
# m_o1_h1 = proj['o   ']/proj['h1  ']*molm_h/molm_oxy
# m_o1_h1 = np.log10(m_o1_h1)
# m_o1_h1 = m_o1_h1[(~np.isnan(m_o1_h1)) & (~np.isinf(m_o1_h1))]
#
# print('Metallicity of cloud:', np.mean(m_o1_h1) - met_solar)
#
# m_o6_o = proj['o5  ']/proj['t_o']
# m_o6_o = np.log10(m_o6_o)
# m_o6_o = m_o6_o[(~np.isnan(m_o6_o)) & (~np.isinf(m_o6_o))]
#
# print('Ionization fraction of OVI:', np.mean(m_o6_o))
#
# projt = ds.proj('h   ', 'x')
#
# frb = proj.to_frb((1.5, 'kpc'), (1000, 10000), height = (11, 'kpc'))
# im = frb['o   ']/frb['h1  ']*molm_h/molm_oxy
# im = np.array(im)
# im = np.log10(im) - met_solar
# #im = im[(~np.isnan(im)) & (~np.isinf(im))] - met_solar
#
# plt.figure(figsize=(10,30))
# plt.imshow(im, origin='lower', extent=(-0.6,0.6,-6,6))
# plt.colorbar()
# plt.xlabel('y (kpc)')
# plt.ylabel('z (kpc)')
# plt.savefig('metallicity.png')
# plt.close()
#
#
#
# m_h2_h1 = proj['h2  ']/proj['h1  ']
# m_h2_h1 = np.log10(m_h2_h1)
# m_h2_h1 = m_h2_h1[(~np.isnan(m_h2_h1)) & (~np.isinf(m_h2_h1))]
#
# print('Ratio of ionized to neutral hydrogen:', np.mean(m_h2_h1))


x = np.log10(cut3['temperature'])
y2 = np.log10(cut3['o5  ']/cut3['t_o'])
plt.figure()
plt.scatter(x,y2,s=4)
plt.xlabel('Log(T)')
plt.ylabel('Log of Ionization Fraction of OVI')
plt.savefig('../../Plots/Scatter_OVI_Young.png')
#plt.close()


# x = np.log10(cut3['temperature'])
# o1 = cut3['o   ']/cut3['t_o']
# o2 = cut3['o1  ']/cut3['t_o']
# o3 = cut3['o2  ']/cut3['t_o']
# o4 = cut3['o3  ']/cut3['t_o']
# o5 = cut3['o4  ']/cut3['t_o']
# o6 = cut3['o5  ']/cut3['t_o']
# o7 = cut3['o6  ']/cut3['t_o']
# o8 = cut3['o7  ']/cut3['t_o']
# o9 = cut3['o8  ']/cut3['t_o']

# fig, axs = plt.subplots(1,3,sharex=True, sharey=True)
# axs[0].scatter(x,o1, c = 'b', label = 'O I', s=4)
# axs[0].scatter(x,o2, c = 'g', label = 'O II',s=4)
# axs[0].scatter(x,o3, c = 'r', label = 'O III',s=4)
# axs[1].scatter(x,o4, c = 'c', label = 'O IV',s=4)
# axs[1].scatter(x,o5, c = 'm', label = 'O V',s=4)
# axs[1].scatter(x,o6, c = 'y', label = 'O VI',s=4)
# axs[2].scatter(x,o7, c = 'k', label = 'O VII',s=4)
# axs[2].scatter(x,o8, c = 'fuchsia', label = 'O VIII',s=4)
# axs[2].scatter(x,o9, c = 'chartreuse', label = 'O IX', s=4)
# fig.text(0.5, 0.04, 'Log(T)', ha='center')
# fig.text(0.04, 0.5, 'Ionization Fraction of Oxygen Ions', va='center', rotation='vertical')
# axs[0].legend()
# axs[1].legend()
# axs[2].legend()
# plt.savefig('Scatter_Oxy_Young.png')
# plt.close()
