from cotede_qc.cotede_test import get_qc
import numpy

def test(p, parameters, data_store):
    '''Run the WOA normbias QC from the CoTeDe config.'''

    config   = 'cotede'
    testname = 'woa_normbias'

    qc =get_qc(p, config, testname)

    return qc


def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass