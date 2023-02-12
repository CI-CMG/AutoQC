from cotede_qc.cotede_test import get_qc


def test(p, parameters, data_store):
    '''Run the rate_of_change QC from the CoTeDe config.'''

    config   = 'cotede'
    testname = 'rate_of_change'

    qc = get_qc(p, config, testname)

    return qc

def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass