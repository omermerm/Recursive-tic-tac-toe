
class TTTBoard(Tile):
    #winning sets: rows, columns, diagonals
    WIN_TRIPLES = [[(i,j) for j in range(3)] for i in range(3)] + \
                   [(i,j) for i in range(3)] for j in range(3)] + \
                   [[(i,i) for i in range(3)], [(i, 2-i) for i in range(3)]]

    def __init__(self, depth=1):
        assert depth > 0, 'TTTBoard must have positive depth'
        self.depth = depth
        initialize_board()
        self.won = None # this attribute holds the winner of the board if one exists, or None otherwise. Used for boolean checks.

    '''
    Create a 3x3 board made out of empty boards of lower depth (or tiles, in case depth is 1)
    '''
    def initialize_board(self):
        self.board = []
        for i in range(3):
            self.board.append([])
            for j in range(3):
                self.board.append(TTTTile() if self.depth == 1 else TTTBoard(depth=self.depth-1))
    
    '''
    receives a symbol to play and a list of pairs of length self.depth with the outermost coordinate first
    returns True if coordinate was won, False if win status of coordinate didn't change
    '''
    def play(self, symbol, coord_list):
        assert len(coord_list) == self.depth, 'Coordinate-depth mismatch'
        assert symbol in {'X', 'O'}, 'The only allowed plays are X and O'
        (x,y) = coord_list[0]
        if self.board[x][y].play(symbol. coord_list[1:]):
            return update_victory()
        return False

    '''
    updates self.won, the victory status of the board. Return true iff victory status has changed since last check
    '''
    def check_victory(self):
        if not self.won:
            for condition in TTTBoard.WIN_TRIPLES:
                win_status = [board[x][y].get_winner() for (x,y) in condition]
                if len(set(win_status)) == 1 and win_status[0]: #if all three cells respond with the same non-None symbol, it has won
                    self.won = win_status[0]
                    return True
        return False

    '''
    Getter of who won the board
    '''
    def get_winner(self):
        return self.won

class TTTTile(Tile):
