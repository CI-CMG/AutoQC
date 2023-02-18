from cotede_qc.cotede_test import get_qc, load_parameters


def test(p, parameters, data_store):
    '''Run the tukey53H QC from the CoTeDe config.'''

    config   = {"sea_water_temperature": {"tukey53H": {"threshold": 6}}}
    testname = 'tukey53H'

    qc = get_qc(p, config, testname, parameters)

    return qc

def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    load_parameters(parameterStore)