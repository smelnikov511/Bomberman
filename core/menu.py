"""Menu: стартовый экран"""

import pygame
from .config import COLOURS, WINDOW_WIDTH, WINDOW_HEIGHT

class Menu:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 80)    # крупный заголовок
        self.info_font = pygame.font.Font(None, 36)      # подписи

    def render(self, screen):
        screen.fill(COLOURS['PURPLE'])
    
        title = self.title_font.render("BOMBERMAN", True, COLOURS['GREEN'])
        title_rect = title.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60)
        )
        screen.blit(title, title_rect)

        hint = self.info_font.render("Нажмите SPACE чтобы играть, ESC чтобы выйти", True, COLOURS['WHITE'])
        hint_rect = hint.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20)
        )
        screen.blit(hint, hint_rect)