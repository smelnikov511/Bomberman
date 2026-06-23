import pygame

from .config import COLOURS, WINDOW_WIDTH, WINDOW_HEIGHT
from .sprites import Sprites


LABELS = ['Player 1', 'Player 2', 'Player 3', 'Player 4']
CHOICES = ['Нет', 'Player', 'AI']


class Menu:

    def __init__(self):
        self.slot = 0
        self.selections = [1, 1, 2, 0]  # Player, Player, AI, Нет
        self.slot_font = pygame.font.Font(None, 48)
        self.choice_font = pygame.font.Font(None, 42)

    def get_config(self):
        result = []
        for s in self.selections:
            if s == 0:
                result.append(None)
            elif s == 1:
                result.append('player')
            else:
                result.append('ai')
        return result

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.slot = (self.slot - 1) % 4
            elif event.key == pygame.K_DOWN:
                self.slot = (self.slot + 1) % 4
            elif event.key == pygame.K_LEFT:
                self.selections[self.slot] = (self.selections[self.slot] - 1) % 3
            elif event.key == pygame.K_RIGHT:
                self.selections[self.slot] = (self.selections[self.slot] + 1) % 3
            elif event.key == pygame.K_SPACE:
                if any(s != 0 for s in self.selections):
                    return 'start'
            elif event.key == pygame.K_ESCAPE:
                return 'quit'
        return None

    def render(self, screen):
        bg = Sprites.bg_menu
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(COLOURS['PURPLE'])

        start_y = 920
        row_h = 70

        for i in range(4):
            y = start_y + i * row_h

            colour = COLOURS['YELLOW'] if i == self.slot else COLOURS['WHITE']
            label = self.slot_font.render(LABELS[i], True, colour)
            screen.blit(label, (1020, y))

            for j, choice in enumerate(CHOICES):
                x = 1200 + j * 150
                if j == self.selections[i] and i == self.slot:
                    c = COLOURS['YELLOW']
                    text = f"[{choice}]"
                elif j == self.selections[i]:
                    c = COLOURS['WHITE']
                    text = f"[{choice}]"
                else:
                    c = COLOURS['WHITE']
                    text = f" {choice} "
                rendered = self.choice_font.render(text, True, c)
                screen.blit(rendered, (x, y))

        hint = self.choice_font.render("SPACE — старт, ESC — выход", True, COLOURS['WHITE'])
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 60))
        screen.blit(hint, hint_rect)
