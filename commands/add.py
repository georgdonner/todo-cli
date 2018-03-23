import re, os, sys
from datetime import datetime, timedelta, timezone
from todoist.api import TodoistAPI
from colorama import Fore

api = TodoistAPI(os.environ['TODOIST_TOKEN'])
api.sync()

def add_item(args):
    project = [p for p in api.state['projects'] if p['name'].lower() == args.project.lower()]
    if len(project) != 1:
        sys.exit('Couldn\'t determine project')
    project = project[0]
    options = {}
    if args.date:
        options['date_string'] = args.date
    item = api.items.add(args.content, project['id'], **options)
    api.commit()
    print_message(item, project)

def print_message(item, project):
    message = Fore.LIGHTYELLOW_EX + item['content'] + Fore.RESET + ' added to project '
    message += Fore.LIGHTYELLOW_EX + project['name'] + Fore.RESET
    print(message)
