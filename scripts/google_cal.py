from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from dateutil import parser
import datetime
import pytz

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

import os

print("Path at terminal when executing this file")
print(os.getcwd() + "\n")

print("This file path, relative to os.getcwd()")
print(__file__ + "\n")


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = '/home/pi/slackbot/mybot/scripts/client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_next_events(num, mins=0):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow()
    mins_fwd = datetime.timedelta(minutes=mins)
    mins_ahead = now + mins_fwd

    min = now.isoformat() + 'Z'  # 'Z' indicates UTC time
    max = None
    if mins:
        max = mins_ahead.isoformat() + 'Z'
    print('Getting the upcoming {} events'.format(num))
    events_result = service.events().list(
        calendarId='primary', timeMin=min, timeMax=max, maxResults=num, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    results = []
    if not events:
        print('No upcoming events found.')
        return
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        TZ = pytz.timezone('Europe/London')
        date_time = datetime.datetime.now(TZ)
        event_start = parser.parse(start)
        time_range = date_time + datetime.timedelta(minutes=mins)
        if date_time.time() <= event_start.time() <= time_range.time()\
                or mins == 0:
            summary = event.get('summary', "")
            location = event.get('location', "")
            description = event.get('description', "")
            attendees = event.get('attendees', "")
            # html_link = event.get('htmlLink', "")
            results.append('{} {} {} {} {}'.format(summary, location, description, attendees, event_start)
    return results


if __name__ == '__main__':
    print(get_next_events(10))

