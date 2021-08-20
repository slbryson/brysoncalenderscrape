# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START calendar_quickstart]
from __future__ import print_function
import datetime
import os.path
import argparse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main(args):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    # Get Date Range from input
    # start_date = datetime.datetime.strptime(args.startdate, '%Y-%m-%d')
    start_date = datetime.datetime(
        2021, 7, 15, 00, 00, 00, 0).isoformat() + 'Z'

    start_date =args.startdate
    year_s = int(start_date.strftime("%Y"))
    month_s = int(start_date.strftime("%m"))
    day_s = int(start_date.strftime("%d"))

    start_date = datetime.datetime(
        year_s, month_s, day_s, 00, 00, 00, 0).isoformat() + 'Z'
    end_date =args.enddate
    year_s = int(end_date.strftime("%Y"))
    month_s = int(end_date.strftime("%m"))
    day_s = int(end_date.strftime("%d"))       
    end_date = datetime.datetime(
        year_s, month_s, day_s, 00, 00, 00, 0).isoformat() + 'Z'
    print(f"{start_date} , {end_date}")
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='dv7a4kdd814f0s5vp5n1nju2f0@group.calendar.google.com', timeMin=start_date,
                                        timeMax=end_date, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # print(start, event['summary'])
   # This code is to fetch the calendar ids shared with me
    # Src: https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list
    page_token = None
    calendar_ids = []
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            calendar_ids.append(calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    #print(f"\nCalendar Ids {calendar_ids}")

 
 # Only Get Moms Calendar
    calendar_id = 'dv7a4kdd814f0s5vp5n1nju2f0@group.calendar.google.com'
    count = 0
    page_token = None 
    # print('\n----%s:\n' % calendar_id)
    print("Moms Updates from Densie \n")
    eventsResult = service.events().list(
        calendarId=calendar_id,
        timeMin=start_date,
        timeMax=end_date,
        singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    #events = service.events().list(calendarId='primary', pageToken=page_token).execute()

    if not events:
        print('No upcoming events found.')
    for event in events:
        try:
            start = event['start'].get('dateTime', event['start'].get('date'))
            # print(f"Start {start}\n")
            print( f"Date \n{start}\n Description \n{event['description']}\n")
        except KeyError as e:
            pass
            # print (f"No Description for Event {event['updated']} and error {e}")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some Dates.')
    parser.add_argument("-s", 
                    "--startdate", 
                    help="The Start Date - format YYYY-MM-DD", 
                    required=True, 
                    type=datetime.date.fromisoformat)
    parser.add_argument("-e", 
                    "--enddate", 
                    help="The Start Date - format YYYY-MM-DD", 
                    required=True, 
                    type=datetime.date.fromisoformat)
    args = parser.parse_args()
    main(args)
# [END calendar_quickstart]
