import qctests.WOD_range_check

import util.testingProfile
import numpy

from db_test_data_store import DbTestDataStore


##### WOD_range_check -------------------------------------------------------------

def test_WOD_range_check_spotcheck():
    '''
    spot check the WOD_range_test
    '''

    parameters = {
        'db': 'iquod.db',
        'table': 'unit'
    }
    data_store = DbTestDataStore(parameters['db'])

    qctests.WOD_range_check.loadParameters(parameters)

    # should just barely pass; temperatures at threshold for these depths
    p = util.testingProfile.fakeProfile([15, -2.4], [0, 50], -89.5, 0.5) # region 20 == antarctic 
    qc = qctests.WOD_range_check.test(p, parameters, data_store)
    truth = numpy.zeros(2, dtype=bool)
    assert numpy.array_equal(qc, truth), 'incorrectly flagged temperatures within range'    

    # should fail: 10 degrees too warm for 2400 m depth in antarctic
    p = util.testingProfile.fakeProfile([0, 10], [0, 2400], -89.5, 0.5) 
    qc = qctests.WOD_range_check.test(p, parameters, data_store)
    truth = numpy.zeros(2, dtype=bool)
    truth[1] = True 
    assert numpy.array_equal(qc, truth), 'failed to flag deep warm temperatures in antarctic' 
