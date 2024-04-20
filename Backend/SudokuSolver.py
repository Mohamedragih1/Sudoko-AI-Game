class SudokuSolver:
    def __init__(self, board):
        self.board = board
        
    def revise_domain(self, var_i, var_j):
        revised = False
        for val_i in self.board.domains[var_i].copy():
            consistent = any(val_j for val_j in self.board.domains[var_j] if val_j != val_i)
            if not consistent:
                self.board.domains[var_i].remove(val_i)
                revised = True
        return revised

    def apply_arc_consistency(self):
        arcs = [(var_i, var_j) for var_i in self.board.domains for var_j in self.board.get_neighbors(var_i)]
        while arcs:
            var_i, var_j = arcs.pop(0)
            if self.revise_domain(var_i, var_j):
                if len(self.board.domains[var_i]) == 0:
                    return False
                arcs.extend([(var_k, var_i) for var_k in self.board.get_neighbors(var_i) if var_k != var_j])
        return True

    def get_solution(self):
        solution = [[0 for _ in range(9)] for _ in range(self.board.dim)]
        for var in self.board.domains:
            row, col = var
            if len(self.board.domains[var]) == 1:
                solution[row][col] = next(iter(self.board.domains[var]))
            else:
                return None
        return solution