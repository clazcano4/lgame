import pygame

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Set grid dimensions
grid_size = 4
cell_size = 100

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw grid
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size
            y = row * cell_size
            pygame.draw.rect(screen, white, (x, y, cell_size, cell_size), 2)

    # Update display
    pygame.display.flip()
pygame.quit()
 