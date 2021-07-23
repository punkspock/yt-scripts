"""
05/13/2021
Sydney Whilden

Read in every file in 4.2.1.density and plot ionization fraction
as a function of time.
"""

import sys
from os import listdir
from os.path import isfile, join
# import yt
import OH_fields as oh
import scaleeverything as se
oh.yt.funcs.mylog.setLevel(50)
import matplotlib.pyplot as plt
from tqdm import tqdm

def loadNCut(file):
	'''
	Load the file and do velocity cut/bad cell cut.

	Parameters:
		file (str): path to file to load
	'''

	ds, ad = oh.loadData(file)
	oh.addFields()
	cut = ad.cut_region(["(obj['bulk_subtracted'] <= -100) & (obj['product'] != 0)"])

	return ds, ad, cut


if __name__ == "__main__":

	# arguments
	if len(sys.argv[1]) > 1:
		scale_arg = sys.argv[1]

	# read in all the files
	path = '../../Data/4.2.1.density'
	dir = listdir(path)  # list of files and subdirectories
	wfile = open('../../Plots/if_over_time.csv', 'w')
	wfile.write('Time, O VI, O, O VI/O')

	# sort out just the files
	only_files = []
	for object in dir:
		# join object name with path name for whole path to object
		joined = join(path, object)
		if isfile(joined) and 'hdf5' in object:
			only_files.append(object)

	only_files.sort()

	# for item in only_files:
	# 	print('{}\n'.format(item))

	# initialize arrays
	times = []
	ion_fracs = []
	sembach = []  # sembach ionization fraction
	# load each file into yt
	for file in tqdm(only_files):
		time = file[len(file) - 4:len(file)]  # last four digits
		times.append(time)
		full_path = '../../Data/4.2.1.density/' + file
		# print(full_path)  # test
		ds, ad, cut = loadNCut(full_path)
		se.main()  # add scaled fields
		# find weighted average ionization fraction
		# just use cells
		if scale_arg == 'unscaled':
			OVI = cut['OVI_scaled']
			t_o = cut['o_total_scaled']
		elif scale_arg == 'scaled':
			OVI = cut['OVI_number']
			t_o = cut['o_total_number']
		else:  # default to unscaled
			OVI = cut['OVI_number']
			t_o = cut['o_total_number']

		t_o = t_o[t_o != 0]
		all_ovi = sum(OVI)
		all_o = sum(t_o)

		if all_o != 0:
			ion_frac = all_ovi / all_o
		else:
			ion_frac = 0
		# ion_fracs.append(ion_frac)

		# don't need to get a mean value
		# append to array of ionization fractions
		ion_fracs.append(ion_frac)

		wfile.write('{}, {}, {}, {}\n'.format(time, all_ovi, all_o, ion_frac))

	for time in times:
		sembach.append(0.2)

	wfile.close()  # conclude
