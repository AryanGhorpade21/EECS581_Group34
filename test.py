import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Pygame")

# Set up clock (controls frame rate)
clock = pygame.time.Clock()

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # window close button
            pygame.quit()
            sys.exit()

    # Update game state (nothing yet)

    # Draw background
    screen.fill((30, 30, 30))  # dark gray

    # Draw a red rectangle (example)
    pygame.draw.rect(screen, (255, 0, 0), (100, 100, 50, 50))

    # Flip display
    pygame.display.flip()

    # Limit to 60 FPS
    clock.tick(60)
