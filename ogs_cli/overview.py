import json

from .request_handler import *
from .game import is_user_to_move


def get_game_details(user, access_token):
    games = get('/api/v1/me/games/', access_token=access_token).json()['results']
    game_details = []
    i = 1
    for game in games:
        game_detail = get(game['related']['detail']).json()

        if game_detail['ended'] is None:
            game_details.append(game_detail)
            i += 1
    return game_details


def print_overview(user, game_details):
    for i, game_detail in enumerate(game_details, 1):
        if game_detail['players']['white']['id'] == user['id']:
            opponent = game_detail['players']['black']
        else:
            opponent = game_detail['players']['white']
            
        if is_user_to_move(user, game_detail) == True:
            active_player = user
        else:
            active_player = opponent
        print('{key}) {player1} (B) vs {player2} (W) | {active_player} to move.'.format(
                key=i,
                active_player=active_player['username'],
                player1=game_detail['players']['black']['username'],
                player2=game_detail['players']['white']['username'])
        )


def choose_game(user, access_token):
    game_details = get_games(user, access_token)
    return game_details[key - 1]


### for debugging
def choose_first_game(user, access_token):
    game_details = get_games(user, access_token)
    return game_details[0]
