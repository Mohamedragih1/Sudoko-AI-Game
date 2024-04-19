from itertools import product

class SudokuSolver:
    def __init__(self):
        self.domains = {}
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def initialize_domains(self, puzzle):
        self.grid = puzzle
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

    def get_neighbors(self, var):
        row, col = var
        neighbors = set()
        for i in range(9):
            neighbors.add((row, i))
            neighbors.add((i, col))
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                neighbors.add((i, j))
        neighbors.remove(var)
        return neighbors

    def get_solution(self):
        solution = [[0 for _ in range(9)] for _ in range(9)]
        for var in self.domains:
            row, col = var
            if len(self.domains[var]) == 1:
                solution[row][col] = next(iter(self.domains[var]))
            else:
                return None
        return solution


