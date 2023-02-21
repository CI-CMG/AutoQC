import abc
import numpy as np
from cotede.qctests.possible_speed import haversine

class Buddy(object):
  def __init__(self, uid, year, month, cruise, latitude, longitude):
    self.profile = None
    self.distance = None
    self.uid = uid
    self.year = year
    self.month = month
    self.cruise = cruise
    self.latitude = latitude
    self.longitude = longitude


def assessBuddyDistance(p, buddy):
    """
    given a profile <p> and a possible buddy profile <buddy>,
    return None if <buddy> is not a valid buddy, or the distance
    to <p> if it is.
    """

      # Check that it is not the same profile and that they
      # are near in time. The time criteria matches the EN
      # processing but would probably be better if it checked
      # that the profiles were within a time threshold. The
      # cruise is compared as two profiles from the same instrument
      # should not be compared.
    if (buddy.uid == p.uid() or
        buddy.year != p.year() or
        buddy.month != p.month() or
        buddy.cruise == p.cruise()): return None
    lat = p.latitude()
    lon = p.longitude()
    latComp = buddy.latitude
    lonComp = buddy.longitude
    # Do a rough check of distance.
    latDiff = np.abs(latComp - lat)
    if latDiff > 5: return None
    # Do a more detailed check of distance.
    # Check in case they are either side of the edge of the map.
    if np.abs(lonComp - lon) > 180:
        if lonComp < lon:
            lonComp += 360.0
        else:
            lonComp -= 360.0
    # Calculate distance and return.
    return haversine(lat, lon, latComp, lonComp)


class BuddyFinder(metaclass=abc.ABCMeta):

  def _assessBuddyDistance(self, p, buddy):
      return assessBuddyDistance(p, buddy)

  @abc.abstractmethod
  def find_buddy(self, p, max_distance, parameters):
      pass