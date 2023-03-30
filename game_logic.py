import random
import pygame

# Initialize Pygame
pygame.init()

# Set the window dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 533

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Ninjago vs. Bakugan")

# Define some colors for later use
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
player_y = WINDOW_HEIGHT / 2

# Set the enemy position
enemy_x = WINDOW_WIDTH
enemy_y = random.randint(0, WINDOW_HEIGHT - 96)

# Set the enemy speed
enemy_speed = 1

# Set the player speed
player_speed = 1

# Set the score and level
score = 0
level = 1

# Set the clock
clock = pygame.time.Clock()
FRAMERATE = 30
dt = 1

# The game loop
while True:
    # Calculate the time since the last frame
    dt = clock.tick(FRAMERATE) / 5

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= player_speed * dt
        player = player_image
    if keys[pygame.K_DOWN]:
        player_y += player_speed * dt
        player = player_image
    if keys[pygame.K_LEFT]:
        player_x -= player_speed * dt
        player = player_side_image
    if keys[pygame.K_RIGHT]:
        player_x += player_speed * dt
        player = pygame.transform.flip(player_side_image, True, False)
    # Move the enemy
    enemy_x -= enemy_speed * dt

    # Check if the enemy is off the screen
    if enemy_x < -96:
        enemy_x = WINDOW_WIDTH
        enemy_y = random.randint(0, WINDOW_HEIGHT - 96)
        score += 1
        level = score // 10 + 1
        enemy_speed += 0.1

    # Check for collisions
    if all([(player_x + 96 > enemy_x),
            (player_x < enemy_x + 96),
            (player_y + 96 > enemy_y),
            (player_y < enemy_y + 96)]
        ):
        score = 0
        level = 1
        enemy_speed = 1

    # Draw the background
    screen.blit(background_image, (0, 0))

    # Draw the player
    screen.blit(player, (player_x, player_y))

    # Draw the enemy
    screen.blit(enemy_image, (enemy_x, enemy_y))

    # Draw the score
    score_text = font.render(f"Score: {score} | Level: {level}", True, WHITE)
    screen.blit(score_text, (WINDOW_WIDTH / 2 - 100, 10))

    # Update the screen
    pygame.display.update()
