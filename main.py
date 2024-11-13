import pygame
import sys



#player's position
player_positions = [
    (2,1 ), (3,1 ), (3,2 ), (3,3 ),  #player 1
    (2,2 ), (2,3 ), (2,4 ), (3, 4)   #player 2
]

dot_positions = [(1, 1), (4, 4)]  # Initial positions for the dots
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
 