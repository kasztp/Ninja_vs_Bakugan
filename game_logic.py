"""
Game logic for the game.
"""
import os
import sys
import random
from datetime import datetime
import pygame
from views.game_ui import GameUI
from views.menu import menu_loop
from utils import (
    COLORS,
    CONFIG,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    load_sprite,
    load_backgrounds,
    detect_collision,
    screen_init,
)


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

    def update_keyboard(self, key_list: list, _dt: float):
        """
        Update the player based on keyboard input.

        Parameters
        ----------
        key_list : list
            The keys that are pressed.
        """
        if key_list[pygame.K_UP]:
            self.rect.y -= self.speed * _dt
            self.image = player_image
        if key_list[pygame.K_DOWN]:
            self.rect.y += self.speed * _dt
            self.image = player_image
        if key_list[pygame.K_LEFT]:
            self.rect.x -= self.speed * _dt
            self.image = player_side_image
        if key_list[pygame.K_RIGHT]:
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

    def draw(self, screen: pygame.SurfaceType):
        """
        Draw the player.

        Parameters
        ----------
        screen : pygame.SurfaceType
            The screen to draw on.
        """
        screen.blit(self.image, self.rect)


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

    def draw(self, screen: pygame.SurfaceType):
        """
        Draw the enemy.

        Parameters
        ----------
        screen : pygame.SurfaceType
            The screen to draw on.
        """
        screen.blit(self.image, self.rect)


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


def game_loop(
    difficulty: str,
    controls: str,
    player: Player,
    enemy: Enemy,
    score: int,
    level: int,
    background_image: pygame.SurfaceType,
    game_ui: GameUI,
) -> None:
    """
    The game loop.

    Parameters
    ----------
    difficulty : str
        The difficulty of the game.
    controls : str
        The controls of the game.
    player : Player
        The player.
    enemy : Enemy
        The enemy.
    score : int
        The score.
    level : int
        The level.
    background_image : pygame.SurfaceType
        The background image.
    game_ui : GameUI
        The game UI.

    Returns
    -------
    None
    """
    # Set the clock
    clock = pygame.time.Clock()
    dt = 1

    # Create the shuriken group
    shurikens = []

    while True:
        # Calculate the time since the last frame
        dt = clock.tick(CONFIG.fps) / 5

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Drop back to the pause menu
                pygame.mouse.set_visible(True)
                difficulty_marker, controls_marker = menu_loop(paused=True)
                difficulty = diff[difficulty_marker]
                print("Difficulty:", difficulty)
                controls = controller[controls_marker]
                print("Controls:", controls)
            # Take a screenshot
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                img_name = (
                    f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
                )
                pygame.image.save(
                    screen, os.path.join(CONFIG.paths.screenshots, img_name)
                )

        if controls == "keyboard":
            # Check if the player is moved with keyboard
            keys = pygame.key.get_pressed()
            if any(
                [
                    keys[pygame.K_UP],
                    keys[pygame.K_DOWN],
                    keys[pygame.K_LEFT],
                    keys[pygame.K_RIGHT],
                ]
            ):
                player.update_keyboard(keys, dt)
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
            enemy.rect.y = random.randint(50, WINDOW_HEIGHT - 96)
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
            screen.fill(COLORS.black)
            screen.blit(
                CONFIG.ui_font.render("Game Over", True, COLORS.red),
                (WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT / 2 - 50),
            )
            screen.blit(
                CONFIG.ui_font.render(f"Score: {old_score}", True, COLORS.green),
                (WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT / 2),
            )
            pygame.display.update()
            pygame.time.delay(3000)
            pygame.mouse.set_visible(True)
            return None

        # Check if player is shooting a shuriken.
        # Create a shuriken if there are less than 3 shurikens on screen
        if controls == "keyboard":
            if keys[pygame.K_SPACE]:
                if len(shurikens) < 3:
                    shuriken = Shuriken(
                        x=player.rect.x + 96,
                        y=player.rect.y + 48,
                        speed=SHURIKEN_SPEED,
                        image=shuriken_image,
                    )
                    shurikens.append(shuriken)
        if controls == "mouse":
            if pygame.mouse.get_pressed()[0]:
                if len(shurikens) < 3:
                    shuriken = Shuriken(
                        x=player.rect.x + 96,
                        y=player.rect.y + 48,
                        speed=SHURIKEN_SPEED,
                        image=shuriken_image,
                    )
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
        # Remove the shurikens that collided with the enemy
        if len(shurikens_to_remove) > 0:
            shurikens_to_remove.sort(reverse=True)
            for idx in shurikens_to_remove:
                del shurikens[idx]

        # Update UI elements
        game_ui.update_level(level)
        game_ui.update_score(score)

        # Draw the background
        screen.blit(background_image, (0, 0))

        # Redraw UI
        game_ui.draw(player.hp)

        # Draw the player
        screen.blit(player.image, (player.rect.x, player.rect.y))

        # Draw the enemy
        screen.blit(enemy.image, (enemy.rect.x, enemy.rect.y))

        # Draw the shurikens
        for shuriken in shurikens:
            screen.blit(shuriken.image, (shuriken.rect.x, shuriken.rect.y))

        # Check if max level is reached
        if level == CONFIG.max_level:
            screen.fill(COLORS.white)
            game_over_text = CONFIG.ui_font.render("You Win", True, COLORS.green)
            screen.blit(
                game_over_text, (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 - 50)
            )
            pygame.display.update()
            pygame.time.delay(3000)
            pygame.mouse.set_visible(True)
            return None

        # Update the screen
        pygame.display.update()


