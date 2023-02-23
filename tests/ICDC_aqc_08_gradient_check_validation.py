import os

import qctests.ICDC_aqc_01_level_order as ICDC
import qctests.ICDC_aqc_08_gradient_check as ICDC_gc

import util.testingProfile
import util.main as main
import numpy as np

from db_test_data_store import DbTestDataStore


##### ICDC gradient check.
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

    def test_ICDC_gradient_check(self):
        '''Make sure code processes data supplied by Viktor Gouretski
           correctly.
        '''

        lines = data.splitlines()
        for i, line in enumerate(lines):
            if line[0:2] == 'HH':
                header  = line.split()
                nlevels = int(header[-1][:-3])
                
                depths  = []
                temps   = []
                qctruth = []
                for j in range(nlevels):
                    d = lines[i + j + 1].split()
                    depths.append(float(d[0]))
                    temps.append(float(d[1]))
                    qctruth.append(int(d[2]) > 0)
                
                p  = util.testingProfile.fakeProfile(temps, depths, uid=i)
                ICDC_gc.prepare_data_store(self.data_store)
                qc = ICDC_gc.test(p, self.parameters, self.data_store)

                assert np.array_equal(qc, qctruth), 'Failed profile with header ' + line

# Data provided by Viktor Gouretski, ICDC, University of Hamburg.
data = '''
HH     527484    59.120    11.350 1968  1 18      6OSD
     .0     1.130 1
    2.0     6.490 1
    4.0     9.230 0
    8.0     6.160 0
   15.0     6.600 0
   24.0     7.520 0
HH    3229722    19.308  -119.000 1967  1 29    564CTD
     .0    22.500 0
    1.0    22.500 0
    2.0    22.500 0
    3.0    22.500 0
    4.0    22.490 0
    5.0    22.490 0
    6.0    22.490 0
    7.0    22.480 0
    8.0    22.480 0
    9.0    22.480 0
   10.0    22.480 0
   11.0    22.480 0
   12.0    22.480 0
   13.0    22.470 0
   14.0    22.470 0
   15.0    22.470 0
   16.0    22.470 0
   17.0    22.470 0
   18.0    22.480 0
   19.0    22.480 0
   20.0    22.480 0
   21.0    22.480 0
   22.0    22.480 0
   23.0    22.480 0
   24.0    22.480 0
   25.0    22.490 0
   26.0    22.490 0
   27.0    22.490 0
   28.0    22.490 0
   29.0    22.490 0
   30.0    22.490 0
   31.0    22.490 0
   32.0    22.490 0
   33.0    22.500 0
   34.0    22.500 0
   35.0    22.500 0
   36.0    22.490 0
   37.0    22.500 0
   38.0    22.500 0
   39.0    22.490 0
   40.0    22.500 0
   41.0    22.500 0
   42.0    22.490 0
   43.0    22.490 0
   44.0    22.490 0
   45.0    22.490 0
   46.0    22.490 0
   47.0    22.480 0
   48.0    22.480 0
   49.0    22.480 0
   50.0    22.470 0
   51.0    22.460 0
   52.0    22.460 0
   53.0    22.450 0
   54.0    22.430 0
   55.0    22.390 0
   56.0    22.350 0
   57.0    22.300 0
   58.0    22.240 0
   59.0    22.180 0
   60.0    22.110 0
   61.0    22.040 0
   62.0    21.970 0
   63.0    21.890 0
   64.0    21.820 0
   65.0    21.740 0
   66.0    21.690 0
   67.0    21.630 0
   68.0    21.580 0
   69.0    21.530 0
   70.0    21.490 0
   71.0    21.450 0
   72.0    21.410 0
   73.0    21.380 0
   74.0    21.340 0
   75.0    21.310 0
   76.0    21.280 0
   77.0    21.250 0
   78.0    21.230 0
   79.0    21.210 0
   80.0    21.190 0
   81.0    21.160 0
   82.0    21.150 0
   83.0    21.130 0
   84.0    21.110 0
   85.0    21.080 0
   86.0    21.040 0
   87.0    20.980 0
   88.0    20.920 0
   89.0    20.850 0
   90.0    20.770 0
   91.0    20.680 0
   92.0    20.580 0
   93.0    20.470 0
   94.0    20.330 0
   95.0    20.170 0
   96.0    19.970 0
   97.0    19.770 0
   98.0    19.580 0
   99.0    19.400 0
  100.0    19.230 0
  101.0    19.070 0
  102.0    18.900 0
  103.0    18.750 0
  104.0    18.600 0
  105.0    18.440 0
  106.0    18.310 0
  107.0    18.200 0
  108.0    18.080 0
  109.0    17.950 0
  110.0    17.820 0
  111.0    17.670 0
  112.0    17.510 0
  113.0    17.320 0
  114.0    17.090 0
  115.0    16.860 0
  116.0    16.650 0
  117.0    16.420 0
  118.0    16.210 0
  119.0    16.000 0
  120.0    15.800 0
  121.0    15.600 0
  122.0    15.400 0
  123.0    15.220 0
  124.0    15.070 0
  125.0    14.980 0
  126.0    14.890 0
  127.0    14.790 0
  128.0    14.710 0
  129.0    14.640 0
  130.0    14.600 0
  131.0    14.560 0
  132.0    14.520 0
  133.0    14.470 0
  134.0    14.420 0
  135.0    14.370 0
  136.0    14.310 0
  137.0    14.260 0
  138.0    14.210 0
  139.0    14.170 0
  140.0    14.120 0
  141.0    14.050 0
  142.0    13.990 0
  143.0    13.940 0
  144.0    13.900 0
  145.0    13.860 0
  146.0    13.810 0
  147.0    13.750 0
  148.0    13.690 0
  149.0    13.640 0
  150.0    13.590 0
  151.0    13.560 0
  152.0    13.540 0
  153.0    13.520 0
  154.0    13.510 0
  155.0    13.500 0
  156.0    13.480 0
  157.0    13.480 0
  158.0    13.480 0
  159.0    13.490 0
  160.0    13.500 0
  161.0    13.510 0
  162.0    13.500 0
  163.0    13.480 0
  164.0    13.450 0
  165.0    13.420 0
  166.0    13.390 0
  167.0    13.360 0
  168.0    13.330 0
  169.0    13.290 0
  170.0    13.250 0
  171.0    13.200 0
  172.0    13.160 0
  173.0    13.110 0
  174.0    13.060 0
  175.0    13.010 0
  176.0    12.970 0
  177.0    12.930 0
  178.0    12.880 0
  179.0    12.830 0
  180.0    12.790 0
  181.0    12.750 0
  182.0    12.720 0
  183.0    12.680 0
  184.0    12.650 0
  185.0    12.630 0
  186.0    12.600 0
  187.0    12.580 0
  188.0    12.560 0
  189.0    12.540 0
  190.0    12.530 0
  191.0    12.520 0
  192.0    12.500 0
  193.0    12.480 0
  194.0    12.460 0
  195.0    12.450 0
  196.0    12.430 0
  197.0    12.420 0
  198.0    12.410 0
  199.0    12.390 0
  200.0    12.370 0
  201.0    12.350 0
  202.0    12.320 0
  203.0    12.300 0
  204.0    12.280 0
  205.0    12.270 0
  206.0    12.250 0
  207.0    12.230 0
  208.0    12.210 0
  209.0    12.190 0
  210.0    12.170 0
  211.0    12.150 0
  212.0    12.130 0
  213.0    12.120 0
  214.0    12.100 0
  215.0    12.080 0
  216.0    12.060 0
  217.0    12.040 0
  218.0    12.020 0
  219.0    11.990 0
  220.0    11.970 0
  221.0    11.940 0
  222.0    11.910 0
  223.0    11.890 0
  224.0    11.860 0
  225.0    11.840 0
  226.0    11.810 0
  227.0    11.790 0
  228.0    11.760 0
  229.0    11.740 0
  230.0    11.720 0
  231.0    11.700 0
  232.0    11.680 0
  233.0    11.670 0
  234.0    11.650 0
  235.0    11.640 0
  236.0    11.620 0
  237.0    11.610 0
  238.0    11.600 0
  239.0    11.580 0
  240.0    11.560 0
  241.0    11.540 0
  242.0    11.520 0
  243.0    11.500 0
  244.0    11.480 0
  245.0    11.470 0
  246.0    11.450 0
  247.0    11.440 0
  248.0    11.420 0
  249.0    11.410 0
  250.0    11.400 0
  251.0    11.380 0
  252.0    11.370 0
  253.0    11.360 0
  254.0    11.340 0
  255.0    11.330 0
  256.0    11.310 0
  257.0    11.290 0
  258.0    11.270 0
  259.0    11.250 0
  260.0    11.230 0
  261.0    11.210 0
  262.0    11.200 0
  263.0    11.180 0
  264.0    11.170 0
  265.0    11.160 0
  266.0    11.150 0
  267.0    11.140 0
  268.0    11.120 0
  269.0    11.110 0
  270.0    11.090 0
  271.0    11.070 0
  272.0    11.060 0
  273.0    11.050 0
  274.0    11.040 0
  275.0    11.020 0
  276.0    11.010 0
  277.0    10.990 0
  278.0    10.980 0
  279.0    10.970 0
  280.0    10.960 0
  281.0    10.950 0
  282.0    10.950 0
  283.0    10.940 0
  284.0    10.930 0
  285.0    10.920 0
  286.0    10.910 0
  287.0    10.900 0
  288.0    10.900 0
  289.0    10.890 0
  290.0    10.880 0
  291.0    10.870 0
  292.0    10.860 0
  293.0    10.850 0
  294.0    10.830 0
  295.0    10.810 0
  296.0    10.790 0
  297.0    10.770 0
  298.0    10.750 0
  299.0    10.730 0
  300.0    10.710 0
  301.0    10.690 0
  302.0    10.670 0
  303.0    10.660 0
  304.0    10.650 0
  305.0    10.630 0
  306.0    10.620 0
  307.0    10.600 0
  308.0    10.590 0
  309.0    10.580 0
  310.0    10.570 0
  311.0    10.550 0
  312.0    10.540 0
  313.0    10.530 0
  314.0    10.520 0
  315.0    10.510 0
  316.0    10.510 0
  317.0    10.510 0
  318.0    10.510 0
  319.0    10.510 0
  320.0    10.500 0
  321.0    10.480 0
  322.0    10.470 0
  323.0    10.450 0
  324.0    10.430 0
  325.0    10.410 0
  326.0    10.390 0
  327.0    10.360 0
  328.0    10.330 0
  329.0    10.300 0
  330.0    10.260 0
  331.0    10.230 0
  332.0    10.210 0
  333.0    10.180 0
  334.0    10.150 0
  335.0    10.120 0
  336.0    10.100 0
  337.0    10.070 0
  338.0    10.050 0
  339.0    10.020 0
  340.0    10.000 0
  341.0     9.990 0
  342.0     9.970 0
  343.0     9.950 0
  344.0     9.940 0
  345.0     9.920 0
  346.0     9.910 0
  347.0     9.900 0
  348.0     9.890 0
  349.0     9.890 0
  350.0     9.880 0
  351.0     9.860 0
  352.0     9.850 0
  353.0     9.840 0
  354.0     9.830 0
  355.0     9.830 0
  356.0     9.820 0
  357.0     9.810 0
  358.0     9.800 0
  359.0     9.790 0
  360.0     9.780 0
  361.0     9.770 0
  362.0     9.770 0
  363.0     9.760 0
  364.0     9.750 0
  365.0     9.740 0
  366.0     9.730 0
  367.0     9.720 0
  368.0     9.710 0
  369.0     9.700 0
  370.0     9.680 0
  371.0     9.670 0
  372.0     9.650 0
  373.0     9.640 0
  374.0     9.630 0
  375.0     9.620 0
  376.0     9.610 0
  377.0     9.600 0
  378.0     9.580 0
  379.0     9.560 0
  380.0     9.550 0
  381.0     9.530 0
  382.0     9.510 0
  383.0     9.490 0
  384.0     9.470 0
  385.0     9.450 0
  386.0     9.440 0
  387.0     9.420 0
  388.0     9.400 0
  389.0     9.380 0
  390.0     9.370 0
  391.0     9.350 0
  392.0     9.340 0
  393.0     9.320 0
  394.0     9.310 0
  395.0     9.290 0
  396.0     9.270 0
  397.0     9.240 0
  398.0     9.230 0
  399.0     9.210 0
  400.0     9.190 0
  401.0     9.170 0
  402.0     9.150 0
  403.0     9.130 0
  404.0     9.110 0
  405.0     9.090 0
  406.0     9.070 0
  407.0     9.040 0
  408.0     9.020 0
  409.0     8.990 0
  410.0     8.960 0
  411.0     8.940 0
  412.0     8.920 0
  413.0     8.900 0
  414.0     8.890 0
  415.0     8.870 0
  416.0     8.860 0
  417.0     8.850 0
  418.0     8.840 0
  419.0     8.830 0
  420.0     8.820 0
  421.0     8.810 0
  422.0     8.800 0
  423.0     8.790 0
  424.0     8.780 0
  425.0     8.780 0
  426.0     8.770 0
  427.0     8.760 0
  428.0     8.750 0
  429.0     8.740 0
  430.0     8.730 0
  431.0     8.720 0
  432.0     8.710 0
  433.0     8.700 0
  434.0     8.700 0
  435.0     8.690 0
  436.0     8.680 0
  437.0     8.670 0
  438.0     8.650 0
  439.0     8.640 0
  440.0     8.620 0
  441.0     8.610 0
  442.0     8.590 0
  443.0     8.580 0
  444.0     8.570 0
  445.0     8.550 0
  446.0     8.530 0
  447.0     8.510 0
  448.0     8.490 0
  449.0     8.480 0
  450.0     8.460 0
  451.0     8.440 0
  452.0     8.420 0
  453.0     8.410 0
  454.0     8.390 0
  455.0     8.380 0
  456.0     8.370 0
  457.0     8.360 0
  458.0     8.350 0
  459.0     8.340 0
  460.0     8.330 0
  461.0     8.320 0
  462.0     8.300 0
  463.0     8.290 0
  464.0     8.280 0
  465.0     8.260 0
  466.0     8.250 0
  467.0     8.240 0
  468.0     8.230 0
  469.0     8.220 0
  470.0     8.200 0
  471.0     8.200 0
  472.0     8.190 0
  473.0     8.180 0
  474.0     8.180 0
  475.0     8.170 0
  476.0     8.160 0
  477.0     8.160 0
  478.0     8.150 0
  479.0     8.150 0
  480.0     8.140 0
  481.0     8.140 0
  482.0     8.140 0
  483.0     8.140 0
  484.0     8.150 0
  485.0     8.150 0
  486.0     8.160 0
  487.0     8.160 0
  488.0     8.160 0
  489.0     8.150 0
  490.0     8.140 0
  491.0     8.130 0
  492.0     8.110 0
  493.0     8.090 0
  494.0     8.080 0
  495.0     8.060 0
  496.0     7.980 0
  497.0     7.970 0
  498.0     7.960 0
  499.0     7.960 0
  500.0     7.950 1
  501.0     7.260 1
  502.0     7.250 0
  503.0     7.240 0
  504.0     7.230 0
  505.0     7.230 0
  506.0     7.220 0
  507.0     7.220 0
  508.0     7.220 0
  509.0     7.220 0
  510.0     7.210 0
  511.0     7.210 0
  512.0     7.210 0
  513.0     7.200 0
  514.0     7.200 0
  515.0     7.190 0
  516.0     7.190 0
  517.0     7.180 0
  518.0     7.170 0
  519.0     7.170 0
  520.0     7.160 0
  521.0     7.150 0
  522.0     7.150 0
  523.0     7.140 0
  524.0     7.140 0
  525.0     7.130 0
  526.0     7.130 0
  527.0     7.130 0
  528.0     7.130 0
  529.0     7.120 0
  530.0     7.120 0
  531.0     7.110 0
  532.0     7.110 0
  533.0     7.100 0
  534.0     7.100 0
  535.0     7.090 0
  536.0     7.080 0
  537.0     7.070 0
  538.0     7.060 0
  539.0     7.050 0
  540.0     7.040 0
  541.0     7.030 0
  542.0     7.020 0
  543.0     7.020 0
  544.0     7.010 0
  545.0     7.000 0
  546.0     6.990 0
  547.0     6.980 0
  548.0     6.970 0
  549.0     6.960 0
  550.0     6.950 0
  551.0     6.940 0
  552.0     6.930 0
  553.0     6.920 0
  554.0     6.910 0
  555.0     6.900 0
  556.0     6.890 0
  557.0     6.880 0
  558.0     6.880 0
  559.0     6.870 0
  560.0     6.860 0
  561.0     6.850 0
  562.0     6.840 0
  563.0     6.830 0
HH   10086071    52.616   -50.060 1997  4 10     52PFL
    5.2     2.884 0
   15.5     4.661 0
   25.8     6.997 0
   36.0     9.391 0
   46.3    11.086 0
   56.6    12.840 0
   66.9    13.045 0
   77.2    13.128 0
   87.5    14.455 0
   97.7    13.899 0
  108.0    17.343 0
  118.3    17.700 0
  128.6    21.167 0
  138.9    24.256 1
  149.2     3.032 1
  159.5     3.032 0
  169.7     3.028 0
  180.0     3.052 0
  195.5     3.165 0
  216.1     3.251 0
  236.6     3.255 0
  257.2     3.192 0
  277.7     3.188 0
  298.2     3.208 0
  318.8     3.180 0
  339.4     3.149 0
  359.9     3.204 0
  380.5     3.212 0
  401.0     3.204 0
  421.5     3.165 0
  442.1     3.173 0
  462.7     3.204 0
  501.1     3.212 0
  552.4     3.223 0
  603.8     3.196 0
  655.1     3.180 0
  706.4     3.157 0
  757.7     3.134 0
  808.9     3.110 0
  860.2     3.106 0
  911.5     3.095 0
  962.7     3.095 0
 1013.9     3.126 0
 1065.1     3.141 0
 1116.3     3.149 0
 1167.5     3.149 0
 1218.6     3.134 0
 1269.8     3.114 0
 1320.9     3.091 0
 1372.1     3.059 0
 1423.2     3.009 0
 1474.3     2.985 0
HH   13896185    49.790  -127.646 2004  3 17    142APB
     .0     8.800 0
    1.0     8.800 0
    4.0     8.800 0
    7.5     8.900 0
   13.0     8.800 0
   18.0     8.700 0
   24.0     8.700 0
   29.5     8.700 0
   35.5     8.700 0
   41.0     8.700 0
   46.5     8.900 0
   52.0     9.000 0
   56.5     8.950 0
   61.0     8.850 0
   65.5     8.800 0
   70.0     8.650 0
   73.5     8.500 0
   77.0     8.450 0
   81.0     8.450 0
   84.5     8.400 0
   88.5     8.350 0
   93.0     8.300 0
   96.0     8.200 0
   99.5     8.150 0
  103.5     8.150 0
  107.0     8.100 0
  110.0     8.150 0
  113.5     8.250 0
  116.5     8.200 0
  119.5     8.100 0
  120.0     8.100 0
  123.5     8.000 0
  126.5     7.900 0
  130.0     7.900 0
  132.5     7.800 0
  134.5     7.750 0
  136.5     7.700 0
  139.0     7.550 0
  142.0     7.400 0
  146.0     7.300 0
  150.5     7.200 0
  155.0     7.100 0
  160.5     7.100 0
  164.5     7.100 0
  168.0     7.100 0
  171.0     7.100 0
  175.5     7.100 0
  178.5     7.100 0
  180.0     7.100 0
  183.5     7.100 0
  187.5     7.050 0
  192.0     7.000 0
  196.0     7.000 0
  199.5     6.900 0
  203.5     6.850 0
  207.0     6.800 0
  211.5     6.550 0
  212.0     6.550 0
  212.5     6.500 0
  213.0     6.550 0
  213.5     6.500 0
  214.0     6.500 0
  214.5     6.500 0
  215.0     6.500 0
  215.5     6.500 0
  216.0     6.500 0
  216.5     6.500 0
  217.0     6.500 0
  218.0     6.500 0
  218.5     6.450 0
  219.0     6.600 0
  219.5     6.450 0
  220.0     6.600 0
  220.5     6.450 0
  221.0     6.600 0
  221.5     6.350 1
  222.0     6.600 1
  222.5     6.350 0
  223.0     6.350 0
  223.5     6.350 1
  224.0     6.600 1
  224.5     6.300 0
  225.5     6.350 0
  226.0     6.300 1
  226.5     6.600 1
  227.0     6.300 0
  227.5     6.300 0
  228.5     6.300 0
  229.0     6.300 0
  230.0     6.300 0
  230.5     6.300 1
  231.0     6.650 1
  231.5     6.300 1
  232.0     6.300 0
  232.5     6.350 0
  233.0     6.300 0
  233.5     6.300 0
  234.0     6.300 0
  235.5     6.300 0
  236.5     6.300 0
  237.5     6.300 0
  238.0     6.300 0
  238.5     6.300 0
  239.0     6.300 0
  240.0     6.300 0
  241.0     6.300 0
  242.0     6.300 0
  242.5     6.250 0
  243.5     6.250 0
  244.5     6.250 0
  245.0     6.250 0
  245.5     6.250 0
  247.0     6.250 0
  247.5     6.250 0
  248.5     6.250 0
  249.0     6.250 0
  250.5     6.250 0
  251.0     6.250 0
  252.0     6.250 0
  253.5     6.250 0
  254.0     6.200 0
  255.0     6.200 0
  256.0     6.200 0
  256.5     6.200 0
  257.5     6.200 0
  258.5     6.200 0
  259.5     6.200 0
  260.5     6.200 0
  261.0     6.200 0
  262.0     6.200 0
  263.0     6.200 0
  263.5     6.200 0
  265.0     6.200 0
  265.5     6.150 0
  267.0     6.200 0
  267.5     6.200 0
  269.0     6.150 0
  269.5     6.150 0
  270.0     6.150 0
  270.5     6.150 0
  271.5     6.200 0
  273.0     6.150 0
HH    4364678    33.200   -53.650 1950  1  3     22MBT
     .0    19.900 0
    5.0    12.600 1
   10.0    27.300 1
   15.0    19.900 0
   20.0    19.900 0
   25.0    19.900 0
   30.0    35.100 0
   35.0    20.400 0
   40.0    19.700 0
   45.0    19.700 0
   50.0    19.700 0
   55.0    19.700 0
   60.0    19.700 0
   65.0    19.700 0
   70.0    19.600 0
   75.0    19.600 0
   80.0    19.600 0
   85.0    19.600 0
   90.0    19.600 0
   95.0    19.500 0
  100.0    19.500 0
  105.0    19.500 0
HH    2063855    14.430  -109.430 1968  1  7     17XBT
     .0    34.600 0
   63.0    34.700 0
   64.0    26.200 1
   65.0    22.200 1
   67.0    21.200 0
   74.0    18.500 0
   82.0    17.800 0
   89.0    17.000 0
   95.0    16.300 0
   99.0    15.700 0
  110.0    14.200 0
  123.0    13.400 0
  155.0    12.100 0
  201.0    11.200 0
  292.0    10.100 0
  356.0     9.300 0
  401.0     8.600 0
'''

