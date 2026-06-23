"""Player: управление стрелками, установка бомб, сбор улучшений"""

import pygame

from .bomb import Bomb
from .config import Direction, TILE_SIZE, COLOURS, SPEED_BOOST, FIRE_BOOST
from .entities import Entity


class Player(Entity):
    
    # O(1)
    def __init__(self, col, row, colour=COLOURS['BLUE'],
                 up=pygame.K_UP, down=pygame.K_DOWN,
                 left=pygame.K_LEFT, right=pygame.K_RIGHT,
                 bomb_key=pygame.K_SPACE):
        super().__init__(col, row, colour)
        self.up_key = up
        self.down_key = down
        self.left_key = left
        self.right_key = right
        self.bomb_key = bomb_key
        self.player_name = None

    # O(1)
    def handle_input(self, keys):
        new_dir = Direction.NONE
        if keys[self.up_key]:
            new_dir = Direction.UP
        elif keys[self.down_key]:
            new_dir = Direction.DOWN
        elif keys[self.left_key]:
            new_dir = Direction.LEFT
        elif keys[self.right_key]:
            new_dir = Direction.RIGHT
        
        if new_dir != self.direction:
            self.direction = new_dir
            self._snap_to_grid()
        
    # O(B + P) — B = бомбы, P = пауэрапы
    def update(self, game_map, bombs, powerups):
        if not self.alive:
            return
        x, y = self.direction.value
        old_x, old_y = self.pixel_x, self.pixel_y
        self.move(x, y, game_map, bombs)
        moved = (self.pixel_x != old_x or self.pixel_y != old_y)
        self._update_animation(moved)
        for pu in powerups[:]:
            if self.rect().colliderect(pu.rect()):
                pu.apply(self)
                powerups.remove(pu)
    
    # O(1)
    def place_bomb(self):
        if self.active_bomb < self.max_bombs:
            self.active_bomb += 1
            return Bomb(self.row, self.col, self.bomb_range, self)
        return None
    