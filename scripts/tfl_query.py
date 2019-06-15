from tfl.client import Client
from tfl.api_token import ApiToken
from tfl.models.api_error import ApiError

from collections import OrderedDict
import datetime

import ConfigParser

global APP_ID, APP_KEY 
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.optionxform = str

# config.read('/home/simon/IdeaProjects/slackbot/scripts/tfl_api_key.config')
config.read('/home/pi/slackbot/mybot/scripts/tfl_api_key.config')
# config.read('/Users/nasras03/workspace/slackbot/scripts/tfl_api_key.config')
APP_ID = config.get('app_cred', 'app_id')
APP_KEY = config.get('app_cred', 'app_key')

token = ApiToken(APP_ID, APP_KEY)

# TODO: push to a config file for easier editing
locations = {
    'rs': '490000192S',
    'rr': '490000144S',
    'tl': '490013174E',
}


def get_arrivals(location_id=''):
    client = Client(token)
    buses_ordered = {}
    location = locations.get(location_id, None)
    if not location:
        return 'No location found'
    lines = (client.get_arrivals_by_stop_id(locations.get(location_id, 0)))
    buses = {}
    if type(lines) == ApiError:
        return 'ApiError occurred'
    for line in lines:
        buses[(line.line_name, line.destination_name)] = line.time_to_station
    buses_ordered = OrderedDict(sorted(buses.items(), key=lambda t: t[1]))
    return buses_ordered


if __name__ == '__main__':
    stop_id = 'tl'
    buses_ordered_by_time = get_arrivals(stop_id)
    for count, (name_dest, arrival) in enumerate(buses_ordered_by_time.iteritems(), 1):
        print '{}. {} {} [{}]'.format(count, name_dest[0], name_dest[1], str(datetime.timedelta(seconds=arrival)))
