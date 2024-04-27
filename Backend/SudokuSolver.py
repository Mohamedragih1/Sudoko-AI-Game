import numpy as np
from itertools import product
import random
from Board import Board
from copy import deepcopy

def revise_domain(board:Board, var_i, var_j):
    revised = False
    for val_i in board.domains[var_i].copy():
        consistent = any(val_j for val_j in board.domains[var_j] if val_j != val_i)
        if not consistent:
            board.domains[var_i].remove(val_i)
            revised = True
    return revised

def apply_arc_consistency(board:Board):
    arcs = [(var_i, var_j) for var_i in board.domains for var_j in board.get_neighbors(var_i)]
    while arcs:
        var_i, var_j = arcs.pop(0)
        if revise_domain(board, var_i, var_j):
            if len(board.domains[var_i]) == 0:
                return False
            arcs.extend([(var_k, var_i) for var_k in board.get_neighbors(var_i) if var_k != var_j])
    return True

def is_valid(board: Board, var, value):
    for neighbor in board.get_neighbors(var):
        if value == board.board[neighbor]:
            return False  # Value conflicts with a neighbor's value
    return True  # Value is valid for the variable

def select_variable_mrv(board:Board):
    unassigned_vars = [var for var in board.domains if len(board.domains[var]) > 1]
    return min(unassigned_vars, key=lambda var: len(board.domains[var]))

def select_value_lcv(board:Board, var):
    values = sorted(board.domains[var], key=lambda val: count_constraints(board, var, val))
    return values  # Choose the value with the least constraints

def count_constraints(board:Board, var, value):
    count = 0
    for neighbor in board.get_neighbors(var):
        if value in board.domains[neighbor]:
            count += 1
    return count

def solve_with_backtracking(board: Board):
    if not apply_arc_consistency(board):
        return None  # No solution possible after arc consistency
    steps = []
    def backtrack(board: Board, steps):

        unassigned_vars = [var for var in board.domains if len(board.domains[var]) > 1]
        if not unassigned_vars:
            return True  # No unassigned variables left, solution found
        
        var = select_variable_mrv(board)  # Get next variable to assign using MRV
        for value in select_value_lcv(board, var):
        # for value in board.domains[var]:
            if is_valid(board, var, value):
                board_temp = deepcopy(board)
                board.domains[var] = {value}  # Assign the value
                board.board[var] = value
                steps.append((deepcopy(board), var, value, 'a'))
                
                if apply_arc_consistency(board):
                    if backtrack(board, steps):
                        return True  # If this assignment leads to a solution, return True
                    
                board = board_temp
                steps.append((deepcopy(board), var, value, 'r'))
                
        return False  # No valid value found for this variable
    
    if backtrack(board, steps):
        solution = np.zeros((board.dim, board.dim), dtype=np.uint8)
        
        for var in board.domains:
            if len(board.domains[var]) > 1 or len(board.domains[var]) < 1:
                board.domains[var] = 0
            row, col = var
            try:
                solution[row][col] = next(iter(board.domains[var]))
            except:
                pass
        return solution, steps
    else:
        return None, steps  # No solution found

def generate_random_puzzle(dim, visible_count):
    empty_board = np.zeros((dim*3, dim*3), dtype=int)
    initial_values = random.sample(range(1, 10), 1)[0]  
    random_row = random.sample(range(0, 9), 1)[0]
    random_col = random.sample(range(0, 9), 1)[0]
    empty_board[random_row][random_col] = initial_values
    
    board = Board(3, empty_board)
    
    empty_board, steps = get_solution(board)  # Fill in initial values using backtracking
    solution = empty_board.copy()
    
    # Randomly select cells to keep visible
    visible_cells = random.sample(list(product(range(dim*3), repeat=2)), dim*3 * dim*3 - visible_count)
    for cell in visible_cells:
        empty_board[cell] = 0

    return empty_board, solution, steps

def get_solution(board:Board):
    return solve_with_backtracking(board)