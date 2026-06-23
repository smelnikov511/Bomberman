"""ResultScreen — экран победы/поражения (замена GameOver + Win)"""

import pygame
from .config import COLOURS, WINDOW_HEIGHT, WINDOW_WIDTH


class ResultScreen:

    # O(1)
    def __init__(self):
        self.font = pygame.font.Font(None, 72)
        self.hint_font = pygame.font.Font(None, 36)

    # O(1)
    def render(self, screen, bg_sprite, fallback_color, title_text):
        if bg_sprite:
            screen.blit(bg_sprite, (0, 0))
        else:
            screen.fill(fallback_color)
        title = self.font.render(title_text, True, COLOURS['WHITE'])
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        screen.blit(title, title_rect)
        hint = self.hint_font.render(
            "Нажмите SPACE для рестарта, ESC чтобы вернуться в Меню",
            True, COLOURS['WHITE']
        )
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        screen.blit(hint, hint_rect)
