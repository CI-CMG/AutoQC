'''Checks the profile location against a global relief dataset to check it is in the ocean.
   It is similar CoTeDe's location at sea test but instead of interpolating to the position
   the surrounding points are checked to see if any are ocean points. This allows for
   errors in the global relief data or imprecise locations close to the coast. This makes it
   similar to the way the ICDC and EN tests work.
'''

from netCDF4 import Dataset
import numpy as np
import os

# Define the area either side of the closest global relief point that is 
# checked for ocean points. 
width = 2

def test(p, parameters, data_store):
    '''Return an array of QC decisions. There is a QC result per level but these
       are all set to the same value, determined by the location.
    '''

    etopx = parameters['etopx']
    etopy = parameters['etopy']
    etoph = parameters['etoph']

    qc = np.zeros(p.n_levels(), dtype=bool)

    # Ensure that lon is in the range -180 to 180 or 0 to 360 and lat is from -90 to 90.
    lat = p.latitude()
    lon = p.longitude()
    if lat is None or lon is None:
        return qc
    if lon < -180 or lon >=360 or lat < -90 or lat > 90: 
        qc[:] = True
        return qc
    if lon < 0: lon += 360 # Needs to be in range 0 to 360.

    # Find closest global relief point and extract section of the array.
    ilat = np.argmin(np.abs(etopy - lat)) + width # Add on the halo width.
    ilon = np.argmin(np.abs(etopx - lon)) + width
    data = etoph[ilat - width:ilat + width + 1, ilon - width:ilon + width + 1]

    # If any point is an ocean point then do not reject.
    if np.all(data >= 0):
        qc[:] = True

    return qc



def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    # Load data into memory. Include a halo so that we can handle points next the data line.
    with Dataset('data/etopo5.nc') as nc:
        etopx = nc.variables['ETOPO05_X'][:]
        etopy = nc.variables['ETOPO05_Y'][:]
        etoph = np.ndarray([len(etopy) + width * 2, len(etopx) + width * 2])
        etoph[:, :] = -1 # Default is ocean points.
        etoph[width:-width, width:-width] = nc.variables['ROSE'][:, :]
        etoph[width:-width, 0:width] = etoph[width:-width, -2*width:-width]
        etoph[width:-width, -width:] = etoph[width:-width, width:2*width]
        parameterStore['etopx'] = etopx
        parameterStore['etopy'] = etopy
        parameterStore['etoph'] = etoph