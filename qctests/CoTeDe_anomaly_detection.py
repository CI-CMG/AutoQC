from cotede_qc.cotede_test import get_qc


def test(p, parameters, data_store):
    '''Run the CoTeDe Anomaly Detection QC.'''

    config   = 'anomaly_detection'
    testname = 'anomaly_detection'

    qc = get_qc(p, config, testname)

    return qc

def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass