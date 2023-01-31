from cotede_qc.cotede_test import get_qc
import numpy

def test(p, parameters, data_store):
    '''Run the global range QC from the CoTeDe GTSPP config.'''

    config   = 'gtspp'
    testname = 'global_range'

    qc = get_qc(p, config, testname)

    return qc

def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass

