import sys
import pygame
from game import place_mines, create_game, reveal, toggle_flag, ai_make_move
import mineSelector
import mainMenu
import themeSelector
import aiSelector

# Config
GRID_SIZE = 10
NUM_MINES = 10
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 440
MENU_HEIGHT = 40
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREY = (50, 50, 50)
DARKGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 160, 0)
BLUE = (0, 0, 255)

#Sound mixer file initialization
lose_sound = pygame.mixer.Sound("sound_assets/lose.mp3")
win_sound = pygame.mixer.Sound("sound_assets/win.mp3")
tile_clicked = pygame.mixer.Sound("sound_assets/tile_click.mp3")
flag_placed = pygame.mixer.Sound("sound_assets/flag_placed.mp3")

sound_effects = [lose_sound, win_sound, tile_clicked, flag_placed]

# Function to set volume for all sound effects at once
def set_sfx_volume(volume):
    for sfx in sound_effects:
        sfx.set_volume(volume)

set_sfx_volume(1) #set to 100%

TUTORIAL_TEXT = [
    "MINESWEEPER",
    "",
    "Left Click: Reveal",
    "Right Click: Flag / Unflag",
    "R: Restart",
    "Esc: To Return to Main Menu",
    "",
    "Click or press any key to start"
]

def load_icon(path, size):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, (size, size))
    except Exception as e:
        print(f"Warning: cannot load {path}: {e}")
        surf = pygame.Surface((size, size))
        surf.fill((255, 0, 0))
        return surf

def new_game(x=None, y=None, num_mines=10):
    board = place_mines(num_mines, GRID_SIZE, GRID_SIZE,x,y)
    return create_game(board)

def draw_menu(surface, state, flag_icon, ai_turn_timer=0, ai_turn_delay=2000):
    pygame.draw.rect(surface, GREY, (0, 0, WINDOW_WIDTH, MENU_HEIGHT))
    font = pygame.font.Font(None, 28)
    font_timer = pygame.font.Font(None, 42)
    font_flag = pygame.font.Font(None, 35)
    surface.blit(flag_icon, (10, 6))
    if not state["first_click"]:
        surface.blit(font_flag.render(f"{state['flags_left']}", True, WHITE), (50, 10))
    
    #UI for Game state
    status = ""
    color = WHITE
    if not state["playing"]:
        if state["won"] or state["ai_hit_bomb"]:
            pygame.mixer.music.stop()
            status = "You Won!"
            color = GREEN
            if not state.get("win_played", False): #prevents looping of mp3
                win_sound.play()
                state["win_played"] = True
        else:
            pygame.mixer.music.stop()
            status = "Game Over"
            color = RED
            if not state.get("lose_played", False): #prevents looping of mp3
                lose_sound.play()
                state["lose_played"] = True

    else:
        # Check if AI is enabled
        ai_enabled = state.get("ai_enabled", True)
        
        if not ai_enabled:
            # Solo play mode
            status = "Playing Solo"
            color = WHITE
        else:
            # AI vs Human mode
            if state['current_turn'] == 'ai' and ai_turn_timer > 0:
                remaining = max(0, ai_turn_delay - (pygame.time.get_ticks() - ai_turn_timer))
                countdown = remaining // 1000 + 1
                status = f"AI thinking... {countdown}"
                color = BLUE
            else:
                if state['current_turn'] == 'human':
                    status = "Your Turn"
                    color = WHITE
                else:
                    status = f"{state['current_turn'].title()}'s Turn"
                    color = BLUE
    
    surface.blit(font.render(status, True, color), (260, 8))


    # UI for Timer
    if not state["ai_difficulty"] == "solver":
        timer_text = font_timer.render(f"{state.get('timer_elapsed', '00:00:00')}", True, WHITE)
        timer_rect = timer_text.get_rect(left=100, centery=22)
        surface.blit(timer_text, timer_rect)

def draw_grid(surface, grid_icon):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        for y in range(MENU_HEIGHT, WINDOW_HEIGHT, CELL_SIZE):
            surface.blit(grid_icon, (x + 3, y + 3))

