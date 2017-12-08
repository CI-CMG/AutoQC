from cotede_qc.cotede_test import get_qc
import numpy

def test(p, parameters):
    '''Run the WOA normbias QC from the CoTeDe GTSPP config.'''

    config   = 'gtspp'
    testname = 'woa_normbias'
 
    qc = get_qc(p, config, testname)
    
    return qc

