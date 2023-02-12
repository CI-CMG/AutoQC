from cotede_qc.cotede_test import get_qc


def test(p, parameters, data_store):
    '''Run the gradient QC from the CoTeDe config.'''

    config   = 'cotede'
    testname = 'gradient'

    qc = get_qc(p, config, testname)

    return qc

def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass