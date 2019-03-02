import json
import requests
import yaml


### API DOCS = https://ogs.docs.apiary.io/

with open('secrets.yml', 'r') as stream:
    try:
        secrets = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

api = 'https://beta.online-go.com'

def request(req_func, endpoint: str, data=None, access_token=None):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    if access_token is not None:
        headers['authorization'] = 'Bearer ' + access_token
    url = api + endpoint
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
    return response.json()['access_token']

def debug_login():
    uname = 'PinkPanther'
    pw = 'test1'
    response = post('/oauth2/token/', {
        'client_id': secrets['client_id'],
        'client_secret': secrets['client_secret'],
        'grant_type': 'password',
        'username': uname,
        'password': pw
    })
    return response.json()['access_token']


def list_open_games(access_token):
    response = get('/api/v1/me/games/', access_token=access_token)
    print(response.json())


if __name__ == '__main__':
    access_token = debug_login()
    list_open_games(access_token)