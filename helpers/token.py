import os, sys

def get_token():
    config_file = os.path.join(os.path.expanduser('~'), '.todoist')
    token = None
    if os.path.isfile(config_file):
        with open(config_file) as f:
            token = f.read().strip()
    if not token:
        sys.exit('Put your Todoist API token in ~/.todoist')
    else:
        return token