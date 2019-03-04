from .request_handler import *


def get_sgf(game_id, access_token):
    sgf = get(game_id+'/sgf/', access_token=access_token, header=1).text
    return sgf


def parse_sgf(sgf):
    board = []
    return board


def print_board(sgf):
    board = parse_sgf(sgf)
    pass
