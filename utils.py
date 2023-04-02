"""
Utility functions for the game.
"""
import os
import pygame
import yaml

# Define some colors for later use
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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


def load_backgrounds(how_many_to_load: int) -> list[pygame.SurfaceType]:
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
            backgrounds.append(image)
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
    def __init__(self, screen: pygame.SurfaceType, font: pygame.font.FontType):
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
        self.level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.hp_text = self.font.render(f"HP: ", True, WHITE)

    def draw(self, hp: int):
        """
        Draw the UI.

        A 50px lightbrown margin is left at the top of the screen for the UI.
        The edges of the upper margin are rounded, marked with darker brown.
        HP, score and level are displayed in this top margin.

        Parameters
        ----------
        hp : int
            The player's current HP.
        """
        # Draw the upper margin
        pygame.draw.rect(self.screen, (139, 69, 19), (0, 0, WINDOW_WIDTH, 50))
        pygame.draw.rect(self.screen, (139, 69, 19), (0, 0, 50, 50), border_radius=50)
        pygame.draw.rect(self.screen, (139, 69, 19), (WINDOW_WIDTH - 50, 0, 50, 50), border_radius=50)
        # Draw the HP bar
        self.screen.blit(self.hp_text, (8, 8))
        for i in range(self.max_hp):
            if i < hp:
                self.screen.blit(self.ui_elements["heart_full"], (50 + i * 32, 8))
            else:
                self.screen.blit(self.ui_elements["heart_empty"], (50 + i * 32, 8))
        # Draw the score
        self.screen.blit(self.score_text, (WINDOW_WIDTH - 200, 8))
        # Draw the level
        self.screen.blit(self.level_text, (WINDOW_WIDTH - 400, 8))
    
    def update_score(self, score: int):
        """
        Update the score.

        Parameters
        ----------
        score : int
            The new score.
        """
        self.score = score
        self.score_text = self.font.render(f"Score: {self.score}", True, WHITE)
    
    def update_level(self, level: int):
        """
        Update the level.

        Parameters
        ----------
        level : int
            The new level.
        """
        self.level = level
        self.level_text = self.font.render(f"Level: {self.level}", True, WHITE)
