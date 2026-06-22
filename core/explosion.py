"""Explosion: распространение по 4 направлениям, уничтожение блоков, цепная реакция"""

import pygame
from .config import COLOURS, EXPLOSION_DURATION, TILE_SIZE

class Explosion():

    def __init__(self, segments):
        self.segments = segments
        self.timer = EXPLOSION_DURATION
    
    def update(self):
        self.timer -= 1
        return self.timer <= 0  # True -> взрыв закончился, надо удалить
    
    def render(self, screen):
        for col, row in self.segments:
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            # Внешний слой — оранжевый
            pygame.draw.rect(screen, COLOURS['ORANGE'], (x, y, TILE_SIZE, TILE_SIZE))
            # Внутренний слой — белый/жёлтый
            pygame.draw.rect(screen, COLOURS['YELLOW'], (x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8))