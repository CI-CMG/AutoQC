from cotede_qc.cotede_test import get_qc
import numpy

def test(p, parameters, data_store):
    '''Run the tukey53H QC from the CoTeDe config.'''

    config   = {"sea_water_temperature": {"tukey53H": {"threshold": 6}}}
    testname = 'tukey53H'

    qc = get_qc(p, config, testname)

    return qc

def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass