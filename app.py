import logging
import sys
from clockify import Clokify, ClockifyDay
from jira import Jira


def merge_entries_by_date(clockify_entries):
    clockify_days = []
    for entry in clockify_entries:
        start = entry["timeInterval"]["start"].split("T")[0]
        if not any(x.date == start for x in clockify_days):
            clockifyDay = ClockifyDay(start)
            clockify_days.append(clockifyDay)
    return sorted(clockify_days, key=lambda day: day.date)


def merge_entries(entries, entries_by_date):
    for entry_date in entries_by_date:
        date = entry_date.date
        for entry in entries:
            if "✅" in entry["description"]:
                continue
            start = entry["timeInterval"]["start"].split("T")[0]
            if start == date:
                entry_date.add_entry(entry)
    return entries_by_date


def run_app():
    if len(sys.argv) != 3:
        raise Exception('illegal arguments')
    start = sys.argv[1]
    end = sys.argv[2]
    logging.info(f"started for dates: {start} - {end}")

    clockify = Clokify()
    jira = Jira()
    entries = clockify.list_time_entries(start, end)
    logging.info(f"downloaded:  {entries}")
    entries_by_date = merge_entries_by_date(entries)
    entries_by_date = merge_entries(entries, entries_by_date)

    for d in entries_by_date:
        date = d.date
        entries = d.entries
        for e in entries:
            issue = e.get_issue()
            description = e.get_description()
            logging.info(f"processing {date} - {issue} - {description}, {e.hours}:{e.minutes}")
            result = jira.add_entry(issue, e.get_time_in_seconds(), date, description)
            if result:
                for id in e.ids:
                    clockify.mark_as_processed(id, issue, description, e.ids[id])

logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level='INFO')