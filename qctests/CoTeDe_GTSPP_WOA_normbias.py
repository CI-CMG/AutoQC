from cotede_qc.cotede_test import get_qc, load_parameters


def test(p, parameters, data_store):
    '''Run the WOA normbias QC from the CoTeDe GTSPP config.'''

    config   = 'gtspp'
    testname = 'woa_normbias'
 
    qc = get_qc(p, config, testname, parameters)
    
    return qc

def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    load_parameters(parameterStore)