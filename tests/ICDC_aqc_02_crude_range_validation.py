import os

import qctests.ICDC_aqc_01_level_order as ICDC
import qctests.ICDC_aqc_02_crude_range as ICDC_crude_range

import util.testingProfile
import util.main as main
import numpy as np

from db_test_data_store import DbTestDataStore


##### ICDC crude range check.
##### --------------------------------------------------

class TestClass:

    parameters = {
        'db': 'iquod.db',
        'table': 'unit'
    }
    data_store = DbTestDataStore(parameters['db'])

    def setUp(self):
        if os.path.exists("iquod.db"): os.remove("iquod.db")
        # refresh this table every test
        ICDC.loadParameters(self.parameters)

    def tearDown(self):
        main.dbinteract('DROP TABLE icdclevelorder;')

    def test_ICDC_crude_range(self):
        '''Make sure code processes data supplied by Viktor Gouretski
           correctly.
        '''

        examples = [example1, example2, example3, 
                    example4, example5, example6]

        for i, example in enumerate(examples):
            z = example[:, 0]
            t = example[:, 1]
            f = example[:, 2]

            qctruth = f > 0
            p = util.testingProfile.fakeProfile(t, z, uid=i)
            ICDC_crude_range.prepare_data_store(self.data_store)
            qc = ICDC_crude_range.test(p, self.parameters, self.data_store)

            assert np.array_equal(qc, qctruth), 'Example {} failed'.format(i + 1)

