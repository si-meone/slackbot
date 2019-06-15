from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
import datetime
import sys
sys.path.insert(0, "/home/pi/slackbot/mybot/scripts")
import tfl_query

locations = {
    'rs': ('490000192S')
}


import tfl_query


@listen_to('^\.bus', re.IGNORECASE)
def tfl_check(message):
       	    message.send('locations: {}'.format(locations.keys()))


@listen_to('^\.bus (.*)', re.IGNORECASE)
def tfl_check(message, stop_id):
    buses_ordered_by_time = tfl_query.get_arrivals(locations.get(stop_id, 0))
    if buses_ordered_by_time == 'ApiError occurred':
        message.send(buses_ordered_by_time)
    else:
        for count, (name_dest, arrival) in enumerate(buses_ordered_by_time.iteritems(), 1):
       	    message.send('{}. {} {} [{}]'.format(count, name_dest[0], name_dest[1], str(datetime.timedelta(seconds=arrival))))
