"""Bomb: таймер 3с, взрыв"""

import pygame

from .config import TileType, BOMB_TIMER, COLOURS, TILE_SIZE
from .explosion import Explosion
from .powerup import PowerUp
from .sprites import Sprites


class Bomb():

    # O(1)
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
    
    # Обновление состояния бомбы: уменьшаем таймер, если время вышло — взрываем
    # O(1)
    def update(self, game_map, entities, bombs, powerups):
        if self.exploded:
            return None
        self.timer -= 1
        if self.timer > 0:
            return None
        return self.explode(game_map, entities, bombs, powerups)

    # Распространение взрыва: 4 направления от бомбы до HARD_WALL/SOFT_WALL,
    # разрушение стен, спавн пауэрапов, цепная реакция, урон сущностям
    # O(R + B + E + P) — R = радиус, B = бомбы, E = сущности, P = пауэрапы
    def explode(self, game_map, entities, bombs, powerups):
        self.exploded = True
        self.owner.active_bomb -= 1
        segments = [(self.col, self.row)]
        existing_powerups = list(powerups)  # копия старых powerup'ов до спавна новых

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
                    pu = PowerUp.try_spawn(c, r)
                    if pu:
                        powerups.append(pu)
                    break
                # Взрыв останавливается на тайле с powerup
                if any(pu.col == c and pu.row == r for pu in powerups):
                    segments.append((c, r))
                    break
                # if tile == EMPTY
                segments.append((c, r))
    
        # Цепная реакция: если сегмент взрыва достиг другой бомбы — взрываем рекурсивно
        for bomb in bombs[:]:
            if bomb is self or bomb.exploded:
                continue
            if (bomb.col, bomb.row) in segments:
                chained = bomb.explode(game_map, entities, bombs, powerups)
                if chained:
                    segments.extend(chained.segments)

        for entity in entities:
            if not entity.alive:
                continue
            for c, r in segments:
                seg_rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if seg_rect.colliderect(entity.rect()):
                    entity.die()
                    break

        for pu in existing_powerups:
            for c, r in segments:
                seg_rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if seg_rect.colliderect(pu.rect()) and pu in powerups:
                    powerups.remove(pu)
                    break

        return Explosion(segments)
    
    # O(1)
    def render(self, screen):
        Sprites.ensure()
        if Sprites.bomb:
            screen.blit(Sprites.bomb, (self.pixel_x, self.pixel_y))
        else:
            pygame.draw.rect(screen, COLOURS['BLACK'], (self.pixel_x, self.pixel_y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, COLOURS['WHITE'], (self.pixel_x + 2, self.pixel_y + 2, TILE_SIZE - 4, TILE_SIZE - 4))