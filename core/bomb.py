"""Bomb: таймер 3с, взрыв"""

import pygame

from .config import TileType, BOMB_TIMER, COLOURS, POWERUP_DROP_CHANCE, TILE_SIZE
from .explosion import Explosion


class Bomb():

    def __init__(self, row, col, bomb_range, owner):
        self.row = row
        self.col = col
        self.bomb_range = bomb_range
        self.owner = owner
        self.timer = BOMB_TIMER
        self.exploded = False  # Взорвалась ли бомба или нет
        self.pixel_x = col * TILE_SIZE
        self.pixel_y = row * TILE_SIZE
        self.owner_can_pass = True  # владелец может пройти через бомбу
    
    def update(self, game_map, entities, bombs):
        if self.exploded:
            return None
        self.timer -= 1
        if self.timer > 0:
            return None
        return self.explode(game_map, entities, bombs)

    def explode(self, game_map, entities, bombs):
        self.exploded = True
        self.owner.active_bomb -= 1
        segments = [(self.col, self.row)]

        direction = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for x, y in direction:
            for dist in range(1, self.bomb_range + 1):
                c = self.col + x * dist
                r = self.row + y * dist
                if not game_map.is_within_bounds(c, r):
                    break
                tile = game_map.grid[r][c]
                if tile == TileType.HARD_WALL:
                    break
                if tile == TileType.SOFT_WALL:
                    segments.append((c, r))
                    game_map.destroy_soft_wall(c, r)
                    break
                # if tile == EMPTY
                segments.append((c, r))
    
        for bomb in bombs[:]:
            if bomb is self or bomb.exploded:
                continue
            if (bomb.col, bomb.row) in segments:
                bomb.explode(game_map, entities, bombs)

        for entity in entities:
            if not entity.alive:
                continue
            for c, r in segments:
                seg_rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if seg_rect.colliderect(entity.rect()):
                    entity.die()
                    break
        return Explosion(segments)
    
    def render(self, screen):
        pygame.draw.rect(screen, COLOURS['BLACK'], (self.pixel_x, self.pixel_y, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, COLOURS['WHITE'], (self.pixel_x + 2, self.pixel_y + 2, TILE_SIZE - 4, TILE_SIZE - 4))