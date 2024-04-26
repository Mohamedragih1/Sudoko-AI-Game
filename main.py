import pygame
import sys
sys.path.append('Frontend')

from GUI import SudokuSolverGUI
from GUI2 import SudokuSolverGUI2
from GUI3 import SudokuSolverGUI3

pygame.init()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 350

WHITE = (255, 0, 255)
BLACK = (0, 0, 0)
violet = (143, 0, 255)


# Set up the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Button Clicker")

# Set up font
font = pygame.font.Font(None, 36)

# Define button properties
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_PADDING = 20

# Define button positions
button1_pos = (100, 50)
button2_pos = (100, 150)
button3_pos = (100, 250)

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

        
        window.fill(violet)

        button1_rect = pygame.draw.rect(window, WHITE, (button1_pos[0], button1_pos[1], BUTTON_WIDTH, BUTTON_HEIGHT))
        button2_rect = pygame.draw.rect(window, WHITE, (button2_pos[0], button2_pos[1], BUTTON_WIDTH, BUTTON_HEIGHT))
        button3_rect = pygame.draw.rect(window, WHITE, (button3_pos[0], button3_pos[1], BUTTON_WIDTH, BUTTON_HEIGHT))


        text_surface = font.render("Mode 1", True, BLACK)
        window.blit(text_surface, (button1_pos[0] + 55, button1_pos[1] + 15))
        text_surface = font.render("Mode 2", True, BLACK)
        window.blit(text_surface, (button2_pos[0] + 55, button2_pos[1] + 15))
        text_surface = font.render("Mode 3", True, BLACK)
        window.blit(text_surface, (button3_pos[0] + 55, button3_pos[1] + 15))

        pygame.display.update()

if __name__ == "__main__":
    main()        
