from request_handler import *


def get_games(user, access_token):
    games = get('/api/v1/me/games/', access_token=access_token).json()['results']
    game_details = []
    for (i, game) in enumerate(games, 1):
        game_detail = get(game['related']['detail']).json()

        if game_detail['players']['white']['id'] == user['id']:
            opponent = game_detail['players']['black']
        else:
            opponent = game_detail['players']['white']

        if game_detail['gamedata']['clock']['current_player'] == user['id']:
            active_player = user
        else:
            active_player = opponent
        print('{key}) {player1} (B) vs {player2} (W) | {active_player} to move.'.format(
            key = i,
            active_player = active_player['username'],
            player1 = game_detail['players']['black']['username'],
            player2 = game_detail['players']['white']['username'])
        )
        game_details.append(game_detail)
    return games, game_details


def choose_game(user, access_token):
    games, game_details = get_games(user, access_token)
    
    key = input("Choose game (number): ")
    while 1:
        try:
            return games[key - 1]['related']['detail'], game_details[key - 1]
        except Exception as _:
            print('invalid key, try again: ')


### for debugging
def choose_first_game(user, access_token):
    games, game_details = get_games(user, access_token)
    key = 2
    return games[key - 1]['related']['detail'], game_details[key - 1]
