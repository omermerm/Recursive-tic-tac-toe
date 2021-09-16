#!/usr/bin/env python3

import sys
import pygame as pg

# initialize pg and display
pg.init()
SIZE = WIDTH, HEIGHT = 900, 1100
screen = pg.display.set_mode(SIZE)
# import tiles only after pg and display are initialized
from tiles import TTTBoard

BLACK = 0, 0, 0
GREEN = 0, 128, 0
ORANGE = 180, 128, 0
RED = 200, 0, 0
BLUE = 0, 0, 200
BROWN = 128, 128, 128
DIM = 3
X, Y = 0, 1

WIN_TRIPLES = \
        [[(i, j) for j in range(DIM)] for i in range(DIM)] + \
        [[(i, j) for i in range(DIM)] for j in range(DIM)] + \
        [[(i, i) for i in range(DIM)], [(i, (DIM-1)-i) for i in range(DIM)]]

grid_dims = WIDTH, WIDTH
board_loc = 0, HEIGHT-WIDTH

DEPTH = 1

cell_contents = [[None for j in range(DIM)] for i in range(DIM)]

board = TTTBoard(depth=DEPTH, parent_surface=screen, offset=board_loc)

myfont = pg.font.SysFont('Comic Sans MS', 100)  # Comic Sans, just because.
header_dic = {'X': myfont.render('Red won!', True, RED),
              'O': myfont.render('Blue won!', True, BLUE),
              'T': myfont.render('Nobody won!', True, BROWN)}

cell_contents = cur_player = winner = grid = None


def loc_to_coords(loc):
    global board
    return board.loc_to_coords((loc[X] - board_loc[X], loc[Y] - board_loc[Y]))

def init_game():
    global cell_contents, cur_player, winner, grid
    cell_contents = [[None for j in range(DIM)] for i in range(DIM)]
    cur_player = 'X'
    winner = None
    grid = grid_sprite.copy()


def get_cell_loc(coords):
    x_idx, y_idx = min(max((coords[X] - grid_loc[X]) // cell_width, 0), DIM-1), min(max((coords[Y] - grid_loc[Y]) // cell_width, 0), DIM-1)
    return cell_locs[x_idx][y_idx]


def get_cell(coords):
    return min(max((coords[X] - grid_loc[X]) // cell_width, 0), DIM-1), min(max((coords[Y] - grid_loc[Y]) // cell_width, 0), DIM-1)


def get_grid_cell_loc(cell):
    i, j = cell[X], cell[Y]
    return [cell_locs[i][j][X] - grid_loc[X], cell_locs[i][j][Y] - grid_loc[Y]]


def add_symbol(cell):
    global cur_player
    cell_contents[cell[X]][cell[Y]] = cur_player
    if cur_player == 'X':
        player_surf, cur_player = X_sprite, 'O'
    else:
        player_surf, cur_player = O_sprite, 'X'
    grid.blit(player_surf, get_grid_cell_loc(cell))
    check_win()


def check_win():
    global winner
    for condition in WIN_TRIPLES:
        win_status = [cell_contents[i][j] for (i, j) in condition]
        if len(set(win_status)) == 1 and win_status[0]:  # if all three cells respond with the same non-None symbol, it has won
            winner = win_status[0]
            break

    if all([all(row) for row in cell_contents]):
        winner = 'T'


while True:

    #init_game()
    screen.fill(BLACK)
    while(not board.get_winner()):
        forced_coords = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
                coords = loc_to_coords(event.pos)
                if coords[:-1] == forced_coords:
                    board.play(coords)

        #mo_i, mo_j = get_cell(pg.mouse.get_pos())
        #mo_col = ORANGE if cell_contents[mo_i][mo_j] else GREEN
        #pg.draw.rect(screen, mo_col, pg.Rect(cell_locs[mo_i][mo_j], cell_dims), width=5, border_radius=1)  # highlight cell mouse is over

        pg.display.flip()

    screen.blit(header_dic[board.get_winner()], (0, 0))
    stay = True
    pg.display.flip()

    while stay:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
                stay = False
