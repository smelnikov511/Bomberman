"""Enemy AI: случайное блуждание + установка бомб рядом с игроком"""

import random

from .bomb import Bomb
from .config import Direction, TileType, COLOURS, ENEMY_SPEED
from .entities import Entity


class Enemy(Entity):

    def __init__(self, col, row):
        super().__init__(col, row, COLOURS['RED'])
        self.speed = ENEMY_SPEED
        self.bomb_cooldown = 0

    # Выбор приоритетной цели: powerup, игрок или None
    def _choose_target(self, game_map, player, powerups):
        best_pu = None
        best_dist = float('inf')
        for pu in powerups:
            d = abs(self.col - pu.col) + abs(self.row - pu.row)
            if d < best_dist:
                best_dist = d
                best_pu = pu
        if best_pu and best_dist <= 4:
            return (best_pu.col, best_pu.row)
        return None

    # Направление к целевой клетке (col, row)
    def _direction_to(self, target_col, target_row):
        dx = target_col - self.col
        dy = target_row - self.row
        if abs(dx) > abs(dy):
            return Direction.RIGHT if dx > 0 else Direction.LEFT
        if dy != 0:
            return Direction.DOWN if dy > 0 else Direction.UP
        if dx != 0:
            return Direction.RIGHT if dx > 0 else Direction.LEFT
        return None

    # Проверка, есть ли рядом с врагом SOFT_WALL
    def _wall_nearby(self, game_map):
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            c, r = self.col + dx, self.row + dy
            if game_map.is_within_bounds(c, r) and game_map.grid[r][c] == TileType.SOFT_WALL:
                return True
        return False

    # Нужно ли ставить бомбу: игрок рядом или рядом SOFT_WALL
    def _should_place_bomb(self, game_map, player):
        if self._wall_nearby(game_map):
            return True
        dist = abs(self.row - player.row) + abs(self.col - player.col)
        if dist <= 2:
            return True
        return False

    # Поставить бомбу
    def _place_bomb(self):
        if self.active_bomb < self.max_bombs:
            self.active_bomb += 1
            return Bomb(self.row, self.col, self.bomb_range, self)
        return None

    def update(self, game_map, bombs, player, powerups):
        if not self.alive:
            return None
        self.bomb_cooldown = max(0, self.bomb_cooldown - 1)

        # Сбор powerup'ов
        for pu in powerups[:]:
            if self.rect().colliderect(pu.rect()):
                pu.apply(self)
                powerups.remove(pu)

        # Выбор цели и движение к ней
        target = self._choose_target(game_map, player, powerups)
        if target:
            direction = self._direction_to(target[0], target[1])
            if direction:
                self.direction = direction
                self._snap_to_grid()

        # Попытка движения
        x, y = self.direction.value
        old_x, old_y = self.pixel_x, self.pixel_y
        self.move(x, y, game_map, bombs)

        # При коллизии — случайное направление
        if self.pixel_x == old_x and self.pixel_y == old_y:
            self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
            self._snap_to_grid()

        # Решение поставить бомбу
        if self.bomb_cooldown == 0 and self._should_place_bomb(game_map, player):
            self.bomb_cooldown = 60
            return self._place_bomb()
        return None
