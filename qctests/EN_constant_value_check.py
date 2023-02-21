""" 
Implements the constant value check used in the EN quality control 
system, described on page 7 of http://www.metoffice.gov.uk/hadobs/en3/OQCpaper.pdf
"""

import numpy


def test(p, parameters, data_store):
    """ 
    Runs the quality control check on profile p and returns a numpy array 
    of quality control decisions with False where the data value has 
    passed the check and True where it failed. 
    """

    # Check if the QC of this profile was already done and if not
    # run the QC.
    qc_log = None
    cached = data_store.get(p.uid(), 'en_constant_value_check')
    if cached:
        qc_log = cached['qc_log']

    if qc_log is not None:
        return qc_log

    qc_log = run_qc(p, parameters)
    data_store.put(p.uid(), 'en_constant_value_check', {'qc_log':qc_log})
    return qc_log

def run_qc(p, parameters):

    # Get temperature values from the profile.
    t = p.t()
    d = p.z()

    temperatures = {}
    # initialize qc as a bunch of falses (pass by default)
    qc = numpy.zeros(len(t.data), dtype=bool)

    # check for gaps in data
    isTemperature = (t.mask==False)
    isDepth = (d.mask==False)

    #dictionary counts instances of each temperature value
    for i in range(len(t.data)):
        if isTemperature[i]:
            if t.data[i] in temperatures:
                temperatures[t.data[i]] += 1
            else:
                temperatures[t.data[i]] = 1

    for key in temperatures:

        if float(temperatures[key]) / float(len(t.data)) >= 0.9:
            repeats = numpy.where(t.data == key)[0]
            #drop the entries that don't have a depth associated with them;
            #this triggers the 90% rule regardless of the presence of depth data, but
            #ensures that depths are available to assess the range over which constant temps were observed.
            repeatsWithDepth = []
            for j in range(len(repeats)):
                if isDepth[repeats[j]]:
                    repeatsWithDepth.append(repeats[j])
            first = repeatsWithDepth[0]
            last = repeatsWithDepth[-1]

            if d.data[last] - d.data[first] >= 100:
                qc = numpy.ones(len(t.data), dtype=bool) #note everyhing is flagged by this test.

    return qc


def prepare_data_store(data_store):
    data_store.prepare('en_constant_value_check', [{'name':'qc_log', 'type':'BLOB'}])

def loadParameters(parameterStore):
    pass
