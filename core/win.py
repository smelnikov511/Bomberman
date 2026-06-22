"""Win: экран победы"""

import pygame
from .config import COLOURS, WINDOW_HEIGHT, WINDOW_WIDTH


class Win:

    def __init__(self):
        self.font = pygame.font.Font(None, 72)
        self.hint_font = pygame.font.Font(None, 36)

    def render(self, screen, winner_text="ПОБЕДА!"):
        screen.fill((10, 40, 10))
        title = self.font.render(winner_text, True, COLOURS['WHITE'])
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        screen.blit(title, title_rect)
        hint = self.hint_font.render("Нажмите SPACE для рестарта, ESC чтобы вернуться в Меню", True, COLOURS['GREY'])
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        screen.blit(hint, hint_rect)
