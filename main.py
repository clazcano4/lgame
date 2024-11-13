import pygame
import sys

# Player's position
player_positions = [
    (2, 1), (3, 1), (3, 2), (3, 3),  # player 1
    (2, 2), (2, 3), (2, 4), (3, 4)   # player 2
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
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)

class NeutralPieces:
    def neutralOne(self):
        pygame.draw.circle(screen, white, (50, 50), 40)
        pygame.display.update()

    def neutralTwo(self):
        pygame.draw.circle(screen, white, (350, 350), 40)
        pygame.display.update()

class PlayersOne:
    def oneX(self):
        pygame.draw.rect(screen, red, (100, 0, 200, 100))  # Adjust to the player 1's piece position
        pygame.display.update()

    def oneY(self):
        pygame.draw.rect(screen, red, (100, 100, 100, 200))  # Adjust to the player 1's piece position
        pygame.display.update()

class PlayersTwo:
    def twoX(self):
        pygame.draw.rect(screen, blue, (100, 300, 200, 100))  # Adjust to the player 2's piece position
        pygame.display.update()

    def twoY(self):
        pygame.draw.rect(screen, blue, (200, 100, 100, 200))  # Adjust to the player 2's piece position
        pygame.display.update()

# Create instances of the player classes
neutral = NeutralPieces()
playerOne = PlayersOne()
playerTwo = PlayersTwo()

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

    # display player and neutral pieces (based on their positions)
    neutral.neutralOne()  
    neutral.neutralTwo()
    playerOne.oneX()  
    playerOne.oneY()  
    playerTwo.twoX()  
    playerTwo.twoY()  

    # Update display
    pygame.display.flip()

pygame.quit()
