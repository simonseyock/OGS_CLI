from .request_handler import *
from sgfmill import sgf
from sgfmill import sgf_moves
from colorama import Fore, Back, Style

def print_sgf(game, access_token):
    sgf_string = get('/api/v1/games/' + str(game['id']) + '/sgf/', access_token=access_token, header=1).text
    game = sgf.Sgf_game.from_string(sgf_string)
    board = [[None] * game.get_size() for _ in range(game.get_size())]
    moves = [node.get_move() for node in game.get_main_sequence()[1:]]
    for move in moves:
        board[move[1][0]][move[1][1]] = move[0]

    for row in board:
        for field in row:
            if field is None:
                print(Back.YELLOW + '  ', end='')
            elif field == 'b':
                print(Back.YELLOW + Fore.BLACK + u'\u25cf', end='')
            elif field == 'w':
                print(Back.YELLOW + Fore.WHITE + u'\u25cf', end='')
        print(Back.WHITE + '')

    print(Style.RESET_ALL)
