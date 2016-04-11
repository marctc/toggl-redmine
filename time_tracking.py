#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from datetime import date, timedelta, datetime
import argparse

from redmine import Redmine
from toggl import Toggl

from config import TOGGL_API_KEY, REDMINE_API_KEY, REDMINE_URL, DEFAULT_ACTIVITY_ID


class TimeTracking(object):

    def __init__(self, toggl_api_key=TOGGL_API_KEY, redmine_api_key=REDMINE_API_KEY):
        self.toggle_api = Toggl(toggl_api_key)
        self.redmine_api = Redmine(REDMINE_URL, key=redmine_api_key)
        self.issue_re = re.compile(r'#(?P<issue_id>\w+)')

    def set_time_entries(self, working_date):
        """
        Get time reports from toggl and tracks the task time to an specific redmine issue
        """
        today = working_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        tomorrow = (working_date + timedelta(1)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        print("tracking time entries for date {}".format(today))

        entries = self.toggle_api.get_time_entries(today,  tomorrow)
        for entry in entries:
            entry_text_issue = self.issue_re.match(entry['description'])
            if entry_text_issue:
                issue_id = entry_text_issue.groups()[0]
                hours = entry['duration'] / 3600.0

                time_entry = self.redmine_api.time_entry.create(
                    issue_id=issue_id,
                    hours=hours,
                    activity_id=DEFAULT_ACTIVITY_ID,
                    comments='',
                    spent_on=working_date.strftime("%Y-%m-%d")
                )
                if time_entry:
                    print("succesfuly tracked time for issue {} ({} hours)".format(issue_id, hours))
                else:
                    print("failed tracking issue {}".format(issue_id))


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', "--date", dest='date', help="The Start Date - format YYYY-MM-DD ",
                        required=False, type=valid_date)
    args = parser.parse_args()
    time_tracking = TimeTracking()
    if args.date:
        entries_date = args.date
    else:
        entries_date = date.today()
    time_tracking.set_time_entries(entries_date)
