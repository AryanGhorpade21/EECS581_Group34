
import pygame
import sys
'''
Initilizes theme selector screen size and button/text positioning
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
pygame.display.set_caption("Minesweeper - Theme Selector")

# buttons
light_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 - 60, 120, 40)
dark_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 - 10, 120, 40)
og_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 40 , 120, 40)
drawn_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 90 , 120, 40)
back_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 140 , 120, 40)

def draw_menu(state):
    '''
    Draws how the theme selector look ie. dark, og, light, drawn
    '''
    screen.fill(WHITE)

    # title
    large_font = pygame.font.SysFont("Calibri", 64, True)
    title_text = large_font.render("Minesweeper", True, BLACK)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 30))

    # theme-button mapping
    button_data = [
        (light_button, "Light", "Themes/Light/"),
        (dark_button, "Dark", "Themes/Dark/"),
        (og_button, "OG", "Themes/OG/"),
        (drawn_button, "Drawn", "Themes/Drawn/"),
        (back_button, "Back", None),
    ]

    for rect, label, theme_path in button_data:
        is_selected = state.get("theme") == theme_path

        # invert colors if selected
        bg_color = GRAY if is_selected else DARK_GRAY
        text_color = BLACK if is_selected else WHITE
        
        # draw button
        pygame.draw.rect(screen, bg_color, rect)
        text_surf = FONT.render(label, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    pygame.display.flip()


def run(state): 
    '''
    Executes drawing handles user input
    of selecting light dark og drawn themes
    '''
    clock = pygame.time.Clock()
    while True:
        draw_menu(state)
        for event in pygame.event.get():
            # when button is clicked
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if light_button.collidepoint(event.pos):
                    state["theme"] = "Themes/Light/"
                elif dark_button.collidepoint(event.pos):
                    state["theme"] = "Themes/Dark/"
                elif og_button.collidepoint(event.pos):
                    state["theme"] = "Themes/OG/"
                elif drawn_button.collidepoint(event.pos):
                    state["theme"] = "Themes/Drawn/"
                elif drawn_button.collidepoint(event.pos):
                    state["theme"] = "Themes/Drawn/"
                elif back_button.collidepoint(event.pos):
                    state["GameState"] = "Menu"
                return state
                

        clock.tick(30)