# Data provided by Viktor Gouretski, ICDC, University of Hamburg.
example1 = np.array([
[     .0,    28.600,  0],
[   10.0,    28.600,  0],
[   25.0,    28.520,  0],
[   50.0,    27.410,  0],
[   73.0,    25.120,  0],
[   98.0,    24.390,  0],
[  122.0,    23.320,  0],
[  147.0,    22.790,  0],
[  197.0,    22.040,  0],
[  247.0,    21.880,  0],
[  297.0,    21.860,  0],
[  396.0,    21.780,  0],
[  496.0,    21.760,  0],
[  595.0,    21.740,  0],
[  795.0,    21.810,  0],
[  994.0,    21.840,  0],
[ 1193.0,    21.860,  0],
[ 1492.0,    21.930,  0],
[ 1888.0,    21.960,  0],
[ 1937.0,    22.330,  0],
[ 1987.0,    24.560,  2],
[ 2008.0,    38.150,  1],
[ 2027.0,    48.800,  1]])
example2 = np.array([
[     .0,    30.310,  0],
[    5.0,    30.310,  0],
[   18.0,    29.260,  0],
[   30.0,    29.170,  0],
[   34.0,    27.500,  0],
[   42.0,    26.300,  0],
[   43.0,    25.740,  0],
[   48.0,    24.810,  0],
[   55.0,    24.070,  0],
[   83.0,    22.590,  0],
[  108.0,    21.850,  0],
[  113.0,    21.300,  0],
[  163.0,    19.920,  0],
[  255.0,    18.830,  0],
[  327.0,    18.730,  0],
[  334.0,    23.330,  0],
[  341.0,    27.780,  2],
[  349.0,    32.050,  2],
[  356.0,    36.140,  1]])
example3 = np.array([
[    6.9,    15.700,  0],
[    8.9,    15.700,  0],
[   18.8,    15.700,  0],
[   28.8,    15.670,  0],
[   38.7,    15.440,  0],
[   48.6,    13.620,  0],
[   58.5,    11.920,  0],
[   68.4,    11.390,  0],
[   78.3,    11.270,  0],
[   98.1,    10.900,  0],
[  117.9,    10.730,  0],
[  137.8,    10.510,  0],
[  157.6,    10.340,  0],
[  177.4,     9.470,  0],
[  197.2,     9.140,  0],
[  222.0,     8.380,  0],
[  246.7,     8.090,  0],
[  271.5,     7.870,  0],
[  296.2,     7.290,  0],
[  321.0,     6.910,  0],
[  345.7,     6.830,  0],
[  370.5,     6.720,  0],
[  395.2,     6.210,  0],
[  419.9,     6.070,  0],
[  444.7,     5.690,  0],
[  469.4,     5.790,  0],
[  494.1,     5.570,  0],
[  518.8,     5.650,  0],
[  543.6,     5.680,  0],
[  568.3,     5.270,  0],
[  593.0,     5.170,  0],
[  617.7,     5.010,  0],
[  642.4,     5.030,  0],
[  667.1,     5.120,  0],
[  691.8,     5.180,  0],
[  741.2,     4.920,  0],
[  787.7,    36.560,  1],
[  790.6,     4.370,  0],
[  840.0,     4.200,  0],
[  888.4,    33.530,  1],
[  889.3,     4.110,  0],
[  938.7,     4.040,  0],
[  987.0,    32.370,  2],
[  988.0,     3.970,  0],
[ 1037.4,     3.910,  0],
[ 1084.7,    15.690,  2],
[ 1086.7,     3.840,  0],
[ 1136.0,     3.780,  0],
[ 1431.6,     3.420,  0],
[ 1480.8,     3.370,  0],
[ 1530.0,     3.340,  0],
[ 1579.2,     3.320,  0],
[ 1628.4,     3.300,  0],
[ 1676.6,     3.260,  0],
[ 1725.8,     3.240,  0],
[ 1775.9,     3.230,  0],
[ 1825.0,     3.230,  0],
[ 1874.2,     3.210,  0],
[ 1923.3,     3.170,  0],
[ 5021.8,     7.290,  2]])
example4 = np.array([
[    5.2,    32.370,  0],
[   31.9,    32.370,  0],
[   66.1,    32.480,  2],
[   73.8,    32.504,  2],
[   96.6,    33.846,  1],
[  123.4,    35.412,  1],
[  131.0,     1.393,  0],
[  161.4,     1.442,  0],
[  195.7,     1.497,  0],
[  260.4,     1.497,  0],
[  298.5,     1.497,  0],
[  344.1,     1.497,  0],
[  363.1,     1.497,  0],
[  370.7,     1.497,  0],
[  386.0,     1.497,  0],
[  412.6,     1.497,  0],
[  465.8,     1.497,  0],
[  492.4,     1.497,  0],
[  610.2,     1.393,  0]])
example5 = np.array([
[     .0,    26.000,  0],
[    5.0,    26.000,  0],
[   10.0,    26.000,  0],
[   15.0,    26.000,  0],
[   20.0,    26.000,  0],
[   25.0,    26.000,  0],
[   30.0,    26.000,  0],
[   35.0,    26.000,  0],
[   40.0,    26.000,  0],
[   45.0,    26.000,  0],
[   50.0,    26.000,  0],
[   55.0,    26.000,  0],
[   60.0,    26.000,  0],
[   65.0,    25.800,  0],
[   70.0,    25.400,  0],
[   75.0,    25.100,  0],
[   80.0,    25.000,  0],
[   85.0,    24.500,  0],
[   90.0,    25.100,  0],
[   95.0,    31.800,  0],
[  100.0,    20.600,  0],
[  105.0,     6.200,  0],
[  110.0,    36.100,  1],
[  115.0,    31.500,  2],
[  120.0,      .300,  0],
[  125.0,      .300,  0],
[  130.0,     6.800,  0],
[  135.0,    95.200,  1],
[  140.0,    14.700,  0]])
example6 = np.array([
[     .0,    24.410,  0],
[    1.0,    24.320,  0],
[   14.0,    25.560,  0],
[   35.0,    25.680,  0],
[   42.0,    26.020,  0],
[   49.0,    24.800,  0],
[   69.0,    24.640,  0],
[   81.0,    25.610,  0],
[   83.0,    26.530,  0],
[   91.0,    26.960,  0],
[   97.0,    27.310,  0],
[  121.0,    26.860,  0],
[  140.0,    28.360,  0],
[  142.0,    29.180,  0],
[  163.0,    29.850,  0],
[  168.0,    30.630,  0],
[  171.0,    32.220,  2],
[  177.0,    33.130,  1],
[  184.0,    30.750,  0],
[  195.0,    29.380,  0],
[  210.0,    28.960,  2],
[  215.0,    28.760,  2],
[  241.0,    28.210,  2],
[  326.0,    28.390,  2]])

