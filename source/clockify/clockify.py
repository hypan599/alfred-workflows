import requests
import json
import os
import sys
from datetime import datetime

API_KEY = os.environ["api_key"]
USER_ID = os.environ["user_id"]
WORKSPACE_ID = os.environ["workspace_id"]
BASE_ENDPOINT = "https://api.clockify.me/api/v1"
HEADERS = {"X-Api-Key": API_KEY}

ENTRY_ITEMS = [{"title": i[0], "subtitle": i[1], "arg":i[2]} for i in [
    ("Start", "SubStart", "start"), ("Stop", "substop", "stop")
]]


class Clockify:
    @staticmethod
    def get_projects():
        url = BASE_ENDPOINT + f"/workspaces/{WORKSPACE_ID}/projects"
        r = requests.get(url, headers=HEADERS)
        return r.json()

    @staticmethod
    def get_tasks(project_id):
        url = BASE_ENDPOINT + \
            f"/workspaces/{WORKSPACE_ID}/projects/{project_id}/tasks"
        r = requests.get(url, headers=HEADERS)
        return r.json()


class App:
    @staticmethod
    def output(result):
        print(json.dumps({"items": result}))

    @staticmethod
    def run(args):
        if args == "":
            App.output(ENTRY_ITEMS)
        if args != "":
            args = args.split(" ")
            sys.stderr.write(f"got args: {args}\n")
            if args[0] == "start":
                App.start(args)
            elif args[0] == "stop":
                App.stop()
            else:
                App.output(ENTRY_ITEMS)

    @staticmethod
    def start(args):
        projects_fetched = Clockify.get_projects()
        if not projects_fetched:
            App.output(ENTRY_ITEMS)
            return
        project_names = {i["name"].lower(): i for i in projects_fetched}
        sys.stderr.write(f"project_names: {project_names}\n")
        project_result = [{"title": i["name"], "subtitle": i["clientName"],
                           "arg":i["id"]} for i in projects_fetched]
        project_result.insert(
            0, {"title": "No Project", "subtitle": "No Project", "arg": json.dumps({"action": "start"})})
        if len(args) > 1 and args[1].lower() in project_names:
            project_id = project_names.get(args[1].lower())["id"]
            tasks_fetched = Clockify.get_tasks(project_id)
            tasks_result = [{"title": i["name"], "arg":i["id"]}
                            for i in tasks_fetched]
            task_names = {i["name"].lower(): i for i in tasks_fetched}
            tasks_result.insert(
                0, {"title": "No Task", "subtitle": "No Task", "arg": json.dumps({"action": "start"})})
            if len(args) > 2 and args[2].lower() in task_names:
                task_id = task_names.get(args[2].lower())["id"]
                params = {"action": "start",
                          "project_id": project_id, "task_id": task_id}
                if (len(args) > 3):
                    params["desc"] = args[3]
                App.output([{"title": f"Start Timer for {args[2]}",
                           "subtitle": "No Task", "arg": json.dumps(params)}])
            else:
                App.output(tasks_result)
        else:
            App.output(project_result)

    @staticmethod
    def stop():
        App.output([{"title": i[0], "subtitle": i[1], "arg":i[2]}
                   for i in [("Stop", "SubStop", json.dumps({"action": "stop"}))]])

App.run(sys.argv[1])

sys.stderr.write(f"pwd: {os.getcwd()}\n")