import pygame
import sys

# Initialize Pygame
pygame.init()

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
NUM_BLOCK_SIDE_LENGTH = 10
SQUARE_SIZE = int(WINDOW_WIDTH / NUM_BLOCK_SIDE_LENGTH)
def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    while True:
        drawGrid()
        draw_in_bombs(SCREEN, generate_starting_config())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def drawGrid():
    for x in range(0, WINDOW_WIDTH, SQUARE_SIZE):
        for y in range(0, WINDOW_HEIGHT, SQUARE_SIZE):
            rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


def generate_starting_config():
  """
  TODO: Generate the starting configuration of the game board.
  """
  return [([True for _ in range(3)] + [False for _ in range(7)]) for _ in range(10)]


def draw_in_bombs(SCREEN, bomb_locations):
  assert len(bomb_locations) == 10
  assert len(bomb_locations[0]) == 10
  image = pygame.image.load("bomb.png") 
  for row_index, row in enumerate(bomb_locations):
    for col_index, is_bomb in enumerate(row):
      if not is_bomb:
        continue
      else:
        image = pygame.image.load("bomb.png")
        image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE)) 
        SCREEN.blit(image, (col_index * SQUARE_SIZE, row_index * SQUARE_SIZE))


if __name__ == "__main__":
    main()