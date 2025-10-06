import pygame
import sys

'''
Module: aiSelector
Description: initializes AI selector page screen size and button/text positioning
Atharva Patil, 9/30/2025
'''

pygame.init()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 100, 200)
GREEN = (50, 150, 50)

# screen setup
WIDTH, HEIGHT = 400, 440

# fonts
FONT = pygame.font.SysFont(None, 36)
SMALL_FONT = pygame.font.SysFont(None, 28)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper - AI Selector")

# AI options
AI_OPTIONS = ["None", "Easy", "Medium", "Hard", "Solver"]

# buttons
back_button = pygame.Rect(WIDTH//2 - 60, HEIGHT - 60, 120, 40)
start_button = pygame.Rect(WIDTH//2 - 60, HEIGHT - 110, 120, 40)
left_button = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 - 20, 40, 40)
right_button = pygame.Rect(WIDTH//2 + 80, HEIGHT//2 - 20, 40, 40)

def draw_menu(ai_index):
    # draws how the AI selector looks with left/right buttons and tracking AI selection
    screen.fill(WHITE)

    # title
    large_font = pygame.font.SysFont("Calibri", 64, True)
    title_text = large_font.render("Minesweeper", True, BLACK)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 30))

    # AI selection label
    label_text = SMALL_FONT.render("Select AI Difficulty:", True, BLACK)
    screen.blit(label_text, (WIDTH//2 - label_text.get_width()//2, HEIGHT//2 - 70))

    # AI selection display
    ai_option = AI_OPTIONS[ai_index]
    color = GREEN if ai_option == "None" else BLUE
    option_text = FONT.render(ai_option, True, color)
    screen.blit(option_text, (WIDTH//2 - option_text.get_width()//2, HEIGHT//2 - 10))

    # description text
    descriptions = {
        "None": "Play solo without AI",
        "Easy": "AI makes random moves",
        "Medium": "AI uses basic strategy",
        "Hard": "AI knows safe moves",
        "Solver": "AI will solve the whole board"
    }
    desc_text = SMALL_FONT.render(descriptions[ai_option], True, BLACK)
    screen.blit(desc_text, (WIDTH//2 - desc_text.get_width()//2, HEIGHT//2 + 20))

    # left arrow button
    pygame.draw.rect(screen, GRAY, left_button)
    left_text = FONT.render("<", True, BLACK)
    screen.blit(left_text, (left_button.centerx - left_text.get_width()//2, left_button.centery - left_text.get_height()//2))

    # right arrow button
    pygame.draw.rect(screen, GRAY, right_button)
    right_text = FONT.render(">", True, BLACK)
    screen.blit(right_text, (right_button.centerx - right_text.get_width()//2, right_button.centery - right_text.get_height()//2))

    # start button
    pygame.draw.rect(screen, DARK_GRAY, start_button)
    start_text = SMALL_FONT.render("Continue", True, WHITE)
    screen.blit(start_text, (start_button.centerx - start_text.get_width()//2, start_button.centery - start_text.get_height()//2))

    # return to menu button
    pygame.draw.rect(screen, DARK_GRAY, back_button)
    back_text = SMALL_FONT.render("Back", True, WHITE)
    screen.blit(back_text, (back_button.centerx - back_text.get_width()//2, back_button.centery - back_text.get_height()//2))

    pygame.display.flip()


def run(state): 
    # executes drawing the menu and handles user input of selecting AI difficulty and continuing to mine selector
    
    # get current AI difficulty index from state
    current_ai = state.get("ai_difficulty", "none").lower()
    ai_index = 0  # default to "None"
    
    for i, option in enumerate(AI_OPTIONS):
        if option.lower() == current_ai:
            ai_index = i
            break
    
    clock = pygame.time.Clock()
    while True:
        draw_menu(ai_index)
        for event in pygame.event.get():
            # when button is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if left_button.collidepoint(event.pos):
                    ai_index = (ai_index - 1) % len(AI_OPTIONS)
                elif right_button.collidepoint(event.pos):
                    ai_index = (ai_index + 1) % len(AI_OPTIONS)
                elif start_button.collidepoint(event.pos):
                    # set AI difficulty in state
                    selected_ai = AI_OPTIONS[ai_index].lower()
                    state["ai_difficulty"] = selected_ai

                    # set game mode based on AI selection
                    if selected_ai == "none":
                        state["current_turn"] = "human"  # human only mode
                        state["ai_enabled"] = False
                    else:
                        state["current_turn"] = "human"  # human starts first
                        state["ai_enabled"] = True
                    
                    # continue to mine selector
                    state["GameState"] = "MineSelector"
                    return state
                elif back_button.collidepoint(event.pos):
                    state["GameState"] = "Menu"
                    return state

        clock.tick(30)