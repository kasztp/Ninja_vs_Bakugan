"""
The menu view.
"""
import sys
import os
import logging
from datetime import datetime
import pygame
from utils import (
    COLORS,
    CONFIG,
    WINDOW_HEIGHT,
    WINDOW_WIDTH
)

# Set the logging level
logging.basicConfig(filename="game.log", level=logging.DEBUG)
logging.debug(f"{datetime.now()} - Menu.py loaded")

# Define assets path
assets_path = os.path.join(os.getcwd(), "assets")

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ninja vs Bakugan")

# Load font
font_size = 36
font = pygame.font.Font(CONFIG.paths.main_font, font_size)

# Define option menu settings
difficulty_setting = 0 # Index of the current difficulty option
control_setting = 0 # Index of the current control option

# Define background images
background_path = os.path.join(assets_path, "backgrounds", "hidden_interior.jpg")
background = pygame.transform.scale(pygame.image.load(background_path).convert(),
                                    (WINDOW_WIDTH, WINDOW_HEIGHT))


def create_text(text, text_size, color, font_path=CONFIG.paths.main_font):
    """
    Create a text surface and rect.

    Parameters
    ----------
    text : str
        The text to display.
    font_size : int
        The size of the font.
    color : tuple
        The color of the text.
    font_path : str
        The path to the font file. Defaults to the global font_path.

    Returns
    -------
    text_surface : pygame.SurfaceType
        The text surface.
    text_rect : pygame.RectType
        The text rect.
    """
    font = pygame.font.Font(font_path, text_size)
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def draw_menu(highlighted_option=None, paused=False):
    """
    Draw the main menu, highlight the hovered option

    Parameters
    ----------
    highlighted_option : int
        The index of the option to highlight.
    paused : bool
        Whether the game is paused or not.

    Returns
    -------
    None
    """
    title_font_size = 48
    screen.blit(background, (0, 0))
    title_surface, title_rect = create_text("Ninja vs Bakugan", title_font_size, COLORS.white)
    title_rect.center = (WINDOW_WIDTH // 2, 40)
    screen.blit(title_surface, title_rect)

    # Define menu positions
    menu_spacing = 100
    menu_x = WINDOW_WIDTH // 4 - 30
    menu_y = 280

    # Define menu options
    if paused:
        menu_options = [
                        ("RESUME", COLORS.white),
                        ("OPTIONS", COLORS.white),
                        ("QUIT", COLORS.white),
                    ]
    else:
        menu_options = [
                        ("START", COLORS.white),
                        ("OPTIONS", COLORS.white),
                        ("QUIT", COLORS.white),
                    ]
    menu_option_rects = []

    for i, (text, color) in enumerate(menu_options):
        if i == highlighted_option:
            color = COLORS.green
        option_surface, option_rect = create_text(text, font_size, color)
        option_rect.center = (menu_x, menu_y + i * menu_spacing)
        screen.blit(option_surface, option_rect)
        menu_option_rects.append(option_rect)

    pygame.display.update()

    return menu_option_rects


def menu_loop(paused=False) -> tuple[int, int]:
    """
    The main menu loop.

    Parameters
    ----------
    paused : bool
        Whether the game is paused or not.

    Returns
    -------
    difficulty_setting : int
        The index of the selected difficulty setting.
    control_setting : int
        The index of the selected control setting.
    """
    global difficulty_setting
    global control_setting
    menu_running = True
    if paused:
        menu_option_rects = draw_menu(paused=True)
    else:
        menu_option_rects = draw_menu()

    while menu_running:
        if pygame.mouse.get_focused():
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(menu_option_rects):
                if rect.collidepoint(mouse_pos):
                    if paused:
                        menu_option_rects = draw_menu(i, paused=True)
                    else:
                        menu_option_rects = draw_menu(i)
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    menu_running = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu_running = False
                case pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(menu_option_rects):
                        if rect.collidepoint(mouse_pos):
                            match i:
                                case 0:
                                    # Start game
                                    return difficulty_setting, control_setting
                                case 1:
                                    # Open options menu
                                    options_menu_loop()
                                case 2:
                                    # Quit game
                                    menu_running = False
    pygame.quit()
    sys.exit()


def options_menu_loop(paused=False):
    """
    The options menu loop.

    Parameters
    ----------
    paused : bool
        Whether the game is paused or not.

    Returns
    -------
    None
    """
    global difficulty_setting
    global control_setting

    # Define option menu items
    option_menu_items = [
        ("DIFFICULTY: ", ["EASY", "NORMAL", "HARD"]),
        ("CONTROLS: ", ["MOUSE", "KEYBOARD"]),
        ("BACK", None)
    ]

    # Calculate positions for menu items
    menu_spacing = 50
    menu_x = WINDOW_WIDTH // 3 - 30
    menu_y = 300
    option_menu_rects = []

    def render_fixed_items():
        """Render the menu background and title."""
        screen.blit(background, (0, 0))
        title_text = "OPTIONS"
        title_text_render = font.render(title_text, True, COLORS.white)
        title_text_rect = title_text_render.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(title_text_render, title_text_rect)

    # Render the menu items the first time
    render_fixed_items()

    def highlight_on_hover(menu_item_idx, selection_idx=None):
        """
        Highlight the menu item if the mouse is hovering over it.

        Parameters
        ----------
        menu_item_idx : int
            The index of the menu item.
        selection_idx : int
            The index of the selection.

        Returns
        -------
        None
        """
        mouse_pos = pygame.mouse.get_pos()
        if option_menu_rects[menu_item_idx].collidepoint(mouse_pos):
            if menu_item_idx == 2:
                option_surface, option_rect = create_text(
                                                option_menu_items[menu_item_idx][0],
                                                font_size,
                                                COLORS.green
                                                )
                option_rect.center = (menu_x,
                                      menu_y + menu_item_idx * menu_spacing)
            elif selection_idx is not None:
                option_surface, option_rect = create_text(
                                                option_menu_items[menu_item_idx][1][selection_idx],
                                                font_size,
                                                COLORS.green
                                                )
                option_rect.center = (menu_x + 300,
                                      menu_y + menu_item_idx * menu_spacing)
            else:
                option_surface, option_rect = create_text(
                                                option_menu_items[menu_item_idx][1][0],
                                                font_size,
                                                COLORS.green
                                                )
                option_rect.center = (menu_x + 300,
                                      menu_y + menu_item_idx * menu_spacing)
            screen.blit(option_surface, option_rect)
            option_menu_rects[menu_item_idx] = option_rect
            pygame.display.update()

    def render_options(initial=False, control_setting=None, difficulty_setting=None):
        """
        Render the options menu.

        Parameters
        ----------
        initial : bool
            Whether this is the first time the options menu is being rendered.
        control_setting : str
            The control setting.
        difficulty_setting : str
            The difficulty setting.

        Returns
        -------
        None
        """
        logging.debug(f"Initial: {initial}, Control Setting: {control_setting},\
                      Difficulty Setting: {difficulty_setting}")
        for i, (label, options) in enumerate(option_menu_items):
            label_surface, label_rect = create_text(label, font_size, COLORS.white)
            label_rect.center = (menu_x, menu_y + i * menu_spacing)
            screen.blit(label_surface, label_rect)
            logging.debug(f"Option Label: {label}, Options: {options}")
            if options is not None:
                if initial:
                    option_surface, option_rect = create_text(options[0],
                                                              font_size,
                                                              COLORS.white
                                                              )
                    option_rect.center = (menu_x + 300,
                                          menu_y + i * menu_spacing)
                    screen.blit(option_surface, option_rect)
                    option_menu_rects.append(option_rect)
                else:
                    if difficulty_setting is not None and i == 0:
                        option_surface, option_rect = create_text(options[difficulty_setting],
                                                                  font_size,
                                                                  COLORS.white
                                                                  )
                        option_rect.center = (menu_x + 300,
                                              menu_y + i * menu_spacing)
                        screen.blit(option_surface, option_rect)
                        option_menu_rects[i] = option_rect
                    elif control_setting is not None and i == 1:
                        option_surface, option_rect = create_text(options[control_setting],
                                                                  font_size,
                                                                  COLORS.white
                                                                  )
                        option_rect.center = (menu_x + 300,
                                              menu_y + i * menu_spacing)
                        screen.blit(option_surface, option_rect)
                        option_menu_rects[i] = option_rect
                    else:
                        option_surface, option_rect = create_text(options[0],
                                                                  font_size,
                                                                  COLORS.white
                                                                  )
                        option_rect.center = (menu_x + 300,
                                              menu_y + i * menu_spacing)
                        screen.blit(option_surface, option_rect)
                        option_menu_rects[i] = option_rect
            elif initial:
                option_menu_rects.append(label_rect)
            else:
                option_menu_rects[i] = label_rect

    # Render the menu options for the first time
    render_options(initial=True)
    pygame.display.update()

    # Loop until the options menu is closed,
    # highlight the current option on mouse hover,
    # and update the option if the user clicks on it.
    # Cycle the option if the user clicks on it again.
    options_menu_running = True
    while options_menu_running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    options_menu_running = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        options_menu_running = False
                case pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(option_menu_rects):
                        if rect.collidepoint(mouse_pos):
                            match i:
                                case 0:
                                    # Toggle difficulty setting
                                    num_difficulties = len(option_menu_items[i][1])
                                    difficulty_setting = (difficulty_setting + 1) % num_difficulties
                                    logging.debug(f"Toggled Option Menu Item: \
                                                  {option_menu_items[difficulty_setting]}")
                                    option_surface, option_rect = create_text(
                                                                    option_menu_items[i][1][difficulty_setting],
                                                                    font_size,
                                                                    COLORS.white
                                                                )
                                    option_rect.center = (menu_x + 300,
                                                          menu_y + i * menu_spacing)
                                    option_menu_rects[i] = option_rect
                                case 1:
                                    # Toggle control setting
                                    num_controls = len(option_menu_items[i][1])
                                    control_setting = (control_setting + 1) % num_controls
                                    logging.debug(f"Toggled Option Menu Item: \
                                                  {option_menu_items[control_setting]}")
                                case 2:
                                    # Return to main menu
                                    options_menu_running = False
                                    break

                            log_text =f"Len Option Items: {len(option_menu_items)}, \
                                        Len Option Rects: {len(option_menu_rects)}, \
                                        i = {i}, Option Items: {option_menu_items}, \
                                        i = {i}, Option Rects: {option_menu_rects}"
                            logging.debug(log_text)

                            # Update the selected option
                            if option_menu_items[i] is not None:

                                render_fixed_items()
                                render_options(control_setting=control_setting,
                                               difficulty_setting=difficulty_setting)

                                screen.blit(option_surface, option_rect)
                                pygame.display.update(option_rect)

        # Highlight the current option if the mouse is over it
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(option_menu_rects):
            if rect.collidepoint(mouse_pos):
                logging.debug(f"Highlighted Option: {option_menu_items[i][1]}")
                match i:
                    case 0:
                        highlight_on_hover(i, difficulty_setting)
                    case 1:
                        highlight_on_hover(i, control_setting)
                    case 2:
                        highlight_on_hover(i)
            else:
                match i:
                    case 0:
                        option_surface, option_rect = create_text(
                                                        option_menu_items[i][1][difficulty_setting],
                                                        font_size,
                                                        COLORS.white
                                                        )
                        option_rect.center = (menu_x + 300,
                                              menu_y + i * menu_spacing)
                    case 1:
                        option_surface, option_rect = create_text(
                                                        option_menu_items[i][1][control_setting],
                                                        font_size,
                                                        COLORS.white
                                                        )
                        option_rect.center = (menu_x + 300,
                                              menu_y + i * menu_spacing)
                    case 2:
                        option_surface, option_rect = create_text(
                                                        option_menu_items[i][0],
                                                        font_size,
                                                        COLORS.white
                                                        )
                        option_rect.center = (menu_x,
                                              menu_y + i * menu_spacing)

                render_fixed_items()
                render_options(control_setting=control_setting,
                               difficulty_setting=difficulty_setting)
                screen.blit(option_surface, option_rect)
                pygame.display.update(option_rect)

    # Return to main menu
    if paused:
        draw_menu(paused=True)
    else:
        draw_menu()
