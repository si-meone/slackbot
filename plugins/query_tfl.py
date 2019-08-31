from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
import datetime
import sys
sys.path.insert(0, "/home/pi/slackbot/mybot/scripts")

import tfl_query

def load_properties():
    tfl_query.load_properties('/home/pi/slackbot/mybot/scripts/tfl.config')


@listen_to('^\.bus$', re.IGNORECASE)
def tfl_check(message):
    load_properties()
    for k, v in tfl_query.LOCATIONS.items():
        message.send('{}: {}'.format(k, v.split()[1]))


@listen_to('^\.bus (.*)', re.IGNORECASE)
def tfl_check(message, stop_id='0'):
    load_properties()
    stop_id = stop_id.strip().lower() # more sanitise input
    buses_ordered_by_time = tfl_query.get_arrivals(stop_id)
    if type(buses_ordered_by_time) == str:
        message.send(buses_ordered_by_time)
    else:
        message.send('{} Arrivals'.format(tfl_query.LOCATIONS.get(stop_id, 'no result').split()[1]))
        for count, (name_dest, arrival) in enumerate(buses_ordered_by_time.iteritems(), 1):
            mins = arrival/60
            if mins == 0:
                mins = 'Due'
            else:
                mins = '{} mins'.format(mins)
            message.send('{}. {} {} [{}]'.format(count, name_dest[0], name_dest[1],mins))
