import sys
import pygame
from game import place_mines, create_game, reveal, toggle_flag

# Config
GRID_SIZE = 10
NUM_MINES = 20
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

TUTORIAL_TEXT = [
    "MINESWEEPER",
    "",
    "Left Click: Reveal",
    "Right Click: Flag / Unflag",
    "R: Restart",
    "Esc: Quit",
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

def new_game(x=None, y=None):
    board = place_mines(NUM_MINES, GRID_SIZE, GRID_SIZE,x,y)
    return create_game(board)
def draw_menu(surface, state, flag_icon, bomb_icon):
    pygame.draw.rect(surface, GREY, (0, 0, WINDOW_WIDTH, MENU_HEIGHT))
    font = pygame.font.Font(None, 28)

    surface.blit(flag_icon, (10, 6))
    surface.blit(font.render(f"{state['flags_left']}", True, WHITE), (40, 8))

    status = ""
    color = WHITE
    if not state["playing"]:
        status = "You Won!" if state["won"] else "Game Over"
        color = GREEN if state["won"] else RED
    surface.blit(font.render(status, True, color), (150, 8))

def draw_grid(surface, grid_icon):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        for y in range(MENU_HEIGHT, WINDOW_HEIGHT, CELL_SIZE):
            surface.blit(grid_icon, (x + 3, y + 3))

def draw_cells(surface, state, flag_icon, bomb_icon, numbers, empty_icon):
    font = pygame.font.Font(None, 28)
    show_mines = not state["playing"] and not state["won"]
    
    for r in range(state["size"]):
        for c in range(state["size"]):
            cell = state["grid"][r][c]
            x, y = c * CELL_SIZE, r * CELL_SIZE + MENU_HEIGHT
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

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
                
def draw_tutorial(surface):
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()
    theme = "Themes/OG/"
    flag_icon = load_icon(theme+"flag.png", CELL_SIZE - 6)
    bomb_icon = load_icon(theme+"bomb.png", CELL_SIZE - 6)
    grid_icon = load_icon(theme+"grid.png", CELL_SIZE - 6)
    empty_icon = load_icon(theme+"empty.png", CELL_SIZE - 6)
    number_icons = []
    for i in range(1,9):
        number_icon = load_icon(theme+"gridnum"+str(i)+".png", CELL_SIZE - 6)
        number_icons.append(number_icon)

    state = new_game() # dummy state before the first square is clicked
    state["first_click"] = True
    show_tut = True

    running = True
    while running:
        screen.fill(BLACK)

        draw_menu(screen, state, flag_icon, bomb_icon)
        draw_grid(screen, grid_icon)
        draw_cells(screen, state, flag_icon, bomb_icon, number_icons, empty_icon)

        if show_tut:
            draw_tutorial(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                state = new_game()
                state["first_click"] = True
                show_tut = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_tut:
                    show_tut = False                    
                x, y = event.pos
                if y > MENU_HEIGHT:
                    row = (y - MENU_HEIGHT) // CELL_SIZE
                    col = x // CELL_SIZE
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                        if state["first_click"]:
                            state = new_game(x=row, y=col)
                            state["first_click"] = False
                        else:
                            if event.button == 1:
                                reveal(state, row, col)
                            elif event.button == 3:
                                toggle_flag(state, row, col)
        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()
