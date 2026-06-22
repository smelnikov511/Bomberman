"""Player: управление стрелками, установка бомб, сбор улучшений"""

import pygame

from .bomb import Bomb
from .config import Direction, TILE_SIZE, COLOURS, SPEED_BOOST, FIRE_BOOST
from .entities import Entity


class Player(Entity):
    
    def __init__(self, col, row):
        super().__init__(col, row, COLOURS['BLUE'])

    def handle_input(self, keys):
        new_dir = Direction.NONE
        if keys[pygame.K_UP]:
            new_dir = Direction.UP
        elif keys[pygame.K_DOWN]:
            new_dir = Direction.DOWN
        elif keys[pygame.K_LEFT]:
            new_dir = Direction.LEFT
        elif keys[pygame.K_RIGHT]:
            new_dir = Direction.RIGHT
        
        if new_dir != self.direction:
            self.direction = new_dir
            self._snap_to_grid()
        
    def update(self, game_map, bombs):
        if not self.alive:
            return
        x, y = self.direction.value
        self.move(x, y, game_map, bombs)
    
    def place_bomb(self):
        if self.active_bomb < self.max_bombs:
            self.active_bomb += 1
            return Bomb(self.row, self.col, self.bomb_range, self)
        return None
    