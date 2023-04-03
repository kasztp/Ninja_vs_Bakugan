"""
Game logic for the game.
"""
import os
import sys
import random
import yaml
import pygame
from utils import (
    GameUI,
    MenuScreen,
    load_sprite,
    load_backgrounds,
    detect_collision,
    screen_init
    )

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

# Define some colors for later use
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    """
    The player class.
    """
    def __init__(self, x: int, y: int, speed: int, hp: int, image: pygame.SurfaceType):
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


if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    screen = screen_init("Ninja vs. Bakugan", (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Set the font
    font = pygame.font.SysFont("Arial", 36)

    # Create the menu screen
    menu = MenuScreen(screen, font)

    # Start the menu loop
    diff = {0: "easy", 1: "medium", 2: "hard"}
    controller = {0: "mouse", 1: "keyboard"}
    difficulty_marker, controls_marker = menu.menu_loop()
    print("Difficulty marker:", difficulty_marker)
    difficulty = diff[difficulty_marker]
    print("Difficulty:", difficulty)
    controls = controller[controls_marker]
    print("Controls:", controls)

    # Load the images
    player_image = load_sprite("ninja.png", (96, 96))
    player_side_image = load_sprite("ninja_side.png", (72, 96))
    enemy_image = load_sprite("enemy.png", (96, 96))
    background_images = load_backgrounds(MAX_LEVEL)
    background_image = background_images[0]
    shuriken_image = load_sprite("shuriken.png", (32, 32))

    # Create the player, enemy and shuriken speed depending on the difficulty
    if difficulty == "easy":
        SHURIKEN_SPEED = 2.5
        BASE_ENEMY_SPEED = 0.8
        BASE_ENEMY_HP = 0.8
        BASE_PLAYER_SPEED = 1.2
        ENEMY_SPEED_INCREASE = 0.05
    elif difficulty == "medium":
        SHURIKEN_SPEED = 2
        BASE_ENEMY_SPEED = 1
        BASE_ENEMY_HP = 2
        BASE_PLAYER_SPEED = 1
        ENEMY_SPEED_INCREASE = 0.1
    elif difficulty == "hard":
        SHURIKEN_SPEED = 2
        BASE_ENEMY_SPEED = 1.2
        BASE_ENEMY_HP = 3
        BASE_PLAYER_SPEED = 1
        ENEMY_SPEED_INCREASE = 0.15
    player = Player(x=100, y=WINDOW_HEIGHT / 2,
                    speed=BASE_PLAYER_SPEED,
                    hp=5, image=player_image)
    enemy = Enemy(x=WINDOW_WIDTH, y=random.randint(0, WINDOW_HEIGHT - 96),
                  speed=BASE_ENEMY_SPEED, hp=BASE_ENEMY_HP, image=enemy_image)

    if controls == "mouse":
        # Set the mouse position to the player position
        pygame.mouse.set_pos(player.rect.x, player.rect.y)
        pygame.mouse.set_visible(False)

    # Create the shuriken group
    shurikens = []

    # Set the score and level
    score = 0
    level = 1

    # Set the clock
    clock = pygame.time.Clock()
    dt = 1

    # Create the game UI
    game_ui = GameUI(screen, font)
    game_ui.draw(player.hp)

    # The game loop
    while True:
        # Calculate the time since the last frame
        dt = clock.tick(FPS) / 5

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            # Take a screenshot
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.image.save(screen,
                                  os.path.join(os.getcwd(), "screenshots",
                                            f"screenshot_{pygame.time.get_ticks()}.png"))

        if controls == "keyboard":
            # Check if the player is moved with keyboard
            keys = pygame.key.get_pressed()
            if any(keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT]):
                player.update(keys, dt)
        if controls == "mouse":
            # Check if the player is moved with mouse
            if pygame.mouse.get_pos() != (player.rect.x, player.rect.y):
                mouse_position = pygame.mouse.get_pos()
                player.update_mouse(mouse_position, dt)

        # Move the enemy
        enemy.update(dt)

        # Check if the enemy is off the screen
        if enemy.rect.x < -96:
            enemy.speed += ENEMY_SPEED_INCREASE
            score += 1
            level = score // 10 + 1
            enemy.rect.x = WINDOW_WIDTH
            enemy.rect.y = random.randint(0, WINDOW_HEIGHT - (50 + 96))
            enemy.hp = BASE_ENEMY_HP
            background_image = background_images[level - 1]

        # Check for collisions
        if detect_collision(player, enemy):
            old_score = score
            score = 0
            level = 1
            player.hp -= 1
            enemy.speed = BASE_ENEMY_SPEED
            enemy.rect.x = WINDOW_WIDTH
            enemy.rect.y = random.randint(0, WINDOW_HEIGHT - (50 + 96))
            enemy.hp = BASE_ENEMY_HP

        # Check if the player is dead
        if player.hp <= 0:
            screen.fill(BLACK)
            screen.blit(font.render(
                "Game Over", True, RED),
                (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 - 50))
            screen.blit(font.render(
                f"Score: {old_score}", True, GREEN),
                (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2))
            pygame.display.update()
            pygame.time.delay(5000)
            pygame.quit()
            sys.exit()

        # Check if player is shooting a shuriken.
        # Create a shuriken if there are less than 3 shurikens on the screen
        if controls == "keyboard":
            if keys[pygame.K_SPACE]:
                if len(shurikens) < 3:
                    shuriken = Shuriken(x=player.rect.x + 96, y=player.rect.y + 48,
                                        speed=SHURIKEN_SPEED, image=shuriken_image)
                    shurikens.append(shuriken)
        if controls == "mouse":
            if pygame.mouse.get_pressed()[0]:
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
                    enemy.rect.x = WINDOW_WIDTH
                    enemy.rect.y = random.randint(0, WINDOW_HEIGHT - 96)
                    enemy.speed += ENEMY_SPEED_INCREASE
                    enemy.hp = BASE_ENEMY_HP
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
