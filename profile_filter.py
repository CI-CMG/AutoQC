import numpy as np

class ProfileFilter(object):

  def __init__(self, check_originator_flag_type = True, months_to_use = range(1, 13)):
    self.__check_originator_flag_type = check_originator_flag_type
    self.__months_to_use = months_to_use

  def assess_profile(self, p):
    'decide whether this profile is acceptable for QC or not; False = skip this profile'

    # not interested in standard levels
    if int(p.primary_header['Profile type']) == 1:
      return False

    # no temperature data in profile
    if p.var_index() is None:
      return False

    # temperature data is in profile but all masked out
    if np.sum(p.t().mask == False) == 0:
      return False

    # all depths are less than 10 cm and there are at least two levels (ie not just a surface measurement)
    if np.sum(p.z() < 0.1) == len(p.z()) and len(p.z()) > 1:
      return False

    # no valid originator flag type
    if self.__check_originator_flag_type:
      o_flag = p.originator_flag_type()
      if o_flag is not None and int(o_flag) not in range(1,15):
        return False

    # check month
    if p.month() not in self.__months_to_use:
      return False

    temp = p.t()
    tempqc = p.t_level_qc(originator=True)

    for i in range(len(temp)):
      # don't worry about levels with masked temperature
      if temp.mask[i]:
        continue

      # if temperature isn't masked:
      # it had better be a float
      if not isinstance(temp.data[i], np.float):
        return False
      # needs to have a valid QC decision:
      if tempqc.mask[i]:
        return False
      if not isinstance(tempqc.data[i], np.integer):
        return False
      if not tempqc.data[i] > 0:
        return False

    return True