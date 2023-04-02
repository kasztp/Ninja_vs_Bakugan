"""
Game logic for the game.
"""
import os
import sys
import random
import yaml
import pygame
from utils import GameUI, load_sprite, load_backgrounds, detect_collision, screen_init

# Load config.yaml
with open(os.path.join("config.yaml"), encoding="utf8") as config_file:
    CONFIG = yaml.load(config_file, Loader=yaml.SafeLoader)

# Define some constants
try:
    WINDOW_WIDTH = CONFIG["resolution"]["horizontal"]
    WINDOW_HEIGHT = CONFIG["resolution"]["vertical"]
    TITLE = CONFIG["window_title"]
    FPS = CONFIG["fps"]
    MAX_LEVEL = CONFIG["max_level"]
except KeyError as error:
    print("Error: Missing key in config.yaml:", error)
    raise SystemExit from error

# Initialize Pygame
pygame.init()

# Create the window
screen = screen_init(TITLE, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Define some colors for later use
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the font
font = pygame.font.Font(None, 36)

# Create the game UI
game_ui = GameUI(screen, font)

# Load the images
player_image = load_sprite("ninja.png", (96, 96))
player_side_image = load_sprite("ninja_side.png", (96, 96))
enemy_image = load_sprite("enemy.png", (96, 96))
background_images = load_backgrounds(MAX_LEVEL)
background_image = background_images[0]
shuriken_image = load_sprite("shuriken.png", (32, 32))


class Player(pygame.sprite.Sprite):
    """
    The player class.
    """
    def __init__(self, x: int, y: int, speed: int, hp:int, image: pygame.SurfaceType):
        """
        Initialize the player.

        Parameters
        ----------
        x : int
            The x position of the player.
        y : int
            The y position of the player.
        speed : int
            The speed of the player.
        hp : int
            The health of the player.
        image : pygame.SurfaceType
            The image of the player.
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.hp = hp

    def update_keyboard(self, keys: list, _dt: float):
        """
        Update the player based on keyboard input.

        Parameters
        ----------
        keys : list
            The keys that are pressed.
        """
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed * _dt
            self.image = player_image
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed * _dt
            self.image = player_image
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * _dt
            self.image = player_side_image
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * _dt
            self.image = pygame.transform.flip(player_side_image, True, False)
    
    def update_mouse(self, mouse_location: tuple[int, int], _df: float):
        """
        Update the player based on mouse input.
        
        Parameters
        ----------
        mouse_location : tuple[int, int]
            The location of the mouse.
        """
        if mouse_location[0] < self.rect.x:
            self.image = player_side_image
        elif mouse_location[0] > self.rect.x:
            self.image = pygame.transform.flip(player_side_image, True, False)
        else:
            self.image = player_image

        self.rect.x = mouse_location[0]
        self.rect.y = mouse_location[1]


class Enemy(pygame.sprite.Sprite):
    """
    The enemy class.
    """
    def __init__(self, x: int, y: int, speed: int, hp: int, image: pygame.SurfaceType):
        """
        Initialize the enemy.

        Parameters
        ----------
        x : int
            The x position of the enemy.
        y : int
            The y position of the enemy.
        speed : int
            The speed of the enemy.
        hp : int
            The health of the enemy.
        image : pygame.SurfaceType
            The image of the enemy.
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.hp = hp

    def update(self, _dt: float):
        """
        Update the enemy.
        """
        self.rect.x -= self.speed * _dt


class Shuriken(pygame.sprite.Sprite):
    """
    The shuriken class.
    """
    def __init__(self, x: int, y: int, speed: int, image: pygame.SurfaceType):
        """
        Initialize the shuriken.

        Parameters
        ----------
        x : int
            The x position of the shuriken.
        y : int
            The y position of the shuriken.
        speed : int
            The speed of the shuriken.
        image : pygame.SurfaceType
            The image of the shuriken.
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.shot_time = pygame.time.get_ticks()

    def update(self, _dt: float):
        """
        Update the shuriken.
        """
        self.rect.x += self.speed * _dt


# Create the player
player = Player(x=100, y=WINDOW_HEIGHT / 2, speed=1, hp=5, image=player_image)

# Set the mouse position to the player position
pygame.mouse.set_pos(player.rect.x, player.rect.y)
pygame.mouse.hiding = True

# Create the enemy
enemy = Enemy(x=WINDOW_WIDTH, y=random.randint(0, WINDOW_HEIGHT - 96),
              speed=1, hp=2, image=enemy_image)

# Set the shuriken speed
SHURIKEN_SPEED = 2

# Create the shuriken group
shurikens = []

# Set the score and level
score = 0
level = 1

# Set the clock
clock = pygame.time.Clock()
dt = 1

# The game loop
while True:
    # Calculate the time since the last frame
    dt = clock.tick(FPS) / 5

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Check if the player is moved with keyboard
    keys = pygame.key.get_pressed()
    player.update(keys, dt)

    # Check if the player is moved with mouse
    if pygame.mouse.get_focused():
        mouse_location = pygame.mouse.get_pos()
        player.update_mouse(mouse_location, dt)

    # Move the enemy
    enemy.update(dt)

    # Check if the enemy is off the screen
    if enemy.rect.x < -96:
        enemy.kill()
        enemy = Enemy(x=WINDOW_WIDTH, y=random.randint(0, WINDOW_HEIGHT - 96),
                      speed=enemy.speed + 0.1, hp=2, image=enemy_image)
        score += 1
        level = score // 10 + 1
        background_image = background_images[level - 1]

    # Check for collisions
    if detect_collision(player, enemy):
        score = 0
        level = 1
        player.hp -= 1
        enemy.speed = 1
        enemy.kill()
        enemy = Enemy(x=WINDOW_WIDTH, y=random.randint(0, WINDOW_HEIGHT - 96),
                      speed=enemy.speed, hp=2, image=enemy_image)

    # Check if the player is dead
    if player.hp <= 0:
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (WINDOW_WIDTH / 2 - 60, WINDOW_HEIGHT / 2 - 50))
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()
        sys.exit()

    # Check if player is shooting a shuriken.
    # Create a shuriken if there are less than 3 shurikens on the screen
    if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
        if len(shurikens) < 3:
            shuriken = Shuriken(x=player.rect.x + 96, y=player.rect.y + 48,
                                speed=SHURIKEN_SPEED, image=shuriken_image)
            shurikens.append(shuriken)

    # Move the shurikens
    shurikens_to_remove = []
    for idx, shuriken in enumerate(shurikens):
        shuriken.update(dt)
        if shuriken.rect.x > WINDOW_WIDTH:
            shuriken.kill()
            shurikens_to_remove.append(idx)
    if len(shurikens_to_remove) > 0:
        shurikens_to_remove.sort(reverse=True)
        for idx in shurikens_to_remove:
            del shurikens[idx]

    # Check for shuriken collisions
    shurikens_to_remove = []
    for idx, shuriken in enumerate(shurikens):
        if detect_collision(shuriken, enemy):
            enemy.hp -= 1
            shuriken.kill()
            shurikens_to_remove.append(idx)
            if enemy.hp <= 0:
                enemy.kill()
                enemy = Enemy(x=WINDOW_WIDTH, y=random.randint(0, WINDOW_HEIGHT - 96),
                              speed=enemy.speed + 0.1, hp=2, image=enemy_image)
                score += 2
                level = score // 10 + 1
                background_image = background_images[level - 1]
    if len(shurikens_to_remove) > 0:
        shurikens_to_remove.sort(reverse=True)
        for idx in shurikens_to_remove:
            del shurikens[idx]
    
    # Update the UI
    game_ui.update_level(level)
    game_ui.update_score(score)

    # Draw the background
    screen.blit(background_image, (0, 0))

    # Draw the UI
    game_ui.draw(player.hp)

    # Draw the player
    screen.blit(player.image, (player.rect.x, player.rect.y))

    # Draw the enemy
    screen.blit(enemy.image, (enemy.rect.x, enemy.rect.y))

    # Draw the shurikens
    for shuriken in shurikens:
        screen.blit(shuriken.image, (shuriken.rect.x, shuriken.rect.y))

    # Check if max level is reached
    if level == MAX_LEVEL:
        screen.fill(WHITE)
        game_over_text = font.render("You Win", True, GREEN)
        screen.blit(game_over_text, (WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2 - 50))
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()
        sys.exit()

    # Update the screen
    pygame.display.update()
