import requests
import yaml

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


def request(req_func, endpoint: str, data=None, access_token=None):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    if access_token is not None:
        headers['authorization'] = 'Bearer ' + access_token
    url = config['api'] + endpoint
    return req_func(url, data=data, headers=headers)


def post(endpoint: str, data, access_token=None):
    return request(requests.post, endpoint, data, access_token=access_token)


def get(endpoint: str, access_token=None):
    return request(requests.get, endpoint, access_token=access_token)


def login():
    uname = input("enter username: ")
    pw = input("enter password: ")
    response = post('/oauth2/token/', {
        'client_id': secrets['client_id'],
        'client_secret': secrets['client_secret'],
        'grand_type': 'password',
        'username': uname,
        'password': pw
    })
    return uname, response.json()['access_token']


def debug_login():
    access_token = post('/oauth2/token/', {
        'client_id': secrets['client_id'],
        'client_secret': secrets['client_secret'],
        'grant_type': 'password',
        'username': config['debug_user'],
        'password': config['debug_password']
    }).json()['access_token']
    return get('/api/v1/me/', access_token=access_token).json(), access_token


def list_open_games(user, access_token):
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
            player2 = game_detail['players']['white']['username']))

        game_details.append(game_detail)
    return game_details


def choose_game(user, access_token):
    games = list_open_games(user, access_token)
    key = int(input("Choose game (number): "))
    return games[key - 1]


if __name__ == '__main__':
    user, access_token = debug_login()
    game = choose_game(user, access_token)
    print(game)