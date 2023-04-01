"""
Utility functions for the game.
"""
import os
import pygame


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


def load_background(name: str) -> pygame.SurfaceType:
    """
    Load a background from the backgrounds folder.

    Parameters
    ----------
    name : str
        The name of the background to load.
    
    Returns
    -------
    pygame.SurfaceType
        The loaded background.
    """
    fullname = os.path.join(os.getcwd(), "assets", "backgrounds", name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print("Cannot load image:", fullname)
        raise SystemExit(message) from message
    return image


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
