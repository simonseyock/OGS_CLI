import json

from .request_handler import *


def get_games(user, access_token):
    games = get('/api/v1/me/games/', access_token=access_token).json()['results']
    game_details = []
    i = 1
    for game in games:
        game_detail = get(game['related']['detail']).json()

        if game_detail['ended'] is None:
            if game_detail['players']['white']['id'] == user['id']:
                opponent = game_detail['players']['black']
            else:
                opponent = game_detail['players']['white']

            if game_detail['gamedata']['clock']['current_player'] == user['id']:
                active_player = user
            else:
                active_player = opponent
            print('{key}) {player1} (B) vs {player2} (W) | {active_player} to move.'.format(
                key=i,
                active_player=active_player['username'],
                player1=game_detail['players']['black']['username'],
                player2=game_detail['players']['white']['username'])
            )
            game_details.append(game_detail)
            i += 1
    return game_details


def choose_game(user, access_token):
    game_details = get_games(user, access_token)

    while True:
        key = input("Choose game (number): ")
        try:
            key = int(key)
            break
        except ValueError:
            print('invalid key, try again: ')

    return game_details[key - 1]


### for debugging
def choose_first_game(user, access_token):
    game_details = get_games(user, access_token)
    return game_details[0]
