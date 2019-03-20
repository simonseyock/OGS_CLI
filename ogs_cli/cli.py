import requests
import yaml
import getpass
from .game import *
from .request_handler import *
from .overview import *
import sys


### API DOCS = https://ogs.docs.apiary.io/

with open('secrets.yml', 'r') as stream:
    try:
        secrets = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open('config.yml', 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)


def login():
    uname = input("enter username: ")
    pw = getpass.getpass("enter password: ")    
    response = post('/oauth2/token/', {
        'client_id': secrets['client_id'],
        'client_secret': secrets['client_secret'],
        'grant_type': 'password',
        'username': uname,
        'password': pw
    }).json()
    try:
        print(response['error_description'])
        return 0, 0
    except Exception as _:
        pass
    access_token = response['access_token']
    return get('/api/v1/me/', access_token=access_token).json(), access_token


def debug_login():
    access_token = post('/oauth2/token/', {
        'client_id': secrets['client_id'],
        'client_secret': secrets['client_secret'],
        'grant_type': 'password',
        'username': config['debug_user'],
        'password': config['debug_password']
    }).json()['access_token']
    return get('/api/v1/me/', access_token=access_token).json(), access_token


def main():
    # user, access_token = login()
    user, access_token = debug_login()
    if access_token == 0:
        sys.exit()
    game_id, game_details = choose_first_game(user, access_token)
    sgf = get_sgf(game_id, access_token)
    print(sgf)
