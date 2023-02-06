""" 
Implements the background check on standard levels and the buddy check
from the EN quality control system, 
http://www.metoffice.gov.uk/hadobs/en3/OQCpaper.pdf
"""

import datetime
from . import EN_background_check, EN_constant_value_check, EN_increasing_depth_check, EN_range_check, EN_spike_and_step_check, EN_stability_check
import util.main as main
import numpy as np

def get_or_calculate_enbackground(p, parameters, data_store):
    enbackground = data_store.get(p.uid(), 'enbackground')
    if not enbackground:
        EN_background_check.test(p, parameters, data_store)
    return data_store.get(p.uid(), 'enbackground')

def test(p, parameters, data_store, allow_level_reinstating=True):
    """
    Runs the quality control check on profile p and returns a numpy array
    of quality control decisions with False where the data value has
    passed the check and True where it failed.

    If allow_level_reinstating is set to True then rejected levels can be
    reprieved by comparing with levels above and below. NB this is done by
    default in EN processing.
    """

    # Define an array to hold results.
    qc = np.zeros(p.n_levels(), dtype=bool)

    # Obtain the obs minus background differences on standard levels.
    result = stdLevelData(p, parameters, data_store)
    if result is None:
        return qc

    # Unpack the results.
    levels, origLevels, assocLevels = result
    # Retrieve the background and observation error variances and
    # the background values.
    enbackground = get_or_calculate_enbackground(p, parameters, data_store)

    bgsl = enbackground['bgstdlevels']
    slev = parameters['enbackground']['depth']
    bgev = enbackground['bgevstdlevels']
    obev = parameters['enbackground']['obev']

    #find initial pge
    pgeData = determine_pge(levels, bgev, obev, p)

    # Find buddy.
    buddy = parameters['buddy_finder'].find_buddy(p, 400000, parameters)

    # Check if we have found a buddy and process if so.
    if buddy:
        pBuddy = buddy.profile
        minDist = buddy.distance

        # buddy vetos
        Fail = False
        if pBuddy.var_index() is None:
            Fail = True
        if Fail == False:
            main.catchFlags(pBuddy)
            if np.sum(pBuddy.t().mask == False) == 0:
                Fail = True

        if Fail == False:

          result = stdLevelData(pBuddy, parameters, data_store)

          buddy_enbackground = get_or_calculate_enbackground(pBuddy, parameters, data_store)

          buddy_pars = buddy_enbackground['bgevstdlevels']

          if result is not None:
            levelsBuddy, origLevelsBuddy, assocLevelsBuddy = result
            bgevBuddy = buddy_pars
            pgeBuddy  = determine_pge(levels, bgevBuddy, obev, pBuddy)
            pgeData   = update_pgeData(pgeData, pgeBuddy, levels, levelsBuddy, minDist, p, pBuddy, obev, bgev, bgevBuddy)

    # Check if levels should be reinstated.
    if allow_level_reinstating:
        if np.abs(p.latitude()) < 20.0:
            depthTol = 300.0
        else:
            depthTol = 200.0
        stdLevelFlags = pgeData >= 0.5
        for i, slflag in enumerate(stdLevelFlags):
            if slflag:
                # Check for non rejected surrounding levels.
                okbelow = False
                if i > 0:
                    if stdLevelFlags[i - 1] == False and levels.mask[i - 1] == False and bgsl.mask[i - 1] == False:
                        okbelow = True
                okabove = False
                nsl = len(stdLevelFlags)
                if i < nsl - 1:
                    if stdLevelFlags[i + 1] == False and levels.mask[i + 1] == False and bgsl.mask[i + 1] == False:
                        okabove = True
                # Work out tolerances.
                if slev[i] > depthTol + 100:
                    tolFactor = 0.5
                elif slev[i] > depthTol:
                    tolFactor = 1.0 - 0.005 * (slev[i] - depthTol)
                else:
                    tolFactor = 1.0
                ttol = 0.5 * tolFactor
                if okbelow == True and okabove == True:
                    xmax = levels[i - 1] + bgsl[i - 1] + ttol
                    xmin = levels[i + 1] + bgsl[i + 1] - ttol
                elif okbelow == True:
                    xmax = levels[i - 1] + bgsl[i - 1] + ttol
                    xmin = levels[i - 1] + bgsl[i - 1] - ttol
                elif okabove == True:
                    xmax = levels[i + 1] + bgsl[i + 1] + ttol
                    xmin = levels[i + 1] + bgsl[i + 1] - ttol
                else:
                    continue
                # Reassign PGE if level is within the tolerances.
                if levels[i] + bgsl[i] >= xmin and levels[i] + bgsl[i] <= xmax:
                    pgeData[i] = 0.49

    # Assign the QC flags to original levels.
    for i, pge in enumerate(pgeData):
        if pgeData.mask[i]: continue
        if pge < 0.5: continue
        for j, assocLevel in enumerate(assocLevels):
            if assocLevel == i:
                origLevel = origLevels[j]
                qc[origLevel] = True

    return qc

