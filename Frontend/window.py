import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 400, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Input Window")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 32)

def draw_text(surface, text, color, x, y):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def input_window():
    input_text = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        screen.fill(WHITE)
        draw_text(screen, "Input: " + input_text, BLACK, 10, 10)
        pygame.display.flip()


