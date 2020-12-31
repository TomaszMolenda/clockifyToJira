import logging
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Clokify:
    clockify_token = os.getenv("clockify-token")
    workspace_id = os.getenv("clockify-workspace-id")
    user_id = os.getenv("clockify-user-id")
    api = "https://api.clockify.me/api/v1"
    headers = {'X-Api-Key': clockify_token}
    page_size = 400

    # format 2020-10-30
    def list_time_entries(self, start, end):
        params = {'page-size': self.page_size, 'start': f"{start}T00:00:00.000Z", 'end': f"{end}T23:59:59.999Z"}
        response = requests.get(
            f"{self.api}/workspaces/{self.workspace_id}/user/{self.user_id}/time-entries",
            headers=self.headers, params=params)
        return json.loads(response.text)

    def mark_as_processed(self, id, issue, description, entry):
        logging.info(f"updating clockify id: {id}, {issue}, {description}, entry: {entry}")
        response = requests.put(
            f"{self.api}/workspaces/{self.workspace_id}/time-entries/{id}",
            headers=self.headers,
            json={
                'start': entry['timeInterval']['start'],
                'billable': entry['billable'],
                'description': f"{issue} ✅ {description}",
                'projectId': entry['projectId'],
                'taskId': entry['taskId'],
                'end': entry['timeInterval']['end'],
                'tagIds': [],
                'customFields': [],
            }
        )
        return response.status_code == 201


class ClockifyDay:

    def __init__(self, date):
        self.date = date
        self.entries = []

    def __get_or_create_entry(self, entry):
        description = entry["description"]
        for e in self.entries:
            if e.description == description:
                return e
        description = entry["description"]

        entry = ClokifyEntry(description)
        self.entries.append(entry)
        return entry

    def add_entry(self, entry_in):
        entry = self.__get_or_create_entry(entry_in)
        id = entry_in["id"]
        duration = entry_in["timeInterval"]["duration"]
        entry.ids[id] = entry_in
        entry.add_duration(duration)


class ClokifyEntry:
    def __get_hours(self, duration):
        if not "H" in duration:
            return 0
        return int(duration[duration.find("PT")+len("PT"):duration.rfind("H")])

    def __get_minutes(self, duration):
        if not "M" in duration:  # PT1H
            return 0
        if not "H" in duration:  # PT52M
            return int(duration[duration.find("PT")+len("PT"):duration.rfind("M")])
        return int(duration[duration.find("H")+len("H"):duration.rfind("M")])  # PT2H38M

    def __init__(self, description):
        self.hours = 0
        self.minutes = 0
        self.ids = {}
        self.description = description

    def add_duration(self, duration):
        self.hours = self.hours + self.__get_hours(duration)
        self.minutes = self.minutes + self.__get_minutes(duration)
        if self.minutes == 0:
            return
        self.hours = self.hours + int(self.minutes / 60)
        self.minutes = self.minutes % 60

    def get_issue(self):
        return self.description.split(" ")[0]

    def get_description(self):
        issue = self.get_issue()
        return self.description.replace(f"{issue}", "").strip()

    def get_time_in_seconds(self):
        return self.hours * 3600 + self.minutes * 60