def determine_pge(levels, bgev, obev, profile):
    '''
    determine the probability of gross error per level given:
    levels: a list of observed - background temperatures per level (ie the first return of stdLevelData)
    bgev: list of background error variance per level
    obev: list of observational error variances per level
    profile: the wodpy profile object in question
    '''
    pge = np.ma.array(np.ndarray(len(levels)))
    pge.mask = True

    for iLevel, level in enumerate(levels):
        if levels.mask[iLevel] or bgev.mask[iLevel]: continue
        bgevLevel = bgev[iLevel]
        if np.abs(profile.latitude()) < 10.0: bgevLevel *= 1.5**2
        obevLevel = obev[iLevel]
        pge_est = EN_background_check.estimatePGE(profile.probe_type(), False)

        kappa   = 0.1
        evLevel = obevLevel + bgevLevel  #V from the text
        sdiff   = level**2 / evLevel
        pdGood  = np.exp(-0.5 * np.min([sdiff, 160.0])) / np.sqrt(2.0 * np.pi * evLevel)
        pdTotal = kappa * pge_est + pdGood * (1.0 - pge_est)
        pge[iLevel] = kappa * pge_est / pdTotal

    return pge

def buddyCovariance(minDist, profile, buddyProfile, meso_ev_a, meso_ev_b, syn_ev_a, syn_ev_b):
    '''
    coavariance formula for buddy profiles, http://www.metoffice.gov.uk/hadobs/en3/OQCpaper.pdf pp.11
    meso_ev_a == mesoscale error variance for profile a, etc.
    '''

    corScaleA = 100.0 # In km.
    corScaleB = 400.0 # In km.
    corScaleT = 432000.0 # 5 days in secs.
    mesSDist  = minDist / (1000.0 * corScaleA)
    synSDist  = minDist / (1000.0 * corScaleB)

    timeDiff2 = timeDiff(profile, buddyProfile)
    if timeDiff2 is None:
        return None
    timeDiff2 = (timeDiff2 / corScaleT)**2

    covar = (np.sqrt(meso_ev_a * meso_ev_b) *
            (1.0 + mesSDist) * np.exp(-mesSDist - timeDiff2) +
            np.sqrt(syn_ev_a * syn_ev_b) *
            (1.0 + synSDist) * np.exp(-synSDist - timeDiff2))

    return covar

def update_pgeData(pgeData, pgeBuddy, levels, levelsBuddy, minDist, profile, buddyProfile, obev, bgev, bgevBuddy):
    '''
    update the PGE for the profile in question using the buddy pge.
    '''

    for iLevel in range(len(levelsBuddy)):
        if levels.mask[iLevel] or levelsBuddy.mask[iLevel]: continue

        # For simplicity, going to assume that length scales
        # are isotropic and the same everywhere; in the EN
        # processing length scales are stretched in E/W direction
        # near the equator and this functionality could be added
        # later.

        covar = buddyCovariance(minDist, profile, buddyProfile, bgev[iLevel]/2.0, bgevBuddy[iLevel]/2.0, bgev[iLevel]/2.0, bgevBuddy[iLevel]/2.0)
        if covar is None:
            continue;

        errVarA = obev[iLevel] + bgev[iLevel]
        errVarB = obev[iLevel] + bgevBuddy[iLevel]
        rho2    = covar**2 / (errVarA * errVarB)
        expArg  = (-(0.5 * rho2 / (1.0 - rho2)) *
                   (levels[iLevel]**2 / errVarA +
                    levelsBuddy[iLevel]**2 / errVarB -
                    2.0 * levels[iLevel] * levelsBuddy[iLevel] / covar))
        expArg  = -0.5 * np.log(1.0 - rho2) + expArg
        expArg  = min(80.0, max(-80.0, expArg))
        Z       = 1.0 / (1.0 - (1.0 - pgeData[iLevel]) *
                         (1.0 - pgeBuddy[iLevel]) * (1.0 - expArg))
        if Z < 0.0: Z = 1.0 # In case of rounding errors.
        Z = Z**0.5
        pgeData[iLevel] = pgeData[iLevel] * Z

    return pgeData

