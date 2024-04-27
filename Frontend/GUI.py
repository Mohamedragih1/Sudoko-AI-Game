import pygame
import sys
from itertools import product
import numpy as np
sys.path.append('Backend')

from Board import Board
import SudokuSolver 

class SudokuSolverGUI:
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Sudoku Solver")
        self.clock = pygame.time.Clock()
        self.step_count = 0
        self.count = 0
        # Set colors
        self.bg_color = (255, 255, 255)  # White background
        self.line_color = (0, 0, 0)  # Black lines
        self.font_color = (0, 0, 0)  # Black font
        self.green_cells = []
        self.red_cells = []
        self.cell_size = 60
        self.grid_offset_x = (self.screen_width - self.cell_size * 9) // 2
        self.grid_offset_y = (self.screen_height - self.cell_size * 9) // 2

        # self.generate_random_puzzle(3, 30)
        self.puzzle = np.array([
                [0,0,0,0,0,4,7,0,8],
                [0,0,0,0,0,8,0,0,3],
                [0,0,0,2,1,5,0,0,0],
                [0,0,7,0,0,0,0,9,6],
                [8,0,0,0,9,0,0,0,0],
                [0,0,4,1,0,0,0,0,0],
                [0,1,0,0,4,0,5,0,0],
                [0,0,0,0,0,0,2,0,0],
                [2,5,0,0,0,0,0,8,0]
            ])
        self.solution = None
        self.steps = None
        self.cell_values = [[str(self.puzzle[i][j]) if self.puzzle[i][j] != 0 else "" for j in range(9)] for i in range(9)]

        self.font = pygame.font.Font(None, 48)

    def draw_grid(self):
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 2
            pygame.draw.line(self.screen, self.line_color, (self.grid_offset_x, self.grid_offset_y + i * self.cell_size),
                             (self.grid_offset_x + 9 * self.cell_size, self.grid_offset_y + i * self.cell_size), line_width)
            pygame.draw.line(self.screen, self.line_color, (self.grid_offset_x + i * self.cell_size, self.grid_offset_y),
                             (self.grid_offset_x + i * self.cell_size, self.grid_offset_y + 9 * self.cell_size), line_width)
            
            for j,i in self.green_cells:
                    cell_rect = pygame.Rect(self.grid_offset_x + i * self.cell_size,
                                        self.grid_offset_y + j * self.cell_size,
                                        self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, (0, 255, 0), cell_rect)  # Red background
                    border_rect = cell_rect.inflate(-3, -3)  # Shrink the cell size for the border
                    pygame.draw.rect(self.screen, (0, 255, 0), border_rect, 3)  # Red border, thickness 3
            
            for j, i in self.red_cells:
                cell_rect = pygame.Rect(self.grid_offset_x + i * self.cell_size,
                                        self.grid_offset_y + j * self.cell_size,
                                        self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (255, 0, 0), cell_rect)  # Red background
                border_rect = cell_rect.inflate(-3, -3)  # Shrink the cell size for the border
                pygame.draw.rect(self.screen, (255, 0, 0), border_rect, 3)  # Red border, thickness 3

    def draw_numbers(self):
        for i, j in product(range(9), repeat=2):
            if self.cell_values[i][j]:
                text_surface = self.font.render(self.cell_values[i][j], True, self.font_color)
                text_rect = text_surface.get_rect(center=(self.grid_offset_x + j * self.cell_size + self.cell_size // 2,
                                                           self.grid_offset_y + i * self.cell_size + self.cell_size // 2))
                self.screen.blit(text_surface, text_rect)

    def solve_sudoku(self):
        
        if self.solution is None:
            board = Board(3, self.puzzle)
            self.solution, self.steps = SudokuSolver.get_solution(board)
        
        solved = self.solution
        
        for board, var, val, color in self.steps:
            self.cell_values[var[0]][var[1]] = str(val) 

            if color == 'a':
                self.green_cells = [var]
            if color == 'r':
                self.red_cells = [var]
                
            print("--------------------------")
            print(f"Domain {self.count}")
            print(board.domains)    
            self.screen.fill(self.bg_color)
            self.draw_grid()
            self.draw_numbers()
            pygame.display.flip()
            self.clock.tick(10)
            self.count+=1
        print()
        for i in range(9):
            for j in range(9):
                self.cell_values[i][j] = str(solved[i][j])
        

    def generate_random_puzzle(self, dim, visible):
        self.puzzle, self.solution, self.steps = SudokuSolver.generate_random_puzzle(dim,visible)
        self.cell_values = [[str(self.puzzle[i][j]) if self.puzzle[i][j] != 0 else "" for j in range(9)] for i in range(9)]


    def solve_step(self):
        if self.solution is None:
            board = Board(3, self.puzzle)
            self.solution, self.steps = SudokuSolver.get_solution(board)
        
        solved = self.solution
        if self.step_count < len(self.steps):
        
            board = self.steps[self.step_count][0]
            var = self.steps[self.step_count][1]
            val = self.steps[self.step_count][2]
            color = self.steps[self.step_count][3]

            if color == 'a':
                self.green_cells = [var]
            if color == 'r':
                self.red_cells = [var]
                
            self.cell_values[var[0]][var[1]] = str(val) 
            #self.puzzle[var[0]][var[1]] = val
            print("--------------------------")
            print(f"Domain {self.count}")
            print(board.domains)    
            self.screen.fill(self.bg_color)
            self.draw_grid()
            self.draw_numbers()
            pygame.display.flip()
            self.clock.tick(10)
            self.count+=1
            self.step_count+=1
        else:
            for i in range(9):
                for j in range(9):
                    self.cell_values[i][j] = str(solved[i][j])    
       

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.solve_sudoku()
                    elif event.key == pygame.K_r:
                        self.generate_random_puzzle(3, 30)
                    elif event.key == pygame.K_s:
                        self.solve_step()  

            self.screen.fill(self.bg_color)
            self.draw_grid()
            self.draw_numbers()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()