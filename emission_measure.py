import yt

file = "../4.2.1.density_sap_hdf5_plt_cnt_0075"  # sample data file
ds = yt.load(file)  # load the data

# print all fields in ds.fields.gas
for field in ds.fields.gas:
    print(field)

# check if emission measure is in the gas fields (should be True)
ds.fields.gas.emission_measure in ds.fields.gas

# find out units for this field
units = ds.fields.gas.emission_measure.get_units
print('Emission measure units: %s' % units)

ad = ds.all_data()

em_meas = ad[ds.fields.gas.emission_measure]  # here i use the field obj

'''
Equivalent statements are:

em_meas = ad['gas', 'emission_measure'] # tuple, no parentheses
em_meas = ad[('gas', 'emission_measure')] # tuple w/ parentheses
em_meas = ad['emission_measure'] # simple field name
'''

length = len(em_meas)  # length of emission measure array
print("How long is the emission measure array? %f" % length)
