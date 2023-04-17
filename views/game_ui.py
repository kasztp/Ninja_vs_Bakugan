"""
The gameplay view.
"""
import pygame
from utils import COLORS, CONFIG, WINDOW_WIDTH, load_ui_item

# Initialize Pygame
pygame.init()


class GameUI:
    """
    The game UI class.
    """

    def __init__(
        self, screen: pygame.SurfaceType, font: pygame.font.FontType = CONFIG.ui_font
    ):
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
            "heart_empty": load_ui_item("Icon_Small_HeartEmpty.png", (32, 32)),
        }
        self.level_text = self.font.render(f" LVL {self.level}", True, COLORS.white)
        self.score_text = self.font.render(f"Score {self.score}", True, COLORS.white)
        self.hp_text = self.font.render("HP ", True, COLORS.white)

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
        self.screen.blit(self.hp_text, (10, 9))
        for i in range(self.max_hp):
            if i < player_hp:
                self.screen.blit(self.ui_elements["heart_full"], (90 + i * 32, 8))
            else:
                self.screen.blit(self.ui_elements["heart_empty"], (90 + i * 32, 8))
        # Draw the score
        self.screen.blit(self.score_text, (WINDOW_WIDTH - 270, 9))
        # Draw the level
        self.screen.blit(self.level_text, (WINDOW_WIDTH - 520, 9))

    def update_score(self, score: int):
        """
        Update the score.

        Parameters
        ----------
        score : int
            The new score.
        """
        self.score = score
        self.score_text = self.font.render(f"Score {self.score}", True, COLORS.white)

    def update_level(self, level: int):
        """
        Update the level.

        Parameters
        ----------
        level : int
            The new level.
        """
        self.level = level
        self.level_text = self.font.render(f" LVL {self.level}", True, COLORS.white)
