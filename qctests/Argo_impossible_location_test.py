"""
Implements the impossible location test on page 6 of http://w3.jcommops.org/FTPRoot/Argo/Doc/argo-quality-control-manual.pdf
"""

import numpy

def test(p, parameters, data_store):
    """
    Runs the quality control check on profile p and returns a numpy array
    of quality control decisions with False where the data value has
    passed the check and True where it failed.
    """

    # Get the lat and long:
    latitude = p.latitude()
    longitude = p.longitude()

    # initialize qc as false:
    qc = numpy.zeros(p.n_levels(), dtype=bool)

    if isinstance(latitude, float) and latitude < -90 or latitude > 90:
        qc[:] = True
    elif isinstance(longitude, float) and longitude < -180 or longitude > 180:
        qc[:] = True

    return qc

def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass