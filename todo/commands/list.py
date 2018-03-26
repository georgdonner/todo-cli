import os, sys
from datetime import datetime, timedelta, timezone
from todo.helpers.token import get_token
from todoist.api import TodoistAPI
from colorama import Fore

api = TodoistAPI(get_token())
api.sync()

def list_items(args):
    items = [i for i in api.state['items'] if i['checked'] == 0]
    if not args.all:
        filtered_projects = [proj for proj in api.state['projects'] if proj['name'].lower() == args.project.lower()]
        if len(filtered_projects) > 0:
            project_id = filtered_projects[0]['id']
            items = [item for item in items if item['project_id'] == project_id]
        else:
            sys.exit('Project not found')
    sorted_items = sort_items(items)
    print_items(sorted_items)

def get_date(date_string):
    return datetime.strptime(date_string, '%a %d %b %Y %H:%M:%S %z')

def sort_items(items):
    due = [] # items with a due date
    not_due = []
    for item in items:
        if item['due_date_utc']:
            due.append(item)
        else:
            not_due.append(item)
    due.sort(key=lambda item: get_date(item['due_date_utc']))
    not_due.sort(key=lambda item: get_date(item['date_added']), reverse=True)
    due.extend(not_due)
    return due

def print_items(items):
    for item in items:
        line = Fore.RESET + item['content']
        if item['due_date_utc']:
            due = get_date(item['due_date_utc'])
            if (due - datetime.now(timezone.utc)) < timedelta(1):
                line += Fore.RED
            elif (due - datetime.now(timezone.utc)) < timedelta(3):
                line += Fore.LIGHTYELLOW_EX
            else:
                line += Fore.LIGHTGREEN_EX
            line += ' ' + due.strftime('%a %d %b')
        print(line)