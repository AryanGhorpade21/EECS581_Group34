import pygame
import sys

'''
Initilizes main menu screen size and button/text positioning
'''
pygame.init()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 100, 200)

# screen setup
WIDTH, HEIGHT = 400, 440

# fonts
FONT = pygame.font.SysFont(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper - Main Menu")

# buttons
play_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 - 30, 120, 40)
themes_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 20, 120, 40)

def draw_menu():
    '''
    Draws how the main menu looks ie. the play and theme selector
    '''
    screen.fill(WHITE)

    # title
    large_font = pygame.font.SysFont("Calibri", 64, True)
    title_text = large_font.render("Minesweeper", True, BLACK)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 30))

    # play button
    pygame.draw.rect(screen, DARK_GRAY, play_button)
    play_text = FONT.render("Play", True, WHITE)
    screen.blit(play_text, (play_button.centerx - play_text.get_width()//2, play_button.centery - play_text.get_height()//2))

    # themes button
    pygame.draw.rect(screen, DARK_GRAY, themes_button)
    themes_text = FONT.render("Themes", True, WHITE)
    screen.blit(themes_text, (themes_button.centerx - themes_text.get_width()//2, themes_button.centery - themes_text.get_height()//2))

    pygame.display.flip()


def run(state): 
    '''
    Executes drawing the menu and handles user input
    of starting game, selecting ai mode, selecting theme
    '''
    clock = pygame.time.Clock()
    while True:
        draw_menu()
        for event in pygame.event.get():
            # when button is clicked
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint(event.pos):
                    state["GameState"] = "MineSelector"
                elif themes_button.collidepoint(event.pos):
                    state["GameState"] = "ThemeSelector"
                
                return state
                

        clock.tick(30)