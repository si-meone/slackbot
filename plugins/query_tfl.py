from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
import datetime
import sys
sys.path.insert(0, "/home/pi/slackbot/mybot/scripts")

import tfl_query

tfl_query.load_properties('/home/pi/slackbot/mybot/scripts/tfl_api_key.config')


@listen_to('^\.bus$', re.IGNORECASE)
def tfl_check(message):
    message.send('locations: {}'.format(tfl_query.LOCATIONS.keys()))


@listen_to('^\.bus (.*)', re.IGNORECASE)
def tfl_check(message, stop_id='0'):
    buses_ordered_by_time = tfl_query.get_arrivals(stop_id)
    if type(buses_ordered_by_time) == str:
        message.send(buses_ordered_by_time)
    else:
        message.send('{} Arrivals'.format(tfl_query.LOCATIONS.get(stop_id, 'no result').split()[1]))
        for count, (name_dest, arrival) in enumerate(buses_ordered_by_time.iteritems(), 1):
            message.send('{}. {} {} [{}]'.format(count, name_dest[0], name_dest[1],
                                                 str(datetime.timedelta(seconds=arrival))))
