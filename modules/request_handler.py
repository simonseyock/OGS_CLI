import requests


def request(req_func, endpoint: str, data=None, access_token=None, header=0):
    headers = [{'content-type': 'application/x-www-form-urlencoded'},
               {'content-type': 'application/x-go-sgf'}]
    headers = headers[header]
    if access_token is not None:
        headers['authorization'] = 'Bearer ' + access_token
    # url = config['api'] + endpoint
    url = 'https://beta.online-go.com' + endpoint
    return req_func(url, data=data, headers=headers)

def post(endpoint: str, data, access_token=None, header=0):
    return request(requests.post, endpoint, data, access_token=access_token)


def get(endpoint: str, access_token=None, header=0):
    return request(requests.get, endpoint, access_token=access_token, header=header)
