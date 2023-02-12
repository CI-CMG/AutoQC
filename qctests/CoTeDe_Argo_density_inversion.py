from cotede_qc.cotede_test import get_qc


def test(p, parameters, data_store):
    '''Run the density inversion QC from the CoTeDe Argo config.'''

    config   = 'argo'
    testname = 'density_inversion'

    qc = get_qc(p, config, testname)

    return qc

def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass