from itertools import product
from collections import deque
import numpy as np
import random

class SudokuSolver:
    def __init__(self):
        self.domains = {}
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def initialize_domains(self, puzzle):
        
        self.grid = puzzle
        print(self.grid)
        for i, j in product(range(9), repeat=2):
            if puzzle[i][j] != 0:
                self.domains[(i, j)] = {puzzle[i][j]}
            else:
                self.domains[(i, j)] = set(range(1, 10))

    def revise_domain(self, var_i, var_j):
        revised = False
        for val_i in self.domains[var_i].copy():
            consistent = any(val_j for val_j in self.domains[var_j] if val_j != val_i)
            if not consistent:
                self.domains[var_i].remove(val_i)
                revised = True
        return revised

    def apply_arc_consistency(self):
        arcs = [(var_i, var_j) for var_i in self.domains for var_j in self.get_neighbors(var_i)]
        while arcs:
            var_i, var_j = arcs.pop(0)
            if self.revise_domain(var_i, var_j):
                if len(self.domains[var_i]) == 0:
                    return False
                arcs.extend([(var_k, var_i) for var_k in self.get_neighbors(var_i) if var_k != var_j])
        return True

    

    def get_solution(self):
        solution = [[0 for _ in range(9)] for _ in range(9)]
        for var in self.domains:
            row, col = var
            if len(self.domains[var]) == 1:
                solution[row][col] = next(iter(self.domains[var]))
            else:
                return None
        return solution

    def is_valid_solution(self, solution):
        for i in range(9):
            for j in range(9):
                if not self.is_valid_cell(solution, i, j):
                    return False
        return True

    def is_valid_cell(self, solution, row, col):
        num = solution[row][col]
        # Check row
        if any(solution[row][c] == num and c != col for c in range(9)):
            return False
        # Check column
        if any(solution[r][col] == num and r != row for r in range(9)):
            return False
        # Check subgrid
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        if any(solution[r][c] == num and (r, c) != (row, col) for r in range(start_row, start_row + 3) for c in range(start_col, start_col + 3)):
            return False
        return True

    def generate_random_puzzle(self, num_filled_cells=60):
        # Initialize an empty grid
        puzzle = [[0 for _ in range(9)] for _ in range(9)]
        # Fill num_filled_cells random cells
        filled_cells = set()
        while len(filled_cells) < num_filled_cells:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if (row, col) not in filled_cells:
                num = random.randint(1, 9)
                puzzle[row][col] = num
                if self.is_valid_cell(puzzle, row, col):
                    filled_cells.add((row, col))
                else:
                    puzzle[row][col] = 0

        return puzzle