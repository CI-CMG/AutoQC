"""
Implements the EN increasing depth check.
"""

from collections import Counter

import numpy as np

from . import EN_spike_and_step_check


def test(p, parameters, data_store):
    """
    Runs the quality control check on profile p and returns a numpy array
    of quality control decisions with False where the data value has
    passed the check and True where it failed.
    """

    # Check if the QC of this profile was already done and if not
    # run the QC.
    qc_log = None
    cached = data_store.get(p.uid(), 'en_increasing_depth_check')
    if cached:
        qc_log = cached['qc_log']

    if qc_log is not None:
        return qc_log

    qc_log = run_qc(p, parameters, data_store)
    data_store.put(p.uid(), 'en_increasing_depth_check', {'qc_log':qc_log})
    return qc_log

def mask_index(mat, index):
    """
    update comparison matrix by setting (index,j) and (i,index) to 0 for all i,j
    corresponds to recomputing the matrix after qc[index] is set True.
    """

    n = len(mat)

    for i in range(n):
        mat[index, i] = 0
        mat[i, index] = 0

def run_qc(p, parameters, data_store):

    # Get z values from the profile.
    d    = p.z()
    mask = d.mask
    n    = p.n_levels()

    # Initialize qc array.
    qc = np.zeros(n, dtype=bool)

    # Basic check on each level.
    qc[d < 0]     = True
    qc[d > 11000] = True

    # don't perform more sophisticated tests for single-level profiles
    if n == 1:
        return qc

    # if all the depths are the same, flag all levels and finish immediately
    most_common_depth = Counter(d.data).most_common(1)
    if most_common_depth[0][1] == len(d.data):
        qc = np.ones(n, dtype=bool)
        uid = p.uid()
        return qc

    # initialize matrix
    # Comp gets set to 1 if there is not an increase in depth.
    rows = []
    for i in range(n):
        # generate ith row
        row = d[i] < d
        # invert logic for columns gt row
        row = np.concatenate([row[0:i], ~row[i:]])
        rows.append(row)
    comp = np.vstack(rows)
    # enforce initial qc, masks:
    qcs = [i for i,q in enumerate(qc) if q]
    masks = [i for i,m in enumerate(mask) if m]
    for m in list(set(qcs+masks)):
        mask_index(comp, m)
    # enforce diagonal
    for i in range(n):
        comp[i,i] = 0
    comp.astype(int)

    # Now check for inconsistencies in the depth levels.
    currentMax = 1

    while currentMax > 0:
        # Check if comp was set to 1 anywhere and which level was
        # most inconsistent with the others.
        currentMax = 0
        currentLev  = -1
        otherLev = -1
        for i in range(n):
            lineSum = np.sum(comp[:, i])
            if lineSum >= currentMax:
                currentMax = lineSum
                currentLev = i

        # Reject immediately if more than one inconsistency or
        # investigate further if one inconsistency.
        if currentMax > 1:
            qc[currentLev] = True
        elif currentMax == 1:
            # Find out which level it is inconsistent with.
            for i in range(n):
                if comp[i, currentLev] == 1: otherLev = i
            # Check if one was rejected by the spike and step
            # check, otherwise reject both.
            try:
                spikeqc
            except:
                spikeqc = EN_spike_and_step_check.test(p, parameters, data_store)
            if spikeqc[currentLev]: qc[currentLev] = True
            if spikeqc[otherLev]:   qc[otherLev]   = True
            if spikeqc[currentLev] == False and spikeqc[otherLev] == False:
                qc[currentLev] = True
                qc[otherLev]   = True
        # update comp matrix:
        if currentLev > -1 and qc[currentLev]:
            mask_index(comp, currentLev)
        if otherLev > -1 and qc[otherLev]:
            mask_index(comp, otherLev)
    return qc

def prepare_data_store(data_store):
    data_store.prepare('en_increasing_depth_check', [{'name':'qc_log', 'type':'BLOB'}])

def loadParameters(parameterStore):
    pass