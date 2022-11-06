import requests
import json
import os
import sys
from datetime import datetime

API_KEY = os.environ["api_key"]
USER_ID = os.environ["user_id"]
WORKSPACE_ID = os.environ["workspace_id"]
BASE_ENDPOINT = "https://api.clockify.me/api/v1"
HEADERS = {"X-Api-Key": API_KEY, "content-type":"application/json"}

class Clockify:

    @staticmethod
    def start_entry(arg):
        sys.stderr.write(f"starting with args: {arg}\n")
        url = BASE_ENDPOINT + f"/workspaces/{WORKSPACE_ID}/time-entries"
        payload = {"start": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
        if "desc" in arg:
            payload["description"] = arg["desc"]
        if "project_id" in arg:
            payload["projectId"] = arg["project_id"]
        if "task_id" in arg:
            payload["taskId"] = arg["task_id"]
        r = requests.post(url, headers=HEADERS, data=json.dumps(payload))
        sys.stderr.write(f"result of start: {r}, payload: {payload}\n")

    @staticmethod
    def stop_entry(arg):
        url = BASE_ENDPOINT + f"/workspaces/{WORKSPACE_ID}/user/{USER_ID}/time-entries"
        payload = {"end": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
        r = requests.patch(url, headers=HEADERS, data=json.dumps(payload))
        sys.stderr.write(f"result of stop: {r}, {r.reason}")


arg = json.loads(sys.argv[1])

sys.stderr.write(f"called with args: {arg}\n")
if arg["action"] == "start":
    Clockify.start_entry(arg)
elif arg["action"] == "stop":
    Clockify.stop_entry(arg)
