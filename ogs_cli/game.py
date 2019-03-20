from .request_handler import *
from sgfmill import sgf
from sgfmill import sgf_moves
from colorama import Fore, Back, Style
from wcwidth import wcswidth

def print_sgf(game, access_token):
    sgf_string = get('/api/v1/games/' + str(game['id']) + '/sgf/', access_token=access_token, header=1).text
    game = sgf.Sgf_game.from_string(sgf_string)
    board = [[None] * game.get_size() for _ in range(game.get_size())]
    moves = [node.get_move() for node in game.get_main_sequence()[1:]]
    for move in moves:
        board[move[1][0]][move[1][1]] = move[0]

    print(wcswidth(' '))
    print(wcswidth(u'\u26ab'))

    for row in board:
        for field in row:
            if field is None:
                print(Fore.YELLOW + u'\u25a0', end='')
            elif field == 'b':
                print(Fore.BLACK+ u'\u25a0', end='')
            elif field == 'w':
                print(Fore.WHITE + u'\u25a0', end='')
        print('')

    print(Style.RESET_ALL)
