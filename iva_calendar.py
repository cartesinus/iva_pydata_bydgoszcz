import datetime
import dateutil.parser
from google.oauth2 import credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

calendar_id = 'msowansk@gmail.com'

# Load credentials from file
creds = service_account.Credentials.from_service_account_file('gcloud-iva-demo-serviceaccount.json')

# Build the service client
service = build('calendar', 'v3', credentials=creds)

def add_event(calendar_id, summary, location, description, start, end):
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'America/Los_Angeles',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')

def get_events(calendar_id, time_min, time_max):
    events_result = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def get_events_today(calendar_id):
    # Get today's date in the RFC3339 format
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    today_start = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'

    # Call the Calendar API
    events_result = service.events().list(calendarId=calendar_id, timeMin=today_start, timeMax=now,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def update_event(calendar_id, event_id, updated_event):
    event = service.events().update(calendarId=calendar_id, eventId=event_id, body=updated_event).execute()
    print(f'Event updated: {event.get("htmlLink")}')

def check_alarm():
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events = get_events(now, now)
    for event in events:
        reminders = event.get('reminders', {}).get('overrides', [])
        for reminder in reminders:
            if reminder['method'] == 'popup' and reminder['minutes'] == 0:
                print(f'Alarm for event {event["summary"]} should be triggered now')

