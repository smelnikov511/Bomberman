"""Enemy AI: FSM (FLEE / SEEK_TARGET / WANDER / PLACE_BOMB) + A* pathfinding"""

import random
from collections import deque
from enum import Enum

from .bomb import Bomb
from .config import Direction, TileType, COLOURS, ENEMY_SPEED, TILE_SIZE
from .entities import Entity
from .pathfinding import AStar


class EnemyState(Enum):
    IDLE = 0
    FLEE = 1
    SEEK_TARGET = 2
    WANDER = 3
    PLACE_BOMB = 4


class Enemy(Entity):

    def __init__(self, col, row):
        super().__init__(col, row, COLOURS['RED'])
        self.speed = ENEMY_SPEED
        self.bomb_cooldown = 0
        self.state = EnemyState.WANDER
        self.path = []
        self.wander_timer = random.randint(30, 90)

    def _choose_target(self, game_map, players, enemies, powerups):
        best_target = None
        best_dist = float('inf')
        for pu in powerups:
            d = abs(self.col - pu.col) + abs(self.row - pu.row)
            if d < best_dist:
                best_dist = d
                best_target = (pu.col, pu.row)
        for p in players:
            if not p.alive:
                continue
            d = abs(self.col - p.col) + abs(self.row - p.row)
            if d < best_dist:
                best_dist = d
                best_target = (p.col, p.row)
        for e in enemies:
            if e is self or not e.alive:
                continue
            d = abs(self.col - e.col) + abs(self.row - e.row)
            if d < best_dist:
                best_dist = d
                best_target = (e.col, e.row)
        if best_target and best_dist <= 4:
            return best_target
        return None

    def _wall_nearby(self, game_map):
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            c, r = self.col + dx, self.row + dy
            if game_map.is_within_bounds(c, r) and game_map.grid[r][c] == TileType.SOFT_WALL:
                return True
        return False

    def _find_nearest_safe_tile(self, game_map, bombs, max_dist=12):
        visited = {(self.col, self.row)}
        queue = deque([(self.col, self.row)])
        while queue:
            c, r = queue.popleft()
            if self._is_safe_tile(c, r, game_map, bombs):
                return (c, r)
            if abs(c - self.col) + abs(r - self.row) >= max_dist:
                continue
            for dc, dr in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                nc, nr = c + dc, r + dr
                if not game_map.is_within_bounds(nc, nr):
                    continue
                if game_map.grid[nr][nc] != TileType.EMPTY:
                    continue
                if any(b.col == nc and b.row == nr and not b.exploded for b in bombs):
                    continue
                if (nc, nr) in visited:
                    continue
                visited.add((nc, nr))
                queue.append((nc, nr))
        return None

    def _should_place_bomb(self, game_map, players, enemies, bombs):
        if self.active_bomb >= self.max_bombs:
            return False
        temp = Bomb(self.row, self.col, self.bomb_range, self)
        temp_bombs = list(bombs) + [temp]
        if not self._find_nearest_safe_tile(game_map, temp_bombs):
            return False
        if self._wall_nearby(game_map):
            return True
        for p in players:
            if not p.alive:
                continue
            if abs(self.row - p.row) + abs(self.col - p.col) <= 2:
                return True
        for e in enemies:
            if e is self or not e.alive:
                continue
            if abs(self.row - e.row) + abs(self.col - e.col) <= 2:
                return True
        return False

    def _place_bomb(self):
        if self.active_bomb < self.max_bombs:
            self.active_bomb += 1
            return Bomb(self.row, self.col, self.bomb_range, self)
        return None

    def _is_safe_tile(self, col, row, game_map, bombs):
        for bomb in bombs:
            if bomb.exploded:
                continue
            if (col, row) == (bomb.col, bomb.row):
                return False
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                for dist in range(1, bomb.bomb_range + 1):
                    c = bomb.col + dx * dist
                    r = bomb.row + dy * dist
                    if not game_map.is_within_bounds(c, r):
                        break
                    tile = game_map.grid[r][c]
                    if tile == TileType.HARD_WALL:
                        break
                    if (col, row) == (c, r):
                        return False
                    if tile == TileType.SOFT_WALL:
                        break
        return True

    def _snap_to_cell(self):
        self.pixel_x = self.col * TILE_SIZE
        self.pixel_y = self.row * TILE_SIZE

    def _follow_path(self):
        while self.path and (self.col, self.row) == self.path[0]:
            self.path.pop(0)
            self._snap_to_cell()
        if not self.path:
            return
        dc = self.path[0][0] - self.col
        dr = self.path[0][1] - self.row
        if dc > 0:
            self.direction = Direction.RIGHT
        elif dc < 0:
            self.direction = Direction.LEFT
        elif dr > 0:
            self.direction = Direction.DOWN
        elif dr < 0:
            self.direction = Direction.UP
        self._snap_to_grid()

    def _update_state(self, game_map, bombs, players, enemies, powerups):
        unsafe = not self._is_safe_tile(self.col, self.row, game_map, bombs)

        if unsafe:
            if self.state != EnemyState.FLEE:
                self.state = EnemyState.FLEE
                self.path.clear()
            return

        if self.state == EnemyState.FLEE:
            self.state = EnemyState.IDLE
            self._snap_to_cell()
            self.path.clear()

        if self.state == EnemyState.PLACE_BOMB:
            return

        target = self._choose_target(game_map, players, enemies, powerups)

        if self.state == EnemyState.SEEK_TARGET:
            if not target:
                self.state = EnemyState.IDLE
            return

        if self.state == EnemyState.IDLE and self.active_bomb > 0:
            return

        if self.state in (EnemyState.IDLE, EnemyState.WANDER):
            if self._should_place_bomb(game_map, players, enemies, bombs):
                self.state = EnemyState.PLACE_BOMB
                return
            if target:
                result = AStar.find_path((self.col, self.row), target, game_map, bombs)
                if result:
                    self.state = EnemyState.SEEK_TARGET
                    self.path = result
                    return
            if self.state == EnemyState.IDLE:
                self.state = EnemyState.WANDER

    def _execute_state(self, game_map, bombs, players, enemies, powerups):
        if self.state == EnemyState.FLEE:
            if not self.path:
                goal = self._find_nearest_safe_tile(game_map, bombs)
                if goal:
                    result = AStar.find_path((self.col, self.row), goal, game_map, bombs)
                    self.path = result if result else []
            self._follow_path()

        elif self.state == EnemyState.SEEK_TARGET:
            if not self.path:
                target = self._choose_target(game_map, players, enemies, powerups)
                if target:
                    result = AStar.find_path((self.col, self.row), target, game_map, bombs)
                    self.path = result if result else []
            self._follow_path()

        elif self.state == EnemyState.WANDER:
            if self.direction == Direction.NONE:
                self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
                self._snap_to_grid()
            if self.wander_timer <= 0:
                self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
                self._snap_to_grid()
                self.wander_timer = random.randint(30, 90)
            self.wander_timer -= 1

        elif self.state == EnemyState.IDLE:
            self.direction = Direction.NONE

    def _on_stuck(self, game_map, bombs):
        if self.state == EnemyState.WANDER:
            self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
            self._snap_to_grid()
            return
        self.path.clear()

    def update(self, game_map, bombs, players, enemies, powerups):
        if not self.alive:
            return None
        self.bomb_cooldown = max(0, self.bomb_cooldown - 1)

        for pu in powerups[:]:
            if self.rect().colliderect(pu.rect()):
                pu.apply(self)
                powerups.remove(pu)

        self._update_state(game_map, bombs, players, enemies, powerups)
        self._execute_state(game_map, bombs, players, enemies, powerups)

        while self.path and (self.col, self.row) == self.path[0]:
            self.path.pop(0)
            self._snap_to_cell()

        x, y = self.direction.value
        old_x, old_y = self.pixel_x, self.pixel_y
        self.move(x, y, game_map, bombs)

        if self.pixel_x == old_x and self.pixel_y == old_y:
            self._on_stuck(game_map, bombs)

        if self.state == EnemyState.PLACE_BOMB:
            self.state = EnemyState.FLEE
            return self._place_bomb()
        return None