def draw_cells(surface, state, flag_icon, bomb_icon, numbers, empty_icon):
    show_mines = not state["playing"] and not state["won"]
    
    for r in range(state["size"]):
        for c in range(state["size"]):
            cell = state["grid"][r][c]
            x, y = c * CELL_SIZE, r * CELL_SIZE + MENU_HEIGHT

            if cell["revealed"]:
                surface.blit(empty_icon, (x + 3, y + 3))
                if cell["mine"]:
                    surface.blit(bomb_icon, (x + 3, y + 3))
                elif cell["srr"] > 0:
                    number = int(cell["srr"])
                    surface.blit(numbers[number-1], (x + 3, y + 3))
            else:
                
                if cell["flagged"]:
                    surface.blit(flag_icon, (x + 3, y + 3))
                elif show_mines and cell["mine"]:
                    surface.blit(bomb_icon, (x + 3, y + 3))

def load_bkgd_music(state):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(state["bkgd_music"])
    pygame.mixer.music.set_volume(0.1)

def pause_music(state):
    if state.get("music_muted", False):
        pygame.mixer.music.play()
        pygame.mixer.music.unpause()
        state["music_muted"] = False
    else:
        pygame.mixer.music.pause()
        state["music_muted"] = True

    print("m pressed", state["music_muted"])

    return state

