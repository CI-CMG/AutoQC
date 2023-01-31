from cotede_qc.cotede_test import get_qc
import numpy

def test(p, parameters, data_store):
    '''Run the CoTeDe fuzzy logic QC.'''

    config   = 'fuzzylogic'
    testname = 'fuzzylogic'

    qc = get_qc(p, config, testname)

    return qc

def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass