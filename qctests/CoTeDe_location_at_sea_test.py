from cotede_qc.cotede_test import get_qc


def test(p, parameters, data_store):
    '''Run the CoTeDe location at sea QC.'''

    config   = 'cotede'
    testname = 'location_at_sea'
    
    qc = get_qc(p, config, testname)

    return qc

def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass