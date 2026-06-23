"""GameOver - окно после смерти или победы"""

import pygame
from .config import COLOURS, WINDOW_HEIGHT, WINDOW_WIDTH
from .sprites import Sprites


class GameOver():

    def __init__(self):
        self.font = pygame.font.Font(None, 72)
        self.hint_font = pygame.font.Font(None, 36)

    def render(self, screen):
        bg = Sprites.bg_gameover
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill((40, 10, 10))   # тёмно-красный фон
        title = self.font.render("GAME OVER", True, COLOURS['WHITE'])
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        screen.blit(title, title_rect)
        hint = self.hint_font.render("Нажмите SPACE для рестарта, ESC чтобы вернуться в Меню", True, COLOURS['WHITE'])
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        screen.blit(hint, hint_rect)
