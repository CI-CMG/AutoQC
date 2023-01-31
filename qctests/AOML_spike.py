# spike test adpated from Patrick Halsall's 
# ftp://ftp.aoml.noaa.gov/phod/pub/bringas/XBT/AQC/AOML_AQC_2018/codes/qc_checks/spike_checker.py
# cal

import numpy

def test(p, parameters, data_store):

    qc = numpy.zeros(p.n_levels(), dtype=bool)
    # this spike test only makes sense for 3 or more levels
    if p.n_levels() < 3:
        return qc

    t = p.t()

    for i in range(2, p.n_levels()-2):
        qc[i] = spike(t[i-2:i+3])

    qc[1] = spike(t[0:3])
    qc[-2] = spike(t[-3:])

    return qc

def spike(t):
	# generic spike check for a masked array of an odd number of consecutive temperature measurements

    if True in t.mask:
    	# missing data, decline to flag
    	return False

    centralTemp = t[int(len(t)/2)]
    medianDiff = numpy.round( abs(centralTemp - numpy.ma.median(t)),2)

    if medianDiff != 0:
        t = numpy.delete(t, int(len(t)/2))
        spikeCheck = numpy.round(abs(centralTemp-numpy.ma.mean(t)), 2)
        if spikeCheck > 0.3:
            return True

    return False

def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass



