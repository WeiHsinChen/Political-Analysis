#
# snippets from https://github.com/inactivist/twitter-streamer/blob/development/streamer/streamer.py
#
from tweepy import OAuthHandler
import logging
import tweepy

logger = logging.getLogger(__name__)

LOCATION_QUERY_MACROS = {
    'any': [-180,-90,180,90],
    'all': 'any',
    'global': 'any',
    'usa': [-124.848974,24.396308,-66.885444,49.384358], # http://www.openstreetmap.org/?box=yes&bbox=-124.848974,24.396308,-66.885444,49.384358
    'contintental_usa': 'usa'
}

def lookup_location_query_macro(name):
    """
    Look up location query name in macro table.
    Return list of coordinates of bounding box as floating point numbers, or None if
    not found.
    """
    resolved = LOCATION_QUERY_MACROS.get(name.lower())
    if isinstance(resolved, basestring):
        return lookup_location_query_macro(resolved)
    return resolved

def get_version():
    from __init__ import __version__
    return __version__


def location_query_to_location_filter(tweepy_auth, location_query):
    t = lookup_location_query_macro(location_query)
    if t:
        return t
    api = tweepy.API(tweepy_auth)
    # Normalize whitespace to single spaces.
    places = api.geo_search(query=location_query)
    normalized_location_query = location_query.replace(' ', '')
    for place in places:
        logger.debug('Considering place "%s"' % place.full_name)
        # Normalize spaces
        if place.full_name.replace(' ', '').lower() == normalized_location_query.lower():
            logger.info('Found matching place: full_name=%(full_name)s id=%(id)s url=%(url)s' % place.__dict__)
            if place.bounding_box is not None:
                t = [x for x in place.bounding_box.origin()]
                t.extend([x for x in place.bounding_box.corner()])
                logger.info('  location box: %s' % t)
                return t
            else:
                raise ValueError("Place '%s' does not have a bounding box." % place.full_name)
    # Nothing found, try for matching macro
    raise ValueError("'%s': No such place." % location_query)

states = { 
'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 
'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado', 
'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 
'GA': 'Georgia', 'HI': 'Hawaii', 'IA': 'Iowa',
'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana',
'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine',
'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri',
'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina',
'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire',
'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada',
'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma',
'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee',
'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia',
'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin',
'WV': 'West Virginia', 'WY': 'Wyoming' }

# returns a dictionary of (state name, bounding box)
def get_state_bounding_boxes(tweepy_auth):
   state_bounding_boxes_dict = {}
   for state_id in states:
      state_name = states[state_id]
      full_state_name = state_name + ", USA"
      print state_name      
      state_bounding_box = location_query_to_location_filter(
         tweepy_auth, full_state_name)
      state_bounding_boxes_dict[state_name] = state_bounding_box
   return state_bounding_boxes_dict
