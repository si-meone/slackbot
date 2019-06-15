import collections
import re

from slackbot.bot import listen_to

d = collections.OrderedDict()

d['[.cal]'] = 'google cal'
d['[.bus | .bus <loc>'] = 'bus arrivals'


@listen_to('^\.help', re.IGNORECASE)
@listen_to('^\.commands', re.IGNORECASE)
def sync_status(message):
    data = ''
    for k, v in d.items():
        data += '{} -> {}\n\n'.format(k, v)
    message.send(data)

