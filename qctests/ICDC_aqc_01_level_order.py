'''
Python version of check_aqc_01_level_order.f with input/output
adjusted to work with the AutoQC testing suite. Details of the 
original code are:

c/ DATE:       JANUARY 14 2016

c/ AUTHOR:     Viktor Gouretski

c/ AUTHOR'S AFFILIATION:   Integrated Climate Data Center, University of Hamburg, Hamburg, Germany

c/ PROJECT:    International Quality Controlled Ocean DataBase (IQuOD)

c/ TITLE:      check_aqc_01_levels_order 

c/ PURPOSE:
c    to check  the original level order; 
c    if necessary to bring the original levels to increasing order
'''

import numpy as np


def test(p, parameters, data_store):
    '''Return a set of QC decisions. This corresponds to levels with
       negative depths.
    '''

    uid, nlevels, origlevels, zr, tr, qc = level_order(p, data_store)

    return qc

def reordered_data(p, data_store):
    '''Return number levels and depth, temperature in depth order.
       Only non-rejected levels are returned.
    '''

    uid, nlevels, origlevels, zr, tr, qc = level_order(p, data_store)

    return nlevels, zr, tr

def revert_order(p, data, data_store):
    '''Return data in the original profile order. Data rejected in
       the level_order function are returned as missing data.
    '''

    uid, nlevels, origlevels, zr, tr, qc = level_order(p, data_store)

    datar      = np.ma.array(np.ndarray(p.n_levels()), 
                             dtype = data.dtype)
    datar.mask = True

    for i, datum in enumerate(data):
        datar[origlevels[i]] = datum

    return datar

def revert_qc_order(p, qc, data_store):
    '''Return QC array. Missing data values are set to False.'''
    
    qcr = revert_order(p, qc, data_store)
    qcr[qcr.mask] = False
    return qcr

def level_order(p, data_store):
    '''Reorders data into depth order and rejects levels with 
       negative depth.
    '''
    
    # check if the relevant info is already in the db
    precomputed = data_store.get(p.uid(), 'icdclevelorder')
    if precomputed:
        return p.uid(), precomputed['nlevels'], precomputed['origlevels'], precomputed['zr'], precomputed['tr'], precomputed['qc']

    # Extract data and define the index for each level.
    z          = p.z()
    t          = p.t()
    origlevels = np.arange(p.n_levels())

    # Implement the QC. For this test we only reject negative depths.
    qc = z < 0

    # Remove occurrences of no data at a level and rejected obs.
    use        = (z.mask == False) & (t.mask == False) & (qc == False)
    z          = z[use]
    t          = t[use]
    origlevels = origlevels[use]
    nlevels    = np.count_nonzero(use)

    if nlevels > 1:
        # Sort the data. Using mergesort keeps levels with the same depth 
        # in the same order.
        isort      = np.argsort(z, kind='mergesort')
        zr         = z[isort]
        tr         = t[isort]
        origlevels = origlevels[isort]
    else:
        zr         = z
        tr         = t

    # register pre-computed arrays in db for reuse
    data_store.put(p.uid(), 'icdclevelorder', {'nlevels':nlevels, 'origlevels':origlevels, 'zr':zr, 'tr':tr, 'qc':qc})

    return p.uid(), nlevels, origlevels, zr, tr, qc

def prepare_data_store(data_store):
    data_store.prepare('icdclevelorder', [{'name':'nlevels', 'type':'INTEGER'}, {'name':'origlevels', 'type':'BLOB'}, {'name':'zr', 'type':'BLOB'}, {'name':'tr', 'type':'BLOB'}, {'name':'qc', 'type':'BLOB'}])

def loadParameters(parameterStore):
    pass