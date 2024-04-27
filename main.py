import pygame
import sys
sys.path.append('Frontend')

from GUI import SudokuSolverGUI
from GUI2 import SudokuSolverGUI2
from GUI3 import SudokuSolverGUI3

pygame.init()

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 550

WHITE = (200, 200, 200)
BLACK = (25, 25, 112)
violet = (143, 0, 255)


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku")
background_image = pygame.image.load("sudoku.jpeg").convert()
window.blit(background_image, (0, 0))


font = pygame.font.SysFont("Berlin Sans FB Demi", 33) 

# Define button properties
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 60
BUTTON_PADDING = 20
BUTTON_RADIUS = 30  


button_x = (WINDOW_WIDTH - BUTTON_WIDTH) // 2

# Define button positions
button1_pos = (button_x, 200)
button2_pos = (button_x, 300)
button3_pos = (button_x, 400)

def draw_rounded_rect(surface, color, rect, radius=0):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def main():
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_pos = pygame.mouse.get_pos()
                if button1_rect.collidepoint(mouse_pos):
                    gui = SudokuSolverGUI()
                    gui.run()
                elif button2_rect.collidepoint(mouse_pos):
                    gui = SudokuSolverGUI2()
                    gui.run()
                elif button3_rect.collidepoint(mouse_pos):
                    gui = SudokuSolverGUI3()
                    gui.run()

        # Draw buttons
        draw_rounded_rect(window, WHITE, (button1_pos[0], button1_pos[1], BUTTON_WIDTH, BUTTON_HEIGHT), BUTTON_RADIUS)
        draw_rounded_rect(window, WHITE, (button2_pos[0], button2_pos[1], BUTTON_WIDTH, BUTTON_HEIGHT), BUTTON_RADIUS)
        draw_rounded_rect(window, WHITE, (button3_pos[0], button3_pos[1], BUTTON_WIDTH, BUTTON_HEIGHT), BUTTON_RADIUS)

        # Draw text on buttons
        text_surface = font.render("Mode 1: AI Generation", True, BLACK)
        window.blit(text_surface, (button1_pos[0] + 45, button1_pos[1] + 15))
        text_surface = font.render("Mode 2: User Input", True, BLACK)
        window.blit(text_surface, (button2_pos[0] + 60, button2_pos[1] + 15))
        text_surface = font.render("Mode 3: Interactive Game", True, BLACK)
        window.blit(text_surface, (button3_pos[0] + 15, button3_pos[1] + 15))

        pygame.display.update()

if __name__ == "__main__":
    main()
