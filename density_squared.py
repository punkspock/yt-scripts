import yt

def dens_sq(field,data):
	dens = data['density']
	dsq = dens*dens
	return dsq

def field_add(new_field):
	'''
	Parameters:
		new_field (str): name of field to add, enclosed in ''

	'''
	yt.add_field(('gas', new_field), units='g**2/cm**6', function=dens_sq)
	print("Field %s added." %s str(new_field))

if __name__==__"main"__:
	field_add('dens_sq')
	
	# load data
	ds = yt.load('4.2.1.density_sap_hdrf
