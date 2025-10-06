import pygame
import sys
from highscores import format_scores

'''
Module: mainMenu
Description: initializes main menu screen size and provides navigation to Play, AI Mode, Themes, and Scores
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
play_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 - 60, 120, 40)
ai_selector_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 - 10, 120, 40)
themes_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 40, 120, 40)
scores_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 90, 120, 40)

# function to render the top 5 highest scores list
def draw_highscores(screen, state=None):
    screen.fill(WHITE)
    title = FONT.render("Top 5 Times", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    scores = format_scores()
    print(scores)

    if not scores:
        # display message when there are no recorded scores
        no_scores_text = FONT.render("No scores recorded yet!", True, DARK_GRAY)
        no_scores_rect = no_scores_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(no_scores_text, no_scores_rect)
    else:
        # display formatted score list
        for i, line in enumerate(scores):
            txt = FONT.render(line, True, BLACK)
            txt_rect = txt.get_rect(centerx=WIDTH // 2, y=120 + i * 40)
            screen.blit(txt, txt_rect)

    back_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 70, 120, 40)
    pygame.draw.rect(screen, DARK_GRAY, back_button)
    back_text = FONT.render("Back", True, WHITE)
    back_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_rect)

    pygame.display.flip()

    # wait for user to exit using back button
    clock = pygame.time.Clock()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint(event.pos):
                    waiting = False  # exit the high scores screen and return to menu
                    if state is not None:
                        state["GameState"] = "Menu"
                        return state
                    else:
                        return

        clock.tick(30)

def draw_menu():
    # draws how the main menu looks ie. the play, AI mode, and theme selector
    screen.fill(WHITE)

    # title
    large_font = pygame.font.SysFont("Calibri", 64, True)
    title_text = large_font.render("Minesweeper", True, BLACK)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 30))

    # play button
    pygame.draw.rect(screen, DARK_GRAY, play_button)
    play_text = FONT.render("Play", True, WHITE)
    screen.blit(play_text, (play_button.centerx - play_text.get_width()//2, play_button.centery - play_text.get_height()//2))

    # ai selector button
    pygame.draw.rect(screen, DARK_GRAY, ai_selector_button)
    ai_selector_text = FONT.render("AI Mode", True, WHITE)
    screen.blit(ai_selector_text, (ai_selector_button.centerx - ai_selector_text.get_width()//2, ai_selector_button.centery - ai_selector_text.get_height()//2))

    # themes button
    pygame.draw.rect(screen, DARK_GRAY, themes_button)
    themes_text = FONT.render("Themes", True, WHITE)
    screen.blit(themes_text, (themes_button.centerx - themes_text.get_width()//2, themes_button.centery - themes_text.get_height()//2))

    # high scores button
    pygame.draw.rect(screen, DARK_GRAY, scores_button)
    scores_text = FONT.render("Scores", True, WHITE)
    screen.blit(scores_text, (scores_button.centerx - scores_text.get_width()//2,
                              scores_button.centery - scores_text.get_height()//2))


    pygame.display.flip()


def run(state): 
    # executes drawing the menu and handles user input of starting game, selecting ai mode, selecting theme
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
                    state["GameState"] = "AISelector"
                elif ai_selector_button.collidepoint(event.pos):
                    state["GameState"] = "AISelector"
                elif themes_button.collidepoint(event.pos):
                    state["GameState"] = "ThemeSelector"
                elif scores_button.collidepoint(event.pos):
                    draw_highscores(screen, state)

                
                return state
                

        clock.tick(30)