if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    screen = screen_init("Ninja vs. Bakugan", (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Load the images
    player_image = load_sprite("ninja.png", (96, 96))
    player_side_image = load_sprite("ninja_side.png", (72, 96))
    enemy_image = load_sprite("enemy.png", (96, 96))
    background_images = load_backgrounds(CONFIG.max_level)
    background_image = background_images[0]
    shuriken_image = load_sprite("shuriken.png", (32, 32))

    # Start main loop
    while True:
        # Start the menu loop, get the difficulty and controls
        diff = {0: "easy", 1: "medium", 2: "hard"}
        controller = {0: "mouse", 1: "keyboard"}
        difficulty_marker, controls_marker = menu_loop()
        difficulty = diff[difficulty_marker]
        controls = controller[controls_marker]
        print("Difficulty:", difficulty)
        print("Controls:", controls)

        # Create the player, enemy and shuriken speed based on the difficulty
        match difficulty:
            case "easy":
                SHURIKEN_SPEED = 2.5
                BASE_ENEMY_SPEED = 0.8
                BASE_ENEMY_HP = 0.8
                BASE_PLAYER_SPEED = 1.2
                ENEMY_SPEED_INCREASE = 0.05
            case "medium":
                SHURIKEN_SPEED = 2
                BASE_ENEMY_SPEED = 1
                BASE_ENEMY_HP = 2
                BASE_PLAYER_SPEED = 1
                ENEMY_SPEED_INCREASE = 0.1
            case "hard":
                SHURIKEN_SPEED = 2
                BASE_ENEMY_SPEED = 1.2
                BASE_ENEMY_HP = 3
                BASE_PLAYER_SPEED = 1
                ENEMY_SPEED_INCREASE = 0.15
        player = Player(
            x=100,
            y=WINDOW_HEIGHT / 2,
            speed=BASE_PLAYER_SPEED,
            hp=5,
            image=player_image,
        )
        enemy = Enemy(
            x=WINDOW_WIDTH,
            y=random.randint(0, WINDOW_HEIGHT - 96),
            speed=BASE_ENEMY_SPEED,
            hp=BASE_ENEMY_HP,
            image=enemy_image,
        )

        if controls == "mouse":
            # Set the mouse position to the player position
            pygame.mouse.set_pos(player.rect.x, player.rect.y)
            pygame.mouse.set_visible(False)

        # Set the score and level
        score = 0
        level = 1

        # Create the game UI
        game_ui = GameUI(screen, CONFIG.ui_font)
        game_ui.draw(player.hp)

        # The game loop
        game_loop(
            difficulty, controls, player, enemy, score, level, background_image, game_ui
        )
