from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
from pprint import pprint
import json

import collections

d = collections.OrderedDict()

d['[.rps]'] = 'Classic remake of the Rock paper scissors game'
d['[.today | .tomorrow | .weekly]'] = 'Calender events'

@listen_to('\.help', re.IGNORECASE)
@listen_to('\.commands', re.IGNORECASE)
def sync_status(message):
   data = ''
   for k,v in d.items():
       data += '{} -> {}\n\n'.format(k, v) 
   message.send(data)

