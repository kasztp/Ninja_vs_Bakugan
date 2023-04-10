"""
Utility functions for the game.
"""
import os
from collections import namedtuple
from dataclasses import dataclass
from typing import NamedTuple
import pygame

# Initialize Pygame
pygame.init()

# Define some colors for later use
COLORS = namedtuple("COLORS", "black white red green blue")
COLORS.black = (0, 0, 0)
COLORS.white = (255, 255, 255)
COLORS.red = (255, 0, 0)
COLORS.green = (0, 255, 0)
COLORS.blue = (0, 0, 255)

ConfigPaths = namedtuple("paths", "assets sprites backgrounds ui fonts main_font sounds screenshots")
ConfigPaths.assets = os.path.join(os.getcwd(), "assets")
ConfigPaths.sprites = os.path.join(os.getcwd(), "assets", "sprites")
ConfigPaths.backgrounds = os.path.join(os.getcwd(), "assets", "backgrounds")
ConfigPaths.ui = os.path.join(os.getcwd(), "assets", "ui")
ConfigPaths.fonts = os.path.join(os.getcwd(), "assets", "fonts")
ConfigPaths.main_font = os.path.join(os.getcwd(), "assets", "fonts", "C64_Pro_Mono-STYLE.ttf")
ConfigPaths.sounds = os.path.join(os.getcwd(), "assets", "sounds")
ConfigPaths.screenshots = os.path.join(os.getcwd(), "screenshots")


@dataclass(frozen=True)
class Config:
    """
    The game config class.
    """
    resolution: tuple[int, int]
    window_title: str = "Ninja vs. Bakugan"
    fps: int = 60
    max_level: int = 10
    paths: NamedTuple = ConfigPaths
    font_size: int = 32
    ui_font: pygame.font.FontType = pygame.font.Font(paths.main_font, font_size)

# Set the game config
CONFIG = Config(
    resolution=(800, 800),
    window_title="Ninja vs. Bakugan"
)

# Define some constants
WINDOW_WIDTH = CONFIG.resolution[0]
WINDOW_HEIGHT = CONFIG.resolution[1]


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


def load_backgrounds(how_many_to_load: int, scale=CONFIG.resolution) -> list[pygame.SurfaceType]:
    """
    Load a given nnumber of backgrounds from the backgrounds folder.

    Parameters
    ----------
    how_many_to_load : int
        The number of backgrounds to load.
    scale : tuple, optional
        The scale to apply to the backgrounds, by default CONFIG.resolution

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
    Wrpaper for pygame.sprite.collide_rect.

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
