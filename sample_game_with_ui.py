import pygame
import sys

# Initialize Pygame
pygame.init()

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREY = (50, 50, 50)
WINDOW_HEIGHT = 440
WINDOW_WIDTH = 400
NUM_BLOCK_SIDE_LENGTH = 10
MENU_HEIGHT = 40
SQUARE_SIZE = int(WINDOW_WIDTH / NUM_BLOCK_SIDE_LENGTH)
def main():
    global SCREEN, CLOCK
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Game with Menu Bar")
    CLOCK = pygame.time.Clock()

    while True:
        SCREEN.fill(BLACK)

        draw_menu_bar(SCREEN)

        drawGrid()
        draw_in_bombs(SCREEN, generate_starting_config())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        CLOCK.tick(30)


def draw_menu_bar(surface, num_bombs_left=10, time_left=60):
    pygame.draw.rect(surface, GREY, (0, 0, WINDOW_WIDTH, MENU_HEIGHT))

    # Load emoji images
    flag_img = pygame.image.load("flag.jpeg")
    clock_img = pygame.image.load("clock.png")

    # Scale them to fit menu bar
    flag_img = pygame.transform.scale(flag_img, (28, 28))
    clock_img = pygame.transform.scale(clock_img, (28, 28))

    # Draw emojis
    surface.blit(flag_img, (10, 6))
    surface.blit(clock_img, (100, 6))

    # Draw text next to emojis
    font = pygame.font.Font(None, 28)
    num_bombs_text = font.render(f"{num_bombs_left}", True, WHITE)
    time_text = font.render(f"{time_left}", True, WHITE)
    surface.blit(num_bombs_text, (40, 8))
    surface.blit(time_text, (140, 8))


def drawGrid():
    for x in range(0, WINDOW_WIDTH, SQUARE_SIZE):
        for y in range(MENU_HEIGHT, WINDOW_HEIGHT, SQUARE_SIZE):
            rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


def generate_starting_config():
    return [([True for _ in range(3)] + [False for _ in range(7)]) for _ in range(10)]


def draw_in_bombs(surface, bomb_locations):
    assert len(bomb_locations) == 10
    assert len(bomb_locations[0]) == 10
    image = pygame.image.load("bomb.png")
    image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

    for row_index, row in enumerate(bomb_locations):
        for col_index, is_bomb in enumerate(row):
            if not is_bomb:
                continue
            surface.blit(image, (col_index * SQUARE_SIZE, row_index * SQUARE_SIZE + MENU_HEIGHT))


if __name__ == "__main__":
    main()
