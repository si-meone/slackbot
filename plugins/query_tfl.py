from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
import datetime
import sys
sys.path.insert(0, "/home/pi/slackbot/mybot/scripts")
import tfl_query

import tfl_query


@listen_to('^\.bus$', re.IGNORECASE)
def tfl_check(message):
       	    message.send('locations: {}'.format(tfl_query.locations.keys()))


@listen_to('^\.bus (.*)', re.IGNORECASE)
def tfl_check(message, stop_id='0'):
    buses_ordered_by_time = tfl_query.get_arrivals(stop_id)
    if buses_ordered_by_time == 'ApiError occurred':
        message.send(buses_ordered_by_time)
    else:
        for count, (name_dest, arrival) in enumerate(buses_ordered_by_time.iteritems(), 1):
       	    message.send('{}. {} {} [{}]'.format(count, name_dest[0], name_dest[1], str(datetime.timedelta(seconds=arrival))))
