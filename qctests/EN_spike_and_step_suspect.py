'''Returns the suspect levels found by the EN spike and step check.'''

from . import EN_spike_and_step_check

def test(p, parameters, data_store):

    return EN_spike_and_step_check.test(p, parameters, data_store, suspect=True)

def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass