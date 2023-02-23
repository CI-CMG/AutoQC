import os

import qctests.EN_background_check
import qctests.EN_spike_and_step_check
from db_test_data_store import DbTestDataStore
from util import main
import util.testingProfile
import numpy

##### EN_background_check ---------------------------------------------------

class TestClass:

    parameters = {
        'db': 'iquod.db',
        "table": 'unit'
    }
    qctests.EN_background_check.loadParameters(parameters)
    data_store = DbTestDataStore(parameters['db'])

    def setUp(self):
        if os.path.exists("iquod.db"): os.remove("iquod.db")
        # this qc test will go looking for the profile in question in the db, needs to find something sensible
        main.faketable('unit')
        main.fakerow('unit')
        # need to re-do this every time to refresh the enspikeandstep table
        qctests.EN_spike_and_step_check.loadParameters(self.parameters)

    def tearDown(self):
        main.dbinteract('DROP TABLE unit;')

    def test_EN_background_check_temperature(self):
        '''
        Make sure EN_background_check is flagging temperature excursions
        '''

        p = util.testingProfile.fakeProfile([1.8, 1.8, 1.8, 7.1], [0.0, 2.5, 5.0, 7.5], latitude=55.6, longitude=12.9, date=[1900, 1, 15, 0], probe_type=7, uid=8888)
        qctests.EN_background_check.prepare_data_store(self.data_store)
        qc = qctests.EN_background_check.test(p, self.parameters, self.data_store)
        expected = [False, False, False, True]
        assert numpy.array_equal(qc, expected), 'mismatch between qc results and expected values'

    def test_EN_background_check_findGridCell(self):
        '''
        check behavior of grid cell identifier:
        wrap around to the beginning of the list after exceeding the end by more than one cell;
        same idea at the beginning.
        '''

        gridLat  = [-90,-60,-30,0,30,60,90]
        gridLong = [0,60,120,180,240,300]
        p = util.testingProfile.fakeProfile([0], [0], latitude=121, longitude=421)

        ilon, ilat = qctests.EN_background_check.findGridCell(p, gridLong, gridLat)
        assert ilon == 1
        assert ilat == 5

    def test_EN_background_check_findGridCell_even_spacing(self):
        '''
        findGridCell will silently fail if grid spacings are not even;
        check that asserts are raised checking for this.
        '''

        gridLat  = [10,21,28,40]
        gridLong = [10,20,30,40]
        p = util.testingProfile.fakeProfile([0], [0], latitude=29, longitude=51) 

        try:
            ilon, ilat = qctests.EN_background_check.findGridCell(p, gridLong, gridLat)
        except AssertionError:
            assert True
            return

        try:
            ilon, ilat = qctests.EN_background_check.findGridCell(p, gridLat, gridLong)
        except AssertionError:
            assert True
            return

        assert False, "findGridCell failed to raise an exception for unevenly spaced grid points"

    def test_EN_background_check_estimatePGE(self):
        '''
        check the basic behavior of the probable gross error prior estimator
        '''

        assert qctests.EN_background_check.estimatePGE(1, False) == 0.05, 'incorrect non-suspect bathythermograph pge'
        assert qctests.EN_background_check.estimatePGE(16, True) == 0.525, 'incorrect suspect bathythermograph pge'
        assert qctests.EN_background_check.estimatePGE(4, False) == 0.01, 'incorrect non-suspect non-bathythermograph pge'
