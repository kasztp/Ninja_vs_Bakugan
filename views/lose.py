import pygame
from utils import CONFIG, COLORS, load_sprite

enemy_image = load_sprite("enemy.png", (100, 100))
WINDOW_WIDTH = CONFIG.resolution[0]
WINDOW_HEIGHT = CONFIG.resolution[1]

# Initialize Pygame
pygame.init()


def lose(
    screen: pygame.SurfaceType,
    score: int,
    enemy_image: pygame.SurfaceType = enemy_image,
) -> None:
    """
    Display the losing screen.
    Render the lose screen and animate the enemy sprite to the left and right of the lose text.
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
        The player's side sprite. Default is the enemy sprite from the utils module.

    Returns
    -------
    None
    """
    pygame.mouse.set_visible(True)
    for i in range(0, 400):
        screen.fill(COLORS.black)
        game_over_text = CONFIG.ui_font.render("You Lost!", True, COLORS.red)
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        screen.blit(game_over_text, game_over_text_rect)
        score_text = CONFIG.ui_font.render(f"Score: {score}", True, COLORS.white)
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50)
        screen.blit(score_text, score_text_rect)

        if i % 2 == 0:
            screen.blit(
                enemy_image,
                (game_over_text_rect.centerx - 300, game_over_text_rect.centery - 30),
            )
            screen.blit(
                pygame.transform.flip(enemy_image, True, False),
                (game_over_text_rect.centerx + 200, game_over_text_rect.centery - 50),
            )
        else:
            screen.blit(
                pygame.transform.flip(enemy_image, True, False),
                (game_over_text_rect.centerx - 300, game_over_text_rect.centery - 50),
            )
            screen.blit(
                enemy_image,
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
