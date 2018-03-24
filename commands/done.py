import re, os, sys
from datetime import datetime, timedelta, timezone
from helpers.token import get_token
from todoist.api import TodoistAPI
from colorama import Fore

api = TodoistAPI(get_token())
api.sync()

def item_done(args):
    items = [i for i in api.state['items'] if i['checked'] == 0]
    done = []
    for item in items:
        if (re.search(args.pattern, item['content'], flags=re.IGNORECASE)):
            done.append(item)
    if len(done) < 1:
        print('Nothing found :(')
    elif len(done) == 1:
        set_done(done[0])
        api.commit()
    else:
        select_items(items)
        api.commit()

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

def get_project_name(item):
    return api.projects.get_by_id(item['project_id'])['name']

def select_items(items):
    print('There are multiple todos matching your query:')
    for index, item in enumerate(items):
        message = '{0} - '.format(index)
        message += Fore.LIGHTYELLOW_EX + item['content'] + ' ' + Fore.RESET + 'in project '
        message += Fore.LIGHTYELLOW_EX + get_project_name(item) + Fore.RESET
        print(message)
    select_input = input('Please select the ones you want to mark as done: ')
    if select_input == '':
        sys.exit('None deleted')
    indexes = select_input.split(',')
    for index_string in indexes:
        try:
            index = int(index_string.strip())
            item = items[index]
            set_done(item)
        except ValueError:
            sys.exit('Invalid input, please provide a comma-separated sequence of numbers')

def set_done(item):
    to_complete = api.items.get_by_id(item['id'])
    to_complete.complete()
    message = Fore.LIGHTYELLOW_EX + item['content'] + ' ' + Fore.RESET + 'in project '
    message += Fore.LIGHTYELLOW_EX + get_project_name(item) + Fore.RESET + ' marked as done.'
    print(message)