from tfl.client import Client
from tfl.api_token import ApiToken
from tfl.models.api_error import ApiError

from collections import OrderedDict
import datetime

import ConfigParser


def load_properties(config_file):
    global APP_ID, APP_KEY, TOKEN, LOCATIONS
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.optionxform = str
    config.read(config_file)
    APP_ID = config.get('app_cred', 'app_id')
    APP_KEY = config.get('app_cred', 'app_key')
    TOKEN = ApiToken(APP_ID, APP_KEY)
    LOCATIONS = dict(config.items('locations'))


def get_arrivals(location_id=''):
    location_id = location_id.strip().lower()  # more sanitise input
    client = Client(TOKEN)
    buses_ordered = {}
    location = LOCATIONS.get(location_id, None)
    if not location:
        return 'No location found'
    lines = (client.get_arrivals_by_stop_id(LOCATIONS.get(location_id, 'no result').split()[0]))
    buses = {}
    if type(lines) == ApiError:
        return 'ApiError occurred'
    for line in lines:
        min = line.time_to_station
        buses[(line.line_name, line.destination_name, line.vehicle_id)] = line.time_to_station
    buses_ordered = OrderedDict(sorted(buses.items(), key=lambda t: t[1]))
    return buses_ordered


if __name__ == '__main__':
    load_properties('./tfl_api_key.config')
    stop_id = 'kL '
    for k, v in LOCATIONS.items():
        print '{} => {}'.format(k, v.split()[1])
    buses_ordered_by_time = get_arrivals(stop_id)
    print '{} Arrivals'.format(LOCATIONS.get(stop_id, 'no result').split()[1])
    if type(buses_ordered_by_time) == str:
        print buses_ordered_by_time
    else:
        for count, (name_dest, arrival) in enumerate(buses_ordered_by_time.iteritems(), 1):
            # print '{}. {} {} [{}]'.format(count, name_dest[0], name_dest[1], str(datetime.timedelta(seconds=arrival)))
            mins = arrival/60
            if mins == 0:
                mins = 'Due'
            else:
                mins = '{} mins'.format(mins)
            print '{}. {} {} [{}]'.format(count, name_dest[0], name_dest[1], str(mins))
