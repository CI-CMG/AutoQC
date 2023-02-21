import qctests.ICDC_aqc_10_local_climatology_check as ICDC

import util.testingProfile
import numpy as np

from db_test_data_store import DbTestDataStore


##### ICDC 10 local climatology check.
##### --------------------------------------------------
class TestClass():

    parameters = {
        'db': 'iquod.db',
        'table': 'unit'
    }
    data_store = DbTestDataStore(parameters['db'])

    def setup_method(self):
        # refresh this table every test
        ICDC.loadParameters(self.parameters)

    def teardown_method(self):
        pass

    def test_ICDC_10_local_climatology_check_locs(self):
        '''Make sure code processes locations as expected.
        '''
        ICDC.prepare_data_store(self.data_store)

        p = util.testingProfile.fakeProfile([-5, -5, -5], [1, 2, 5], latitude=-80.0, longitude=0.0)
        qc = ICDC.test(p, self.parameters, self.data_store)
        truth = np.zeros(3, dtype=bool)
        assert np.array_equal(qc, truth), 'Latitude -80.0 outside grid range and should not have flagged data'    

        p = util.testingProfile.fakeProfile([-5, -5, -5], [1, 2, 5], latitude=-70.0, longitude=0.0) 
        qc = ICDC.test(p, self.parameters, self.data_store)
        truth = np.ones(3, dtype=bool)
        assert np.array_equal(qc, truth), 'Latitude -70.0 outside grid range and should have flagged data'    

        p = util.testingProfile.fakeProfile([-5, -5, -5], [1, 2, 5], latitude=-70.0, longitude=-182.0) 
        qc = ICDC.test(p, self.parameters, self.data_store)
        truth = np.zeros(3, dtype=bool)
        assert np.array_equal(qc, truth), 'Longitude -182.0 outside grid range and should not have flagged data'    

        p = util.testingProfile.fakeProfile([-5, -5, -5], [1, 2, 5], latitude=-70.0, longitude=362.0) 
        qc = ICDC.test(p, self.parameters, self.data_store)
        truth = np.zeros(3, dtype=bool)
        assert np.array_equal(qc, truth), 'Longitude 362.0 outside grid range and should not have flagged data'    

        p = util.testingProfile.fakeProfile([-5, -5, -5], [1, 2, 5], latitude=-70.0, longitude=182.0) 
        qc = ICDC.test(p, self.parameters, self.data_store)
        truth = np.ones(3, dtype=bool)
        assert np.array_equal(qc, truth), 'Longitude 182.0 is adjusted to -178 and should have flagged data'    

    def test_ICDC_10_local_climatology_check_ranges(self):
        '''Make sure code processes ranges as expected.
        '''
        p = util.testingProfile.fakeProfile([0], [5], latitude=50.0, longitude=-180.0, date=[2000, 1, 15, 0]) 
        qc = ICDC.test(p, self.parameters, self.data_store)
        truth = np.array([True])
        assert np.array_equal(qc, truth), 'Below temperature range, should be flagged'    

        p = util.testingProfile.fakeProfile([5], [5], latitude=50.0, longitude=-180.0, date=[2000, 1, 15, 0]) 
        qc = ICDC.test(p, self.parameters, self.data_store)
        truth = np.array([False])
        assert np.array_equal(qc, truth), 'In temperature range, should not be flagged'    

        p = util.testingProfile.fakeProfile([12], [5], latitude=50.0, longitude=-180.0, date=[2000, 1, 15, 0]) 
        qc = ICDC.test(p, self.parameters, self.data_store)
        truth = np.array([True])
        assert np.array_equal(qc, truth), 'Above temperature range, should be flagged'    


