import requests
import yaml
import getpass
from .game import *
from .request_handler import *
from .overview import *
import sys
import colorama


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


def choose_option(num_options):
    while True:
        key = input("Choose option: ")
        try:
            key = int(key)
            if key > num_options or key < 1:
                print('invalid option, try again: ')
            else:
                return key
        except ValueError:
            print('invalid option, try again: ')


def choose_from_game_options(user, game):
    num_options = 1
    print('Actions:\n'
          '1) Back to selection')
    if is_user_to_move(user, game):
        print('2) Make move')
        num_options = 2
    return choose_option(num_options)

        

def main():
    colorama.init()
    print('Press Ctrl+C to quit.')
    # user, access_token = login()
    user, access_token = debug_login()
    if access_token == 0:
        sys.exit()

    while True:
        # game = choose_game(user, access_token)
        game_details = get_game_details(user, access_token)
        print_overview(user, game_details)

        key = choose_option(len(game_details))

        game = game_details[key-1]

        board = get_board_from_sgf(game, access_token)
        print_board(board)
    
        key = choose_from_game_options(user, game)
        if key == 2:
            move = make_move(board, user, game)
            print_board(board)
        

if __name__ == '__main__':
    main()

