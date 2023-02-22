import util.main as main

from buddy_finder import BuddyFinder, Buddy


class DbBuddyFinder(BuddyFinder):

  def __get_profile_info(self, parameters):
    # Gets information about the profiles from the database.
    query = 'SELECT uid,year,month,cruise,lat,long FROM ' + parameters['table']
    return main.dbinteract(query, targetdb=parameters["db"])

  def find_buddy(self, p, max_distance, parameters):
    profiles = self.__get_profile_info(parameters)
    minDist  = 1000000000.0
    iMinDist = None
    min_buddy = None
    for iProfile, profile in enumerate(profiles):
      buddy = Buddy(profile[0], profile[1], profile[2], profile[3], profile[4], profile[5])
      pDist = self._assessBuddyDistance(p, buddy)
      if pDist is not None and pDist < minDist:
        minDist  = pDist
        iMinDist = iProfile
        min_buddy = buddy
    if minDist <= max_distance:
      buddy_profile = main.get_profile_from_db(profiles[iMinDist][0], parameters['table'], parameters['db'])
      if buddy_profile:
        min_buddy.profile = buddy_profile
        min_buddy.distance = minDist
        return min_buddy
    return None
