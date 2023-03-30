import pygame
import random

# Initialize Pygame
pygame.init()

# Set the window dimensions
window_width = 1000
window_height = 533

# Create the window
screen = pygame.display.set_mode((window_width, window_height))

# Set the title of the window
pygame.display.set_caption("Ninjago vs. Bakugan")

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the font
font = pygame.font.Font(None, 36)

# Load the images
player_image = pygame.image.load("ninja.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (96, 96))
player_side_image = pygame.image.load("ninja_side.png").convert_alpha()
player_side_image = pygame.transform.scale(player_side_image, (96, 96))
background_image = pygame.image.load("background.png").convert()
enemy_image = pygame.image.load("enemy.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (96, 96))
player = player_image

# Set the player position
player_x = 100
player_y = window_height / 2

# Set the enemy position
enemy_x = window_width
enemy_y = random.randint(0, window_height - 96)

# Set the enemy speed
enemy_speed = 5

# Set the score
score = 0

# The game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= 5
        player = player_image
    if keys[pygame.K_DOWN]:
        player_y += 5
        player = player_image
    if keys[pygame.K_LEFT]:
        player_x -= 5
        player = player_side_image
    if keys[pygame.K_RIGHT]:
        player_x += 5
        player = pygame.transform.flip(player_side_image, True, False)
    # Move the enemy
    enemy_x -= enemy_speed

    # Check if the enemy is off the screen
    if enemy_x < -96:
        enemy_x = window_width
        enemy_y = random.randint(0, window_height - 96)
        score += 1

    # Check for collisions
    if all([(player_x + 96 > enemy_x),
            (player_x < enemy_x + 96),
            (player_y + 96 > enemy_y),
            (player_y < enemy_y + 96)]
        ):
        score = 0

    # Draw the background
    screen.blit(background_image, (0, 0))

    # Draw the player
    screen.blit(player, (player_x, player_y))

    # Draw the enemy
    screen.blit(enemy_image, (enemy_x, enemy_y))

    # Draw the score
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (window_width / 2 - 50, 10))

    # Update the screen
    pygame.display.update()
