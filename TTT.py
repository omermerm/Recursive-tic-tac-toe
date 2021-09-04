#!/usr/bin/env python3

import sys, pygame
import numpy as np

pygame.init()

SIZE = WIDTH, HEIGHT = 600, 800
BLACK = 0, 0, 0
GREEN = 0, 128, 0
ORANGE = 180, 128, 0
RED = 200, 0 , 0
BLUE = 0, 0, 200
BROWN = 128, 128, 128
DIM = 3
X, Y = 0, 1

WIN_TRIPLES = \
        [[(i, j) for j in range(DIM)] for i in range(DIM)] + \
        [[(i, j) for i in range(DIM)] for j in range(DIM)] + \
        [[(i, i) for i in range(DIM)], [(i, (DIM-1)-i) for i in range(DIM)]]

grid_dims = WIDTH, WIDTH
grid_loc = 0, HEIGHT-WIDTH
cell_dims = cell_width, cell_height = grid_dims[X] // DIM, grid_dims[Y] // DIM
cell_locs = [[(grid_loc[X] + i*(cell_width), grid_loc[Y] + j*(cell_height)) for j in range(DIM)] for i in range(DIM)] #coords of top left point of each cell in the board grid

cell_contents = [[None for j in range(DIM)] for i in range(DIM)]
screen = pygame.display.set_mode(SIZE)
grid_sprite = pygame.transform.smoothscale(pygame.image.load("empty-tic-tac-toe-gray.png").convert_alpha(), grid_dims)
X_sprite = pygame.transform.smoothscale(pygame.image.load("red-splatter.png").convert_alpha(), cell_dims)
O_sprite = pygame.transform.flip(pygame.transform.smoothscale(pygame.image.load("blue-splatter.png").convert_alpha(), cell_dims), True, True)

myfont = pygame.font.SysFont('Comic Sans MS', 100)
header_dic = {'X':myfont.render('Red won!', True, RED),
              'O':myfont.render('Blue won!', True, BLUE),
              'T':myfont.render('Nobody won!', True, BROWN)}

cell_contents = cur_player = winner = grid = None

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
    i,j = cell[X], cell[Y]
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

    init_game()
    while(not winner):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                i,j = get_cell(event.pos)
                if not cell_contents[i][j]: add_symbol((i,j))

        screen.fill(BLACK)
        screen.blit(grid, cell_locs[0][0])
        
        mo_i, mo_j = get_cell(pygame.mouse.get_pos())
        mo_col = ORANGE if cell_contents[mo_i][mo_j] else GREEN
        pygame.draw.rect(screen, mo_col, pygame.Rect(cell_locs[mo_i][mo_j], cell_dims), width=5, border_radius=1) # highlight cell mouse is over

        pygame.display.flip()


    #screen.fill(BLACK)
    #screen.blit(grid, cell_locs[0][0])
    screen.blit(header_dic[winner], (0,0))
    stay = True
    pygame.display.flip()

    while stay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT: stay = False


        
    