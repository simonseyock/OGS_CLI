from .request_handler import *
from sgfmill import sgf
from sgfmill import sgf_moves
from colorama import Fore, Back, Style

def print_sgf(game, access_token):
    sgf_string = get('/api/v1/games/' + str(game['id']) + '/sgf/', access_token=access_token, header=1).text
    game = sgf.Sgf_game.from_string(sgf_string)
    board = [[None] * game.get_size() for _ in range(game.get_size())]
    moves = [node.get_move() for node in game.get_main_sequence()[1:]]
    board[3][3] = '*'
    board[3][9] = '*'
    board[3][15] = '*'
    board[9][3] = '*'
    board[9][9] = '*'
    board[9][15] = '*'
    board[15][3] = '*'
    board[15][9] = '*'
    board[15][15] = '*'
    for move in moves:
        board[move[1][0]][move[1][1]] = move[0]


    star = u'\u2795'
    cross = u'\uff0b'
    stone = u'\u2b24 '

    for row in board:
        for field in row:
            if field is None:
                print(Back.YELLOW + Fore.BLACK + cross, end='')
            elif field == '*':
                print(Back.YELLOW + Fore.BLACK + star, end='')
            elif field == 'b':
                print(Back.YELLOW + Fore.BLACK+ stone, end='')
            elif field == 'w':
                print(Back.YELLOW + Fore.WHITE + stone, end='')
            
        print(Style.RESET_ALL)

    print(Style.RESET_ALL)
