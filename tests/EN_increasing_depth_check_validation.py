import os

import qctests.EN_increasing_depth_check

import util.testingProfile
import numpy as np
import util.main as main
from db_test_data_store import DbTestDataStore


#### EN_increasing_depth_check -------------------------------------------
class TestClass:

    parameters = {
        'db': 'iquod.db',
        "table": 'unit'
    }
    data_store = DbTestDataStore(parameters['db'])

    def setUp(self):
        if os.path.exists("iquod.db"): os.remove("iquod.db")
        # this qc test will go looking for the profile in question in the db, needs to find something sensible
        main.faketable('unit')
        main.fakerow('unit')

    def tearDown(self):
        main.dbinteract('DROP TABLE unit;')

    def test_EN_increasing_depth_outside_valid_range(self):
        '''
        Check EN_increasing_depth_check flags values < 0 and > 11000m.
        '''
        qctests.EN_increasing_depth_check.prepare_data_store(self.data_store)

        p = util.testingProfile.fakeProfile([0,0,0,0,0,0,0,0,0,0], [-1,200,300,400,500,600,700,800,900,1000], uid=8888)
        qc = qctests.EN_increasing_depth_check.test(p, self.parameters, self.data_store)
        truth = np.zeros(10, dtype=bool)
        truth[0] = True
        assert np.array_equal(qc, truth), 'Failed to flag depth < 0'

        p = util.testingProfile.fakeProfile([0,0,0,0,0,0,0,0,0,0], [100,200,300,400,500,600,700,800,900,11001], uid=8889)
        qc = qctests.EN_increasing_depth_check.test(p, self.parameters, self.data_store)
        truth = np.zeros(10, dtype=bool)
        truth[-1] = True
        assert np.array_equal(qc, truth), 'Failed to flag depth > 11000'    

    def test_EN_increasing_depth_flagging(self):
        '''
        Check EN_increasing_depth_check flags incorrect depths.
        '''
        qctests.EN_increasing_depth_check.prepare_data_store(self.data_store)


        p = util.testingProfile.fakeProfile([0,0,0,0,0,0,0,0,0,0], [100,200,300,500,500,600,700,800,900,1000], latitude=0.0, uid=8888)
        qc = qctests.EN_increasing_depth_check.test(p, self.parameters, self.data_store)
        truth = np.zeros(10, dtype=bool)
        truth[3:5] = True
        assert np.array_equal(qc, truth), 'Failed to constant depth'

        p = util.testingProfile.fakeProfile([0,0,0,0,0,0,0,0,0,0], [100,200,300,510,500,600,700,800,900,1000], latitude=0.0, uid=8889)
        qc = qctests.EN_increasing_depth_check.test(p, self.parameters, self.data_store)
        truth = np.zeros(10, dtype=bool)
        truth[3:5] = True
        assert np.array_equal(qc, truth), 'Failed to incorrect depths when cannot determine which is wrong'

        p = util.testingProfile.fakeProfile([0,0,0,0,0,0,0,0,0,0], [100,200,300,610,500,600,700,800,900,1000], latitude=0.0, uid=8890)
        qc = qctests.EN_increasing_depth_check.test(p, self.parameters, self.data_store)
        truth = np.zeros(10, dtype=bool)
        truth[3] = True
        print(qc)
        assert np.array_equal(qc, truth), 'Failed to incorrect depth'

    def test_EN_increasing_depth_all_zero(self):
        '''
        Check EN_increasing_depth_check flags all levels in a profile with all depths = 0
        '''

        p = util.testingProfile.fakeProfile([0]*1000, [0]*1000, uid=8888)
        qctests.EN_increasing_depth_check.prepare_data_store(self.data_store)
        qc = qctests.EN_increasing_depth_check.test(p, self.parameters, self.data_store)
        truth = np.ones(1000, dtype=bool)

        print(qc, truth)

        assert np.array_equal(qc, truth), 'Failed to flag all levels in profile with all 0 depths'  

