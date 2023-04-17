import pygame
from utils import CONFIG, COLORS, load_sprite

player_side_image = load_sprite("ninja_side.png", (100, 100))
WINDOW_WIDTH = CONFIG.resolution[0]
WINDOW_HEIGHT = CONFIG.resolution[1]

# Initialize Pygame
pygame.init()


def win(
    screen: pygame.SurfaceType,
    score: int,
    player_side_image: pygame.SurfaceType = player_side_image,
) -> None:
    """
    Display the win screen.
    Render the win screen and animate the player's side sprite to the left and right of the win text.
    Loop until the player presses any key, or clicks.
    If the player does not press any key or click, the screen will be redrawn every 250 milliseconds.
    Quit the screen after showing it for 10 seconds.

    Parameters
    ----------
    screen : pygame.SurfaceType
        The screen to draw the win screen on.
    score : int
        The player's score.
    player_side_image : pygame.SurfaceType
        The player's side sprite. Default is the player's side sprite from the utils module.

    Returns
    -------
    None
    """
    pygame.mouse.set_visible(True)
    for i in range(0, 400):
        screen.fill(COLORS.white)
        game_over_text = CONFIG.ui_font.render("You Won!", True, COLORS.green)
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        screen.blit(game_over_text, game_over_text_rect)
        score_text = CONFIG.ui_font.render(f"Score: {score}", True, COLORS.black)
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50)
        screen.blit(score_text, score_text_rect)

        if i % 2 == 0:
            screen.blit(
                player_side_image,
                (game_over_text_rect.centerx - 300, game_over_text_rect.centery - 30),
            )
            screen.blit(
                pygame.transform.flip(player_side_image, True, False),
                (game_over_text_rect.centerx + 200, game_over_text_rect.centery - 50),
            )
        else:
            screen.blit(
                pygame.transform.flip(player_side_image, True, False),
                (game_over_text_rect.centerx - 300, game_over_text_rect.centery - 50),
            )
            screen.blit(
                player_side_image,
                (game_over_text_rect.centerx + 200, game_over_text_rect.centery - 30),
            )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                pygame.mouse.set_visible(True)
                pygame.event.clear()
                return None

        pygame.time.wait(250)
    return None
