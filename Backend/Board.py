import numpy as np
from itertools import product

class Board:
    def __init__(self, size):
        self.dim = 3 * size
        self.board = np.zeros((self.dim, self.dim))
        self.domains = {}
    
    # Initialize board and domains
    def init_board(self, board):
        self.board = board
        for i, j in product(range(self.dim), repeat=2):
            if board[i][j] != 0:
                self.domains[(i, j)] = {board[i][j]}
            else:
                self.domains[(i, j)] = set(range(1, 10))
    
    # Get all numbers in the same row, column and block            
    def get_neighbors(self, var):
        row, col = var
        neighbors = set()  # Data structure (set)

        # Add neighbors in the same row or columns
        for i in range(self.dim):
            neighbors.add((row, i))
            neighbors.add((i, col))

        start_row, start_col = (row // 3) * 3, (col // 3) * 3

        # Add neighbors in the same block
        for i in range(start_row, start_row + self.dim//3):
            for j in range(start_col, start_col + self.dim//3):
                neighbors.add((i, j))

        neighbors.remove(var)  # Don't include the cell itself

        return neighbors