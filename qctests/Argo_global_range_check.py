""" 
Implements the global range check used in the Argo quality control 
system. 

See Argo quality control manual (based on version 2.5).
"""

from util import obs_utils

def test(p, parameters, data_store):
    """ 
    Runs the quality control check on profile p and returns a numpy array 
    of quality control decisions with False where the data value has 
    passed the check and True where it failed. 
    """

    # Get temperature and pressure values from the profile.
    t = p.t()
    z = obs_utils.depth_to_pressure(p.z(), p.latitude())

    # Make the quality control decisions. This should
    # return true if the temperature is outside -2.5 deg C
    # and 40 deg C or pressure is less than -5.
    qct = (t.mask == False) & ((t.data < -2.5) | (t.data > 40.0))
    qcp = (z.mask == False) & (z.data < -5)
    qc  = qct | qcp
    
    return qc


def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass