from abc import ABC, abstractmethod

import pygame as pg
from pygame import transform
from pygame import Surface


class Tile(ABC):

    def __init__(self):
        self.won = None  # this attribute holds the winner of the board if one exists, or None otherwise. Used for boolean checks.

    '''
    Method with which plays are made.
    Returns True iff tile was won because of this play.
    '''
    @abstractmethod
    def play(self, symbol, coord) -> bool:
        pass

    '''
    Getter of who won the board, or None if no one has
    '''
    def get_winner(self):
        return self.won

    '''
    Returns a pygame surface visualizing the current state of the tile
    '''
    @abstractmethod
    def get_visual(self):
        pass


#   Tic-Tac-Toe classes

class TTTConst:
    DIM = 3
    OK_SYMB = {'X', 'O'}
    COLORS = {'X':(0,0,200), 'O':(200,0,0)} # x - blue, o- red
    GRID_SPRITE = transform.smoothscale(pg.image.load("empty-tic-tac-toe-gray.png").convert_alpha(), (900,900))
    P1_SPRITE = transform.smoothscale(pg.image.load("red-splatter.png").convert_alpha(), (300,300))
    P2_SPRITE = transform.flip(transform.smoothscale(pg.image.load("blue-splatter.png").convert_alpha(), (300,300)), True, True)



class TTTBoard(Tile):

    DIM = 3

    '''
    winning sets: rows, columns, diagonals
    '''
    WIN_TRIPLES = \
        [[(i, j) for j in range(TTTConst.DIM)] for i in range(TTTConst.DIM)] + \
        [[(i, j) for i in range(TTTConst.DIM)] for j in range(TTTConst.DIM)] + \
        [[(i, i) for i in range(TTTConst.DIM)], [(i, (TTTConst.DIM-1)-i) for i in range(TTTConst.DIM)]]

    '''
    create new board of depth=n containing a grid of baords/tiles of depth=n-1.
    if provided with a surface, create this board's susrface as a subsurface of the one provided, with top left corner at offset.
    '''
    def __init__(self, depth=1, size, parent_surface=None, offset=(0,0)):
        assert depth > 0, 'TTTBoard must have positive depth'
        super().__init__()
        self.depth = depth
        self.size = size
        self.initialize_board(size, parent_surface, offset)

    def __repr__(self):
        board_strs = []
        for i in range(TTTConst.DIM):
            board_strs.append([])
            for j in range(TTTConst.DIM):
                board_strs[i].append(str(self.board[i][j]))
        if self.depth == 1:
            return '\r\n'.join([' '.join(board_strs[i]) for i in range(TTTConst.DIM)])
        else:
            ans = ''
            for i in range(TTTConst.DIM):
                for j in range(TTTConst.DIM):
                    ans += 'cell ' + str((i, j)) + ':' + '\r\n' + \
                            board_strs[i][j] + \
                            '\r\n'
            return ans

    '''
    Create a DIMxDIM array of empty boards of lower depth (tiles, if depth 1). Also initialize visuals.
    '''
    def initialize_board(self, size, parent_surface, offset):
        # create surface and draw empty grid
        self.surface = parent_surface.subsurface(pg.Rect(offset, (size,size))) if parent_surface else Surface(size, size)
        transform.smoothscale(TTTConst.GRID_SPRITE, (size, size), self.surface)
        
        # initialize cell locations relative to board, cell themselves, and draw result on surface
        cell_size = size / TTTConst.DIM
        self.cell_locs = [[(cell_size*j, cell_size*i) for j in range(TTTConst.DIM)] for i in range(TTTConst.DIM)]
        self.board = []
        for r in range(TTTConst.DIM):
            self.board.append([])
            for c in range(TTTConst.DIM):
                self.board[r].append(TTTTile() if self.depth == 1 else TTTBoard(depth=self.depth-1, cell_size, self.surface, self.cell_locs[r][c]))
                #self.draw_cell(r,c)
    '''
    Receives a symbol to play and a list of pairs of length self.depth with the outermost coordinate first
    Return True if coordinate was won by play, False if win status of coordinate didn't change
    '''
    def play(self, symbol, coord_list):
        assert len(coord_list) == self.depth, 'Coordinate-depth mismatch'
        assert symbol in TTTConst.OK_SYMB, 'The only allowed plays are: ' + str(TTTConst.OK_SYMB)
        (r, c) = coord_list[0]
        coord_won = self.board[r][c].play(symbol, coord_list[1:])
        #self.draw_cell(r,c)
        return coord_won

    '''
    updates self.won, the victory status of the board.
    Return true iff victory status has changed since last check
    '''
    def update_victory(self):
        if not self.won:
            for condition in TTTBoard.WIN_TRIPLES:
                win_status = [self.board[x][y].get_winner() for (x, y) in condition]
                if len(set(win_status)) == 1 and win_status[0]:  # if all three cells respond with the same non-None symbol, it has won
                    self.won = win_status[0]
                    self.color_grid(TTTConst.COLORS[win_status[0]])
                    return True
        return False

    '''
    draws current state of the (r,c) cell onto the board's surface
    '''
    #def draw_cell(self, r, c):
    #    self.surface.blit(self.board[r][c].get_visual(), self.cell_locs[r][c])
    
    '''
    changes the grid color.
    called when a player has won the board.
    '''
    def color_grid(self, color):
        w, h = self.surface.get_size()
        r, g, b = color
        for x in range(w):
            for y in range(h):
                a = self.surface.get_at((x, y))[3]
                self.surface.set_at((x, y), pg.Color(r, g, b, a))

class TTTTile(Tile):

    def __init__(self):
        super().__init__()

    def __repr__(self):
        if self.get_winner():
            return self.get_winner()
        else:
            return '.'

    def play(self, symbol, coord_list=[]):
        assert coord_list in [[], (0, 0)], 'TTTTile cannot receive coordinates other than (0,0)'
        assert self.won is None, 'TTTTile was already won/played on'
        assert symbol in TTTConst.OK_SYMB, 'The only allowed plays are: ' + str(TTTConst.OK_SYMB)
        self.won = symbol
        return True
