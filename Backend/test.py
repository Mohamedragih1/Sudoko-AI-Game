class SudokuSolver:
    def __init__(self):
        self.domains = {}  # Initialize domains as an empty dictionary

    def initialize_domains(self, puzzle):
        # Initialize domains based on the initial puzzle
        for row in range(9):
            for col in range(9):
                if puzzle[row][col] != 0:  # Pre-filled cell
                    self.domains[(row, col)] = {puzzle[row][col]}
                else:  # Empty cell
                    self.domains[(row, col)] = set(range(1, 10))

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
                    return False  # Inconsistent assignment
                arcs.extend([(var_k, var_i) for var_k in self.get_neighbors(var_i) if var_k != var_j])
        return True  # Arc consistency applied successfully

    def get_neighbors(self, var):
        row, col = var
        neighbors = set()
        for i in range(9):
            neighbors.add((row, i))  # Add all cells in the same row
            neighbors.add((i, col))  # Add all cells in the same column
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                neighbors.add((i, j))  # Add all cells in the same 3x3 subgrid
        neighbors.remove(var)  # Remove the variable itself
        return neighbors

# Example usage:
solver = SudokuSolver()
puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
solver.initialize_domains(puzzle)
solver.apply_arc_consistency()
print(solver.domains)