def draw_tutorial(surface, state):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill(GREY + (200,))
    surface.blit(overlay, (0, 0))
    font_title = pygame.font.Font(None, 48)
    font_body = pygame.font.Font(None, 28)
    y = MENU_HEIGHT + 30
    for i, line in enumerate(TUTORIAL_TEXT):
        if i == 0:
            txt = font_title.render(line, True, WHITE)
        else:
            txt = font_body.render(line, True, WHITE)
        rect = txt.get_rect(center=(WINDOW_WIDTH // 2, y))
        surface.blit(txt, rect)
        y += 40
    load_bkgd_music(state)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()

    state = new_game() # dummy state before the first square is clicked
    state["first_click"] = True
    show_tut = True

    state["timer_elapsed"] = "00:00:00"
    
    # AI turn timing
    ai_turn_timer = 0
    ai_turn_delay = 2000  # 2 seconds delay before AI moves

    if not "bkgd_music" in state or "theme" in state:
        state["theme"] = "Themes/OG/"
        state["bkgd_music"] = "Themes/OG/OG.mp3"

    running = True
    while running:
        screen.fill(BLACK)
        flag_icon = load_icon(state["theme"]+"flag.png", CELL_SIZE - 6)
        bomb_icon = load_icon(state["theme"]+"bomb.png", CELL_SIZE - 6)
        grid_icon = load_icon(state["theme"]+"grid.png", CELL_SIZE - 6)
        empty_icon = load_icon(state["theme"]+"empty.png", CELL_SIZE - 6)
        number_icons = []

        for i in range(1,9):
            number_icon = load_icon(state["theme"]+"gridnum"+str(i)+".png", CELL_SIZE - 6)
            number_icons.append(number_icon)

        if state["GameState"] == "Play":
            if state.get("timer_start") is not None and state["playing"]:
                now = pygame.time.get_ticks()
                elapsed = (now - state["timer_start"]) // 1000  # total seconds
                hours, remainder = divmod(elapsed, 3600)
                minutes, seconds = divmod(remainder, 60)
                state["timer_elapsed"] = f"{hours:02}:{minutes:02}:{seconds:02}"

            draw_menu(screen, state, flag_icon, ai_turn_timer, ai_turn_delay)
            draw_grid(screen, grid_icon)
            draw_cells(screen, state, flag_icon, bomb_icon, number_icons, empty_icon)

            # Handle AI turn with timer (only if AI is enabled)
            if state.get("ai_enabled", True) and state["current_turn"] == "ai" and state["playing"]:
                if ai_turn_timer == 0:
                    ai_turn_timer = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - ai_turn_timer >= ai_turn_delay:
                    ai_make_move(state)
                    if state["ai_difficulty"] == "solver":
                        tile_clicked.play()
                    ai_turn_timer = 0  # Reset timer

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    state = pause_music(state)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    prev_theme = state["theme"]
                    prev_bkgd_music = state["bkgd_music"]
                    prev_music_state = state["music_muted"]
                    prev_ai_difficulty = state.get("ai_difficulty", "none")
                    prev_ai_enabled = state.get("ai_enabled", False)
                    state = new_game(num_mines=NUM_MINES)
                    state["GameState"] = "Play"
                    state["theme"] = prev_theme
                    state["ai_difficulty"] = prev_ai_difficulty
                    state["ai_enabled"] = prev_ai_enabled
                    state["current_turn"] = "human"
                    state["bkgd_music"] = prev_bkgd_music
                    state["first_click"] = True
                    show_tut = True
                    ai_turn_timer = 0  # Reset AI timer
                    state["music_muted"] = prev_music_state
                    pygame.mixer.music.play(-1)
                    if state["music_muted"]:    
                        pygame.mixer.music.pause()
                        

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    prev_bkgd_music = state["bkgd_music"]
                    prev_theme = state["theme"]
                    state = new_game(num_mines=NUM_MINES)
                    state["GameState"] = "Menu"
                    state["theme"] = prev_theme
                    state["bkgd_music"] = prev_bkgd_music
                    state["first_click"] = True
                    show_tut = True
                    ai_turn_timer = 0  # Reset AI timer
                # #DEBUG FOR WIN CONDITION, PRESS W
                # elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                #     state["playing"] = False
                #     state["won"] = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if show_tut:
                        show_tut = False
                        pygame.mixer.music.play(-1)
                        if state["music_muted"]:
                            pygame.mixer.music.pause()
                        continue            
                    x, y = event.pos
                    if y > MENU_HEIGHT:
                        row = (y - MENU_HEIGHT) // CELL_SIZE
                        col = x // CELL_SIZE
                        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                            if state["first_click"]:
                                prev_GameState = state["GameState"]
                                prev_theme = state["theme"]
                                prev_bkgd_music = state["bkgd_music"]
                                prev_music_state = state["music_muted"]
                                prev_ai_enabled = state["ai_enabled"]
                                prev_ai_difficulty = state["ai_difficulty"]
                                state = new_game(x=row, y=col, num_mines=NUM_MINES)
                                state["GameState"] = prev_GameState
                                state["theme"] = prev_theme
                                state["bkgd_music"] = prev_bkgd_music
                                state["ai_enabled"] = prev_ai_enabled
                                state["ai_difficulty"] = prev_ai_difficulty
                                state["first_click"] = False
                                state["timer_start"] = pygame.time.get_ticks()
                                state["music_muted"] = prev_music_state
                                # Immediately reveal the first clicked cell
                                if state["playing"]:
                                    tile_clicked.play()
                                reveal(state, row, col)
                            else:
                                # Check if AI is enabled
                                ai_enabled = state.get("ai_enabled", True)
                                
                                if not ai_enabled:
                                    # Solo mode - allow all moves
                                    if event.button == 1:
                                        tile_clicked.play()
                                        reveal(state, row, col)
                                        
                                    elif event.button == 3:
                                        toggle_flag(state, row, col)
                                        flag_placed.play()
                                else:
                                    # AI mode - only allow human input on human turn
                                    if state["current_turn"] == "human":
                                        if event.button == 1:
                                            tile_clicked.play()
                                            reveal(state, row, col)
                                            
                                            ai_turn_timer = 0  # Reset timer when human makes a move
                                        elif event.button == 3:
                                            flag_placed.play()
                                            toggle_flag(state, row, col)
                                            

            if show_tut:
                draw_tutorial(screen,state)
        elif state["GameState"] == "AISelector":
            state = aiSelector.run(state)
        elif state["GameState"] == "MineSelector":
            state = mineSelector.run(state["NumMines"], state)
            NUM_MINES = state["NumMines"]
        elif state["GameState"] == "Menu":
            state = mainMenu.run(state)
        elif state["GameState"] == "ThemeSelector":
            state = themeSelector.run(state)

        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()
