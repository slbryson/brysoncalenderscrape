# Google Calendar Python Quickstart

Complete the steps described in the [Google Calendar Python Quickstart](
https://developers.google.com/google-apps/calendar/quickstart/python), and in
about five minutes you'll have a simple Python command-line application that
makes requests to the Google Calendar API.

## Brysonscrape
This version will grab the descriptions out of a specific Google Calendar.
Commented code was used first to grab the Google calendar id.
That Calendar ID was hardcoded 
Added argparse to accept dates (start and stop) to grab the comments from events between a specific date range.
### Future
Modify argparse logic to grab the previous 7 days if no date is provided.
## Install

```
pipenv install -r requirements.txt
```

## Run

```
python get_claudette
```
