from cotede_qc.cotede_test import get_qc
import numpy

def test(p, parameters):
    '''Run the digit roll over QC from the CoTeDe config.'''

    config   = 'cotede'
    testname = 'digit_roll_over'

    try:
        qc = get_qc(p, config, testname)
    except:
        qc = numpy.zeros(1, dtype=bool)

    return qc

