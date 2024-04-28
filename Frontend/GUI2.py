import pygame
import sys
from itertools import product
import numpy as np
from window import input_window
import time
from copy import deepcopy

sys.path.append('Backend')

from Board import Board
import SudokuSolver 

class SudokuSolverGUI2:
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Sudoku Solver")
        self.clock = pygame.time.Clock()

        self.grid_x = 0
        self.grid_y = 0
        self.green_cells = []
        self.red_cells = []
        self.init_board = None

        # Set colors
        self.bg_color = (255, 255, 255)  # White background
        self.line_color = (0, 0, 0)  # Black lines
        self.font_color = (0, 0, 0)  # Black font
        self.step_count = 0
        self.count = 0
        self.cell_size = 60
        self.grid_offset_x = (self.screen_width - self.cell_size * 9) // 2
        self.grid_offset_y = (self.screen_height - self.cell_size * 9) // 2
        self.current_var = (-1,-1)

        # self.generate_random_puzzle(3, 30)
        # self.puzzle = np.array([
        #         [0,0,0,0,0,4,7,0,8],
        #         [0,0,0,0,0,8,0,0,3],
        #         [0,0,0,2,1,5,0,0,0],
        #         [0,0,7,0,0,0,0,9,6],
        #         [8,0,0,0,9,0,0,0,0],
        #         [0,0,4,1,0,0,0,0,0],
        #         [0,1,0,0,4,0,5,0,0],
        #         [0,0,0,0,0,0,2,0,0],
        #         [2,5,0,0,0,0,0,8,0]
        #         ])
        self.puzzle = np.zeros((9,9), dtype=np.uint8)
        self.solution = None
        self.steps = None
        self.prev_board = self.puzzle  
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
            
            if (self.grid_x != -1):
                border_rect = pygame.Rect(self.grid_offset_x + self.grid_x * self.cell_size,
                                                self.grid_offset_y + self.grid_y * self.cell_size,
                                                self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (0, 0, 255), border_rect, 3)  # Red border, thickness 3
            
            if (self.current_var[0] != -1):
                cell_rect = pygame.Rect(self.grid_offset_x + self.current_var[1] * self.cell_size,
                                        self.grid_offset_y + self.current_var[0] * self.cell_size,
                                        self.cell_size, self.cell_size)
                border_rect = cell_rect.inflate(-3, -3)  # Shrink the cell size for the border
                pygame.draw.rect(self.screen, (0, 0, 255), border_rect, 3)  # Red border, thickness 3
                
            for i in range(9):
                for j in range(9):
                    if (self.init_board is not None and self.init_board[i][j] != 0):
                        if (self.grid_x == j and self.grid_y == i):
                            self.grid_x = -1
                            self.grid_y = -1
                            
                        cell_rect = pygame.Rect(self.grid_offset_x + j * self.cell_size,
                                        self.grid_offset_y + i * self.cell_size,
                                        self.cell_size, self.cell_size)
                        # pygame.draw.rect(self.screen, (255, 255, 0), cell_rect)  # Red background
                        border_rect = cell_rect.inflate(-3, -3)  # Shrink the cell size for the border
                        pygame.draw.rect(self.screen, (255, 255, 0), border_rect, 3)  # Red border, thickness 3 
            
    def draw_numbers(self):
        for i, j in product(range(9), repeat=2):
            if self.cell_values[i][j]:
                text_surface = self.font.render(self.cell_values[i][j], True, self.font_color)
                text_rect = text_surface.get_rect(center=(self.grid_offset_x + j * self.cell_size + self.cell_size // 2,
                                                           self.grid_offset_y + i * self.cell_size + self.cell_size // 2))
                self.screen.blit(text_surface, text_rect)

    def solve_sudoku(self):
        self.init_board = deepcopy(self.puzzle)
        self.grid_x = -1
        board = Board(3, self.puzzle)
        self.solution, self.steps = SudokuSolver.get_solution(board)
        solved = self.solution
        if solved is None:
            print("Can't be solved!")
            return
        
        for board, var, val, color in self.steps:
            self.cell_values[var[0]][var[1]] = str(val) 
            self.current_var = var
                    
            self.green_cells = []
            self.red_cells = []

            arcs, domains = SudokuSolver.apply_arc_consistency_one_var(board)
            for var_i, var_j, removed in arcs:
                print(var_i," -> ",var_j, ": ", removed)
                
            for i in range(9):
                for j in range(9):
                    if (self.prev_board[i][j] != board.board[i][j]): 
                        if color == 'a' and board.board[i][j] != 0:
                            self.green_cells.append((i, j))
                            board.board[(i, j)] = board.board[i][j]   
                        if color == 'r' and board.board[i][j] == 0:
                            self.red_cells.append((i, j))
                            board.board[(i, j)] = self.prev_board[i][j]    


            self.cell_values = [[str(board.board[i][j]) if board.board[i][j] != 0 else "" for j in range(9)] for i in range(9)]
            self.prev_board = deepcopy(board.board)        
            print("--------------------------")
            print(f"Domain {self.count}")
            print(domains)    
            print("--------------------------")  
            self.screen.fill(self.bg_color)
            self.draw_grid()
            if color == 'r':
                self.clock.tick(10)
            self.draw_numbers()
            pygame.display.flip()
            self.clock.tick(10)
            self.count+=1
        print()
        for i in range(9):
            for j in range(9):
                self.cell_values[i][j] = str(solved[i][j])


    def solve_step(self):
        self.grid_x = -1
        if (self.init_board == None):
            self.init_board = deepcopy(self.puzzle)
            
        if (self.steps == None):
            board = Board(3, self.puzzle)
            self.solution, self.steps = SudokuSolver.get_solution(board)

        solved = self.solution
        if solved is None:
            print("Can't be solved!")
            return
        
        if self.step_count < len(self.steps):
        
            board = self.steps[self.step_count][0]
            var = self.steps[self.step_count][1]
            val = self.steps[self.step_count][2]
            color = self.steps[self.step_count][3]
            self.green_cells = []
            self.red_cells = []
            self.current_var = var
            
            arcs, domains = SudokuSolver.apply_arc_consistency(board)
            for var_i, var_j, removed in arcs:
                print(var_i," -> ",var_j, ": ", removed)
                
            for i in range(9):
                for j in range(9):
                    if (self.prev_board[i][j] != board.board[i][j]): 
                        if color == 'a' and board.board[i][j] != 0:
                            self.green_cells.append((i, j))
                            board.board[(i, j)] = board.board[i][j]   
                        if color == 'r' and board.board[i][j] == 0:
                            self.red_cells.append((i, j))
                            board.board[(i, j)] = self.prev_board[i][j]   


            self.cell_values = [[str(board.board[i][j]) if board.board[i][j] != 0 else "" for j in range(9)] for i in range(9)]
            self.prev_board = deepcopy(board.board)        
            print("--------------------------")
            print(f"Domain {self.count}")
            print(domains)    
            print("--------------------------")  
            self.screen.fill(self.bg_color)
            self.draw_grid()
            if color == 'r':
                self.clock.tick(10)
            self.draw_numbers()
            pygame.display.flip()
            self.clock.tick(10)
            self.count+=1
            self.step_count+=1
            print()
        else:
            for i in range(9):
                for j in range(9):
                    self.cell_values[i][j] = str(solved[i][j])

    def generate_random_puzzle(self, dim, visible):
        self.puzzle, self.solution, self.steps = SudokuSolver.generate_random_puzzle(dim,visible)
        self.cell_values = [[str(self.puzzle[i][j]) if self.puzzle[i][j] != 0 else "" for j in range(9)] for i in range(9)]

    def move_by_one(self):
        self.grid_x += 1
        
        if self.grid_x == 9:
            self.grid_x = 0
            self.grid_y += 1

        if self.grid_y == 9:
            self.grid_y = 0
            
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start_time = time.time()
                        self.solve_sudoku()
                        end_time = time.time()
                        print("time = ",(end_time-start_time))
                    elif event.key == pygame.K_c:
                        self.init_board = None
                        self.grid_x = -1
                        self.current_var = (-1,-1)   
                        self.green_cells = []
                        self.red_cells = []                     
                        self.puzzle = np.zeros((9,9), dtype=np.uint8)
                        self.prev_board = self.puzzle
                        self.cell_values = [[str(self.puzzle[i][j]) if self.puzzle[i][j] != 0 else "" for j in range(9)] for i in range(9)]
                    elif event.key == pygame.K_s:
                        self.solve_step()     
                    elif event.key == pygame.K_TAB:
                        self.move_by_one()
                    elif event.key == pygame.K_r:
                        self.green_cells = []
                        self.red_cells = []
                        self.step_count = 0
                        self.current_var = (-1,-1)
                        self.generate_random_puzzle(3, 30)
                        self.init_board = deepcopy(self.puzzle)
                        self.prev_board = self.puzzle  
                        self.steps = None    
                    elif event.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
                            self.cell_values[self.grid_y][self.grid_x] = ""
                            self.puzzle[self.grid_y][self.grid_x] = 0
                    
                    
                    elif event.key in [pygame.K_0, pygame.K_KP0, pygame.K_1, pygame.K_KP1, pygame.K_2, pygame.K_KP2,
                                            pygame.K_3, pygame.K_KP3, pygame.K_4, pygame.K_KP4, pygame.K_5, pygame.K_KP5,
                                            pygame.K_6, pygame.K_KP6, pygame.K_7, pygame.K_KP7, pygame.K_8, pygame.K_KP8,
                                            pygame.K_9, pygame.K_KP9]:
                            if self.grid_y != -1:
                                if event.key in [pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4,
                                                pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9]:
                                    digit = int(pygame.key.name(event.key)[1])  # Extract digits after 'KP'
                                else:
                                    digit = int(pygame.key.name(event.key))     
                                      
                                # Set the clicked cell value
                                self.cell_values[self.grid_y][self.grid_x] = str(digit)
                                self.puzzle[self.grid_y][self.grid_x] = digit
                                self.move_by_one()
                            
                            
                            
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        # Calculate grid position based on mouse click
                        x, y = event.pos
                        self.grid_x = (x - self.grid_offset_x) // self.cell_size
                        self.grid_y = (y - self.grid_offset_y) // self.cell_size
                        # Ensure the click is within the grid boundaries
                        if not (0 <= self.grid_x < 9 and 0 <= self.grid_y < 9):
                            self.grid_x = 0
                            self.grid_y = 0

            self.screen.fill(self.bg_color)
            self.draw_grid()
            self.draw_numbers()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()