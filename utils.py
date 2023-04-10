"""
Utility functions for the game.
"""
import os
import sys
import pygame
import yaml

# Define some colors for later use
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load font
assets_path = os.path.join(os.getcwd(), "assets")
font_path = os.path.join(assets_path, "fonts", "C64_Pro_Mono-STYLE.ttf")
font_size = 32
ui_font = pygame.font.Font(font_path, font_size)

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


def load_sprite(name: str, scale: tuple = None) -> pygame.SurfaceType:
    """
    Load a sprite from the sprites folder.

    Parameters
    ----------
    name : str
        The name of the sprite to load.
    scale : tuple, optional
        The scale to apply to the sprite, by default None

    Returns
    -------
    pygame.SurfaceType
        The loaded sprite.
    """
    fullname = os.path.join(os.getcwd(), "assets", "sprites", name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print("Cannot load image:", fullname)
        raise SystemExit(message) from message
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image


def load_ui_item(name: str, scale: tuple = None) -> pygame.SurfaceType:
    """
    Load a UI item from the UI folder.

    Parameters
    ----------
    name : str
        The name of the UI item to load.
    scale : tuple, optional
        The scale to apply to the UI item, by default None

    Returns
    -------
    pygame.SurfaceType
        The loaded UI item.
    """
    fullname = os.path.join(os.getcwd(), "assets", "ui", name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print("Cannot load image:", fullname)
        raise SystemExit(message) from message
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image


def load_backgrounds(how_many_to_load: int, scale=(WINDOW_WIDTH, WINDOW_HEIGHT)) -> list[pygame.SurfaceType]:
    """
    Load a given nnumber of backgrounds from the backgrounds folder.

    Parameters
    ----------
    how_many_to_load : int
        The number of backgrounds to load.

    Returns
    -------
    list[pygame.SurfaceType]
        The loaded backgrounds.
    """
    backgrounds = []
    bg_path = os.path.join(os.getcwd(), "assets", "backgrounds")
    files = os.listdir(bg_path)
    for i in range(how_many_to_load):
        try:
            image = pygame.image.load(os.path.join(bg_path, files[i])).convert()
            backgrounds.append(pygame.transform.scale(image, scale))
        except pygame.error as message:
            print("Cannot load image:", files[i])
            raise SystemExit(message) from message
    return backgrounds


def detect_collision(sprite1: pygame.sprite.Sprite, sprite2: pygame.sprite.Sprite) -> bool:
    """
    Detect a collision between two sprites.

    Parameters
    ----------
    sprite1 : pygame.sprite.Sprite
        The first sprite.
    sprite2 : pygame.sprite.Sprite
        The second sprite.

    Returns
    -------
    bool
        Whether or not the sprites collided.
    """
    return sprite1.rect.colliderect(sprite2.rect)


def screen_init(title: str, size: tuple) -> pygame.SurfaceType:
    """
    Initialize the screen.

    Parameters
    ----------
    size : tuple
        The size of the screen.

    Returns
    -------
    pygame.SurfaceType
        The initialized screen.
    """
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(title)
    return screen


class GameUI():
    """
    The game UI class.
    """
    def __init__(self, screen: pygame.SurfaceType, font: pygame.font.FontType = ui_font):
        """
        Initialize the game UI.

        Parameters
        ----------
        screen : pygame.SurfaceType
            The screen to draw the UI on.
        font : pygame.font.FontType
            The font to use for the UI.
        """
        self.screen = screen
        self.font = font
        self.level = 1
        self.score = 0
        self.max_hp = 5
        self.ui_elements = {
            "heart_full": load_ui_item("Icon_Small_HeartFull.png", (32, 32)),
            "heart_empty": load_ui_item("Icon_Small_HeartEmpty.png", (32, 32))
        }
        self.level_text = self.font.render(f"Level {self.level}", True, WHITE)
        self.score_text = self.font.render(f"Score {self.score}", True, WHITE)
        self.hp_text = self.font.render("HP ", True, WHITE)

    def draw(self, player_hp: int):
        """
        Draw the UI.

        Parameters
        ----------
        player_hp : int
            The player's current HP.
        """
        # Draw the upper margin
        pygame.draw.rect(self.screen, (139, 69, 19), (0, 0, WINDOW_WIDTH, 50))

        # Draw the HP bar
        self.screen.blit(self.hp_text, (10, 7))
        for i in range(self.max_hp):
            if i < player_hp:
                self.screen.blit(self.ui_elements["heart_full"], (90 + i * 32, 8))
            else:
                self.screen.blit(self.ui_elements["heart_empty"], (90 + i * 32, 8))
        # Draw the score
        self.screen.blit(self.score_text, (WINDOW_WIDTH - 270, 7))
        # Draw the level
        self.screen.blit(self.level_text, (WINDOW_WIDTH - 520, 7))

    def update_score(self, score: int):
        """
        Update the score.

        Parameters
        ----------
        score : int
            The new score.
        """
        self.score = score
        self.score_text = self.font.render(f"Score {self.score}", True, WHITE)

    def update_level(self, level: int):
        """
        Update the level.

        Parameters
        ----------
        level : int
            The new level.
        """
        self.level = level
        self.level_text = self.font.render(f"Level {self.level}", True, WHITE)


class MenuScreen():
    """
    The main menu screen class.
    """
    def __init__(self, screen: pygame.SurfaceType, font: pygame.font.FontType):
        """
        Initialize the menu screen.

        Parameters
        ----------
        screen : pygame.SurfaceType
            The screen to draw the menu on.
        font : pygame.font.FontType
            The font to use for the menu.
        """
        self.screen = screen
        self.font = font
        self.title_text = self.font.render("Ninja vs. Bakugan", True, WHITE)
        self.title_rect = self.title_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.menu_text = self.font.render("Press S key or click to start", True, WHITE)
        self.menu_rect = self.menu_text.get_rect(center=(WINDOW_WIDTH // 2,
                                                         WINDOW_HEIGHT // 2))
        self.controls_text = self.font.render("Controls: Mouse", True, WHITE)
        self.controls_rect = self.controls_text.get_rect(center=(WINDOW_WIDTH // 2,
                                                                 WINDOW_HEIGHT - 50))
        self.difficulty_text = self.font.render("Difficulty: Easy", True, WHITE)
        self.difficulty_rect = self.difficulty_text.get_rect(center=(WINDOW_WIDTH // 2,
                                                                     WINDOW_HEIGHT - 100))
        self.difficulty = 0
        self.controls = 0
        self.controls_text_list = ["Controls: Mouse",
                                   "Controls: Keyboard"]
        self.difficulty_text_list = ["Difficulty: Easy",
                                     "Difficulty: Medium",
                                     "Difficulty: Hard"]
        self.menu_timer = 0
        self.menu_fps = 10
        self.highscore_timer = 0
        self.highscore = self.load_highscore()
        self.highscore_text = self.font.render(f"Highscore: {self.highscore}", True, WHITE)

    def draw(self):
        """
        Draw the menu screen.
        """
        self.screen.fill(BLACK)
        # Draw title background with shape
        pygame.draw.rect(self.screen, (139, 69, 19), (0, 0, WINDOW_WIDTH, 400))
        pygame.draw.rect(self.screen, (139, 69, 19), (0, 0, 400, 400), border_radius=400)
        pygame.draw.rect(self.screen, (139, 69, 19), (WINDOW_WIDTH - 400, 0, 400, 400), border_radius=400)
        # Draw title
        self.screen.blit(self.title_text, self.title_rect)
        # Draw menu text
        self.screen.blit(self.menu_text, self.menu_rect)

        # Draw controls text in 3D style with shadow
        self.controls_text = self.font.render(f"{self.controls_text_list[self.controls]} (TOGGLE: ENTER)", True, WHITE)
        self.controls_rect = self.controls_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        self.screen.blit(self.controls_text, (self.controls_rect.x + 2, self.controls_rect.y + 2))

        # Draw difficulty text in 3D style with shadow
        self.difficulty_text = self.font.render(f"{self.difficulty_text_list[self.difficulty]} (TOGGLE: SPACE)", True, WHITE)
        self.difficulty_rect = self.difficulty_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
        self.screen.blit(self.difficulty_text, (self.difficulty_rect.x + 2, self.difficulty_rect.y + 2))

        # Draw highscore text
        #if self.highscore_timer > 0:
        #    self.screen.blit(self.highscore_text, (WINDOW_WIDTH - 200, 8))

    def update_highscore(self, highscore: int):
        """
        Update the highscore.

        Parameters
        ----------
        highscore : int
            The new highscore.
        """
        self.highscore = highscore
        self.highscore_text = self.font.render(f"Highscore: {self.highscore}", True, WHITE)

    def update_controls(self):
        """
        Update the controls text.
        """
        self.controls = (self.controls + 1) % 2
        controls_text = f"{self.controls_text_list[self.controls]} (TOGGLE: ENTER)"
        self.controls_text = self.font.render(controls_text, True, WHITE)

    def update_difficulty(self):
        """
        Update the difficulty text.
        """
        self.difficulty = (self.difficulty + 1) % 3
        difficulty_text = f"{self.difficulty_text_list[self.difficulty]} (TOGGLE: SPACE)"
        self.difficulty_text = self.font.render(difficulty_text, True, WHITE)

    def persist_highscore(self):
        """
        Persist the highscore to a file.
        Highscore as a single integer and player name in the format "name:score".
        """
        with open("highscore.txt", "w", encoding="utf8") as highscorefile:
            highscorefile.write(f"{self.highscore}")

    def load_highscore(self) -> dict:
        """
        Get the highscore from the file.
        If the file does not exist, create it.
        It should contain the highscore as a single integer,
        and player name in the format "name:score".
        """
        try:
            with open("highscore.txt", "r", encoding="utf8") as highscorefile:
                highscore = highscorefile.read().strip()
        except FileNotFoundError:
            with open("highscore.txt", "w", encoding="utf8") as highscorefile:
                highscorefile.write("No One:0")
            highscore = "No One:0"
        return highscore.split(":")

    def get_menu_input(self):
        """
        Get the menu input.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.update_difficulty()
        if keys[pygame.K_RETURN]:
            self.update_controls()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        # Start the game if the player presses the S key or any mouse button
        if keys[pygame.K_s] or any(pygame.mouse.get_pressed()):
            return (self.difficulty, self.controls)

    def menu_loop(self):
        """
        The menu loop.
        """
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(self.menu_fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw()
            pygame.display.flip()
            menu_input = self.get_menu_input()
            if menu_input:
                return menu_input
