"""

Sydney Whilden
01/21/2021

Testing the average N(H II)_Oi across five cells, cell by cell, no projections.

"""

import OH_fields as oh
import scaleeverything as se

if __name__ == "__main__":
        # get epoch from command line arg
        if len(sys.argv[1]) > 1:
            epoch = str(sys.argv[1])
        else:
            epoch == '100'  # default to 100 Myr epoch

        file, time, ds, ad, cut = oh.main(epoch)  # load the data and stuff
        se.main()  # add all the scaled fields
        wfile = open("../../Plots/%s.txt" % (time), 'a')  # open log file
