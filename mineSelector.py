
import pygame
import sys
'''
Initilizes mine selector page screen size and button/text positioning
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
SMALL_FONT = pygame.font.SysFont(None, 28)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper - Mine Selector")

# mine state
mine_count = 10  # default

# buttons
back_button = pygame.Rect(WIDTH//2 - 60, HEIGHT - 60, 120, 40)
start_button = pygame.Rect(WIDTH//2 - 60, HEIGHT - 110, 120, 40)
minus_button = pygame.Rect(WIDTH//2 - 70, HEIGHT//2 - 20, 40, 40)
plus_button = pygame.Rect(WIDTH//2 + 30, HEIGHT//2 - 20, 40, 40)

def draw_menu(mine_count):
    '''
    Draws how the mine selector looks ie. the increase/decrease buttons and tracking mine count
    '''
    screen.fill(WHITE)

    # title
    large_font = pygame.font.SysFont("Calibri", 64, True)
    title_text = large_font.render("Minesweeper", True, BLACK)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 30))

    # mine count label
    label_text = SMALL_FONT.render("Select Mine Count:", True, BLACK)
    screen.blit(label_text, (WIDTH//2 - label_text.get_width()//2, HEIGHT//2 - 50))

    # mine count display
    count_text = FONT.render(str(mine_count), True, BLUE)
    screen.blit(count_text, (WIDTH//2 - count_text.get_width()//2, HEIGHT//2 - 10))

    # minus button
    pygame.draw.rect(screen, GRAY, minus_button)
    minus_text = FONT.render("-", True, BLACK)
    screen.blit(minus_text, (minus_button.centerx - minus_text.get_width()//2, minus_button.centery - minus_text.get_height()//2))

    # plus button
    pygame.draw.rect(screen, GRAY, plus_button)
    plus_text = FONT.render("+", True, BLACK)
    screen.blit(plus_text, (plus_button.centerx - plus_text.get_width()//2, plus_button.centery - plus_text.get_height()//2))

    # start button
    pygame.draw.rect(screen, DARK_GRAY, start_button)
    start_text = SMALL_FONT.render("Start Game", True, WHITE)
    screen.blit(start_text, (start_button.centerx - start_text.get_width()//2, start_button.centery - start_text.get_height()//2))

    # return to menu button
    pygame.draw.rect(screen, DARK_GRAY, back_button)
    back_text = SMALL_FONT.render("Back", True, WHITE)
    screen.blit(back_text, (back_button.centerx - back_text.get_width()//2, back_button.centery - back_text.get_height()//2))

    pygame.display.flip()


def run(mine_count, state): 
    '''
    Executes drawing the menu and handles user input
    of increasing/decreasing mine count and
    starting game (achived by updating state w/ GameStaeManager)
    '''
    clock = pygame.time.Clock()
    while True:
        draw_menu(mine_count)
        for event in pygame.event.get():
            # when button is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if minus_button.collidepoint(event.pos):
                    if mine_count > 10:
                        mine_count -= 1
                elif plus_button.collidepoint(event.pos):
                    if mine_count < 20:
                        mine_count += 1
                elif start_button.collidepoint(event.pos):
                    state["GameState"] = "Play"
                    state["NumMines"] = mine_count
                    return state
                elif back_button.collidepoint(event.pos):
                    state["GameState"] = "Menu"
                    return state
                

        clock.tick(30)