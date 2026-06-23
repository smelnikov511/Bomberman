"""Player, Enemy — общие предки Entity"""

import pygame

from .config import Direction, TileType, TILE_SIZE, PLAYER_SPEED, DEFAULT_BOMB_RANGE, DEFAULT_MAX_BOMB, ANIM_SPEED
from .sprites import Sprites

DIR_TO_INDEX = {
    Direction.DOWN: 0,
    Direction.LEFT: 1,
    Direction.RIGHT: 2,
    Direction.UP: 3,
}


class Entity():

    # O(1)
    def __init__(self, col, row, colour):
        self.col = col
        self.row = row
        self.pixel_x = col * TILE_SIZE
        self.pixel_y = row * TILE_SIZE
        self.direction = Direction.NONE
        self.speed = PLAYER_SPEED
        self.bomb_range = DEFAULT_BOMB_RANGE
        self.max_bombs = DEFAULT_MAX_BOMB
        self.active_bomb = 0
        self.alive = True
        self.death_timer = 0
        self.colour = colour
        self.margin = 4
        self.sprite_index = 0
        self.anim_frame = 0
        self.anim_timer = 0

    # O(1)
    def rect(self):
        """Возвращает хитбокс (pygame.Rect) с учётом отступа."""
        return pygame.Rect(
            self.pixel_x + self.margin,
            self.pixel_y + self.margin,
            TILE_SIZE - 2 * self.margin,
            TILE_SIZE - 2 * self.margin
        )
    
    # AABB collision detection: стены (3×3 окрестность) + бомбы
    # (owner_can_pass + current_rect bypass) + границы карты
    # O(B) — B = количество бомб
    def _collides_with(self, x, y, game_map, obstacles):
        test_rect = pygame.Rect(
            x + self.margin, y + self.margin,
            TILE_SIZE - self.margin * 2,
            TILE_SIZE - self.margin * 2,
        )  # Это то, куда персонаж хочет пройти
        current_rect = pygame.Rect(
            self.pixel_x + self.margin, self.pixel_y + self.margin,
            TILE_SIZE - self.margin * 2,
            TILE_SIZE - self.margin * 2,
        )  # Текущая позиция (для проверки "стою на бомбе")

        # Коллизия со стенами — проверяем только тайлы вокруг проверяемой позиции
        min_col = max(0, int(x // TILE_SIZE) - 1)
        max_col = min(game_map.cols - 1, int((x + TILE_SIZE) // TILE_SIZE) + 1)
        min_row = max(0, int(y // TILE_SIZE) - 1)
        max_row = min(game_map.rows - 1, int((y + TILE_SIZE) // TILE_SIZE) + 1)
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                if game_map.grid[row][col] != TileType.EMPTY:
                    wall_rect = pygame.Rect(
                        col * TILE_SIZE,
                        row * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    if test_rect.colliderect(wall_rect):
                        return True
            
        # Коллизия с бомбами
        for bomb in obstacles:
            bomb_rect = pygame.Rect(
                bomb.col * TILE_SIZE,
                bomb.row * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
            if bomb.owner is self and bomb.owner_can_pass:
                if not test_rect.colliderect(bomb_rect):
                    bomb.owner_can_pass = False
                continue
            if current_rect.colliderect(bomb_rect):
                continue
            if test_rect.colliderect(bomb_rect):
                return True
            
        # Границы карты
        if (x < 0 or x + TILE_SIZE > game_map.cols * TILE_SIZE
            or 
            y < 0 or y + TILE_SIZE > game_map.rows * TILE_SIZE):
            return True
            
        return False


    # O(B) — B = количество бомб
    def move(self, x, y, game_map, obstacles):
        if x == 0 and y == 0:
            return
        new_x = self.pixel_x + x * self.speed
        new_y = self.pixel_y + y * self.speed
        if not self._collides_with(new_x, new_y, game_map, obstacles):
            self.pixel_x = new_x
            self.pixel_y = new_y
        elif not self._collides_with(new_x, self.pixel_y, game_map, obstacles):
            self.pixel_x = new_x
        elif not self._collides_with(self.pixel_x, new_y, game_map, obstacles):
            self.pixel_y = new_y
        self.col = round(self.pixel_x / TILE_SIZE)
        self.row = round(self.pixel_y / TILE_SIZE)
    
    # O(1)
    def _snap_to_grid(self):
        if self.direction in (Direction.UP, Direction.DOWN):
            self.pixel_x = self.col * TILE_SIZE
        elif self.direction in (Direction.LEFT, Direction.RIGHT):
            self.pixel_y = self.row * TILE_SIZE

    # O(1)
    def _update_animation(self, moved):
        if moved:
            if self.anim_frame == 0:
                self.anim_frame = 1
                self.anim_timer = 0
            else:
                self.anim_timer += 1
                if self.anim_timer >= ANIM_SPEED:
                    self.anim_timer = 0
                    self.anim_frame = 3 - self.anim_frame
        else:
            self.anim_frame = 0
            self.anim_timer = 0

    # O(1)
    def get_current_sprite(self):
        dir_idx = DIR_TO_INDEX.get(self.direction, 0)
        walk_frames = Sprites.player_walk[self.sprite_index][dir_idx]
        stand = Sprites.player_stand[self.sprite_index]
        if self.anim_frame == 0:
            return stand
        elif self.anim_frame == 1:
            return walk_frames[0] or stand
        else:
            return walk_frames[1] or stand

    # O(1)
    def die(self):
        self.alive = False
        self.death_timer = 120
    
    # O(1)
    def render(self, screen):
        if not self.alive and self.death_timer <= 0:
            return
        if not self.alive:
            dead = Sprites.player_dead
            if dead:
                screen.blit(dead, (self.pixel_x, self.pixel_y))
                return
        sprite = self.get_current_sprite()
        if sprite and self.alive:
            screen.blit(sprite, (self.pixel_x, self.pixel_y))
        else:
            colour = self.colour if self.alive else (0, 0, 0)
            pygame.draw.rect(screen, colour, self.rect())
