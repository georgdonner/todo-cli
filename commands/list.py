import os, sys
from datetime import datetime, timedelta, timezone
from todoist.api import TodoistAPI
from colorama import Fore

api = TodoistAPI(os.environ['TODOIST_TOKEN'])
api.sync()

def list_items(args):
    items = api.state['items'] # all items
    if not args.all:
        filtered_projects = [proj for proj in api.state['projects'] if proj['name'].lower() == args.project.lower()]
        if len(filtered_projects) > 0:
            project_id = filtered_projects[0]['id']
            def is_relevant(item, project):
                return item['project_id'] == project_id and item['checked'] == 0
            items = [item for item in api.state['items'] if is_relevant(item, project_id)]
        else:
            sys.exit('Project not found')
    print_items(items)

def print_items(items):
    for index, item in enumerate(items):
        line = Fore.RESET + '{0} - {1}'.format(hex(index)[2:], item['content'])
        if item['due_date_utc']:
            due = datetime.strptime(item['due_date_utc'], '%a %d %b %Y %H:%M:%S %z')
            if (due - datetime.now(timezone.utc)) < timedelta(1):
                line += Fore.RED
            elif (due - datetime.now(timezone.utc)) < timedelta(3):
                line += Fore.LIGHTYELLOW_EX
            else:
                line += Fore.LIGHTGREEN_EX
            line += ' ' + due.strftime('%a %d %b')
        print(line)