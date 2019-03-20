from .request_handler import *
from sgfmill import sgf
from sgfmill import sgf_moves

def print_sgf(game, access_token):
    sgf_string = get('/api/v1/games/' + str(game['id']) + '/sgf/', access_token=access_token, header=1).text
    game = sgf.Sgf_game.from_string(sgf_string)
    board = [[None] * game.get_size()] * game.get_size()
    moves = [node.get_move() for node in game.get_main_sequence()[1:]]
    for move in moves:
        board[move[1][0]][move[1][1]] = move[0]
    #TODO: print


def parse_sgf(sgf):
    board = []
    return board


def print_board(sgf):
    board = parse_sgf(sgf)
    pass
