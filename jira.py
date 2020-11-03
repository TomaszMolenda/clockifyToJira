import logging
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class Jira:
    token = os.getenv("jira-token")
    api = os.getenv("jira-api")
    headers = {'Authorization': f"Basic {token}"}

    # format 2020-10-30
    def add_entry(self, issue, timeSpentSeconds, date, description):
        if not description:
            description = os.getenv("default-description")
        logging.info(f"sending to jira {issue}, {date}, {timeSpentSeconds}, {description}")
        response = requests.post(
            f"{self.api}/issue/{issue}/worklog",
            headers=self.headers, json={
                'timeSpentSeconds': timeSpentSeconds,
                'started': f"{date}T00:00:00.000+0000",
                'comment': {
                    'type': 'doc',
                    'version': 1,
                    'content': [
                        {
                            'type': 'paragraph',
                            'content': [
                                {
                                    'type': 'text',
                                    'text': description,
                                }
                            ]
                        }
                    ]
                }
            })
        return response.status_code == 201
