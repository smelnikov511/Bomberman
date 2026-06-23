import pygame
from .config import COLOURS, EXPLOSION_DURATION, TILE_SIZE
from .sprites import Sprites


class Explosion():

    # O(1)
    def __init__(self, segments):
        self.segments = segments
        self.timer = EXPLOSION_DURATION

    # O(1)
    def update(self):
        self.timer -= 1
        return self.timer <= 0

    # O(S) — S = количество сегментов взрыва
    def render(self, screen):
        Sprites.ensure()
        for col, row in self.segments:
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            if Sprites.explosion:
                screen.blit(Sprites.explosion, (x, y))
            else:
                pygame.draw.rect(screen, COLOURS['ORANGE'], (x, y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, COLOURS['YELLOW'], (x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8))
