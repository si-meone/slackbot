from __future__ import print_function
import os
import re
import datetime
import sys

from slackbot.bot import respond_to
from slackbot.bot import listen_to

sys.path.insert(0, "/home/pi/slackbot/mybot/scripts")
import google_cal


@listen_to('\.whereabouts', re.IGNORECASE)
@listen_to('\.cal', re.IGNORECASE)
def sync_status(message):
    return google_cal.get_next_events(10)