def stdLevelData(p, parameters, data_store):
    """
    Combines data that have passed other QC checks to create a
    set of observation minus background data on standard levels.
    """

    # Combine other QC results.
    preQC = (EN_background_check.test(p, parameters, data_store) |
             EN_constant_value_check.test(p, parameters, data_store) |
             EN_increasing_depth_check.test(p, parameters, data_store) |
             EN_range_check.test(p, parameters, data_store) |
             EN_spike_and_step_check.test(p, parameters, data_store) |
             EN_stability_check.test(p, parameters, data_store))

    # Get the data stored by the EN background check.
    # As it was run above we know that the data is available in the db.
    enbackground = get_or_calculate_enbackground(p, parameters, data_store)
    origlevels = enbackground['origlevels']
    ptlevels = enbackground['ptlevels']
    bglevels = enbackground['bglevels']
    origLevels = np.array(origlevels)
    diffLevels = (np.array(ptlevels) - np.array(bglevels))
    nLevels    = len(origLevels)
    if nLevels == 0: return None # Nothing more to do.

    # Remove any levels that failed previous QC.
    nLevels, origLevels, diffLevels = filterLevels(preQC, origLevels, diffLevels)
    if nLevels == 0: return None

    levels, assocLevs = meanDifferencesAtStandardLevels(origLevels, diffLevels, p.z(), parameters)

    return levels, origLevels, assocLevs

def filterLevels(preQC, origLevels, diffLevels):
    '''
    preQC: list or array of bools indicating a QC state for each level, determined from other tests
    origLevels: list of level indices that passed EN_background
    diffLevels: correpsonding to origLevels.
    return (nLevels, origLevels, diffLevels) with all elements corresponding to a True entry in preQC removed.
    '''

    nLevels = len(origLevels)
    use = np.ones(nLevels, dtype=bool)
    for i, origLevel in enumerate(origLevels):
        if preQC[origLevel]: use[i] = False
    nLevels = np.count_nonzero(use)
    origLevels = origLevels[use]
    diffLevels = diffLevels[use]

    return nLevels, origLevels, diffLevels

def meanDifferencesAtStandardLevels(origLevels, diffLevels, depths, parameters):
    '''
    origLevels: list of level indices under consideration
    diffLevels: list of differences corresponding to origLevels
    depths: list of depths of all levels in profile.
    returns (levels, assocLevs), where
    levels == a masked array of mean differences at each standard level
    assocLevs == a list of the indices of the closest standard levels to the levels indicated in origLevels
    '''

    # Get the set of standard levels.
    stdLevels = parameters['enbackground']['depth']

    # Create arrays to hold the standard level data and aggregate.
    nStdLevels = len(stdLevels)
    levels     = np.zeros(nStdLevels)
    nPerLev    = np.zeros(nStdLevels)
    assocLevs  = []
    for i, origLevel in enumerate(origLevels):
        # Find the closest standard level.
        j          = np.argmin(np.abs(depths[origLevel] - stdLevels))
        assocLevs.append(j)
        levels[j]  += diffLevels[i]
        nPerLev[j] += 1

    # Average the standard levels where there are data.
    iGT1 = nPerLev > 1
    levels[iGT1] /= nPerLev[iGT1]
    levels = np.ma.array(levels)
    levels.mask = False
    levels.mask[nPerLev == 0] = True

    return levels, assocLevs




def timeDiff(p1, p2):
    '''
    returns the time difference, in seconds, between two profiles
    returns None if the year, month or day in either profile is invalid
    '''

    dts = []
    for prof in [p1, p2]:
        year  = prof.year()
        month = prof.month()
        day   = prof.day()
        if (year is None) or (month is None) or (day is None):
            return None
        if not (year > 0) or not (1 <= month <= 12) or not (1 <= day <= 31):
            return None
        time  = prof.time()
        if time is None or time < 0 or time >= 24:
            hours   = 0
            minutes = 0
            seconds = 0
        else:
            hours = int(time)
            minutesf = (time - hours) * 60
            minutes  = int(minutesf)
            seconds  = int((minutesf - minutes) * 60)

        dts.append(datetime.datetime(year, month, day, hours, minutes, seconds))

    diff = dts[0] - dts[1]

    return np.abs(diff.total_seconds())



def prepare_data_store(data_store):
    pass

def loadParameters(parameterStore):
    pass
