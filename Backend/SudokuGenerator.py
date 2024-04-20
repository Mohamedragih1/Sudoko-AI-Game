import random

class SudokuGenerator:
    def __init__(self, dim):
        self.dim = dim * 3
        
    def is_valid_solution(self, solution):
        for i in range(self.dim):
            for j in range(self.dim):
                if not self.is_valid_cell(solution, i, j):
                    return False
        return True

    def is_valid_cell(self, solution, row, col):
        num = solution[row][col]
        # Check row
        if any(solution[row][c] == num and c != col for c in range(self.dim)):
            return False
        
        # Check column
        if any(solution[r][col] == num and r != row for r in range(self.dim)):
            return False
        
        # Check subgrid
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        if any(solution[r][c] == num and (r, c) != (row, col) for r in range(start_row, start_row + self.dim//3) for c in range(start_col, start_col + self.dim//3)):
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