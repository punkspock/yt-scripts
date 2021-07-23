"""

05/31/2021
Sydney Whilden

Calculate the ratio of H I/O VI for each epoch and plot over time.

"""

# imports
import sys
from os import listdir
from os.path import isfile, join
# import yt
import OH_fields as oh
import scaleeverything as se
import matplotlib.pyplot as plt
from tqdm import tqdm
oh.yt.funcs.mylog.setLevel(50)


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
    wfile = open('../../Plots/hi_ovi.csv', 'w')
    wfile.write("Times, H I, O VI, H I/O VI\n")

    # sort out just the files
    only_files = []
    for object in dir:
        # join object name with path name for whole path to object
        joined = join(path, object)
        if isfile(joined) and 'hdf5' in object:
            only_files.append(object)

    only_files.sort()

    # load each file into yt
    times = []
    hi_ovi_vals = []
    sembach = []
    for file in tqdm(only_files):
        time = file[len(file) - 4:len(file)]  # last four digits
        times.append(time)
        full_path = '../../Data/4.2.1.density/' + file
        # print(full_path)  # test
        ds, ad, cut = loadNCut(full_path)
        se.main()  # add scaled fields

        # calculate H I
        HI = cut['h_neutral_number']
        if scale_arg == 'unscaled':
            OVI = cut['OVI_number']
        elif scale_arg == 'scaled':
            OVI = cut['OVI_scaled']
        else:  # default to unscaled
            OVI = cut['OVI_number']

        OVI = OVI[OVI != 0]  # just in case

        all_ovi = sum(OVI)  # sum number densities in every cell
        all_hi = sum(HI)

		# a check to prevent divide-by-zero errors
        if all_ovi > 0:
            hi_ovi = all_hi / all_ovi
        else:
            hi_ovi = 0

        hi_ovi_vals.append(hi_ovi)

        wfile.write("{}, {}, {}, {}\n".format(time, all_hi, all_ovi, hi_ovi))

    for time in times:
        sembach.append(528982.98)  # from Sembach (2003)

    wfile.close()  # conclude
