import pygame
import sys
from itertools import product
sys.path.append('Backend')

from test2 import SudokuSolver

class SudokuSolverGUI:
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Sudoku Solver")
        self.clock = pygame.time.Clock()

        # Set colors
        self.bg_color = (255, 255, 255)  # White background
        self.line_color = (0, 0, 0)  # Black lines
        self.font_color = (0, 0, 0)  # Black font

        self.cell_size = 60
        self.grid_offset_x = (self.screen_width - self.cell_size * 9) // 2
        self.grid_offset_y = (self.screen_height - self.cell_size * 9) // 2

        self.puzzle = [
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

        self.cell_values = [[str(self.puzzle[i][j]) if self.puzzle[i][j] != 0 else "" for j in range(9)] for i in range(9)]

        self.font = pygame.font.Font(None, 48)

    def draw_grid(self):
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 2
            pygame.draw.line(self.screen, self.line_color, (self.grid_offset_x, self.grid_offset_y + i * self.cell_size),
                             (self.grid_offset_x + 9 * self.cell_size, self.grid_offset_y + i * self.cell_size), line_width)
            pygame.draw.line(self.screen, self.line_color, (self.grid_offset_x + i * self.cell_size, self.grid_offset_y),
                             (self.grid_offset_x + i * self.cell_size, self.grid_offset_y + 9 * self.cell_size), line_width)

    def draw_numbers(self):
        for i, j in product(range(9), repeat=2):
            if self.cell_values[i][j]:
                text_surface = self.font.render(self.cell_values[i][j], True, self.font_color)
                text_rect = text_surface.get_rect(center=(self.grid_offset_x + j * self.cell_size + self.cell_size // 2,
                                                           self.grid_offset_y + i * self.cell_size + self.cell_size // 2))
                self.screen.blit(text_surface, text_rect)

    def solve_sudoku(self):
        solver = SudokuSolver()
        solver.initialize_domains(self.puzzle)
        solved = solver.apply_arc_consistency()

        if solved:
            solution = solver.get_solution()
            for i in range(9):
                for j in range(9):
                    self.cell_values[i][j] = str(solution[i][j])
        else:
            print("Failed to solve Sudoku puzzle.")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.solve_sudoku()

            self.screen.fill(self.bg_color)
            self.draw_grid()
            self.draw_numbers()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()