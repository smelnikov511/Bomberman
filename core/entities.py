"""Player, Enemy — общие предки Entity"""

import pygame

from .config import Direction, TileType, TILE_SIZE, PLAYER_SPEED, DEFAULT_BOMB_RANGE, DEFAULT_MAX_BOMB
from .map import Map

class Entity():

    def __init__(self, col, row, colour):
        self.col = col
        self.row = row
        self.pixel_x = col * TILE_SIZE
        self.pixel_y = row * TILE_SIZE
        self.direction = Direction.NONE
        self.speed = PLAYER_SPEED
        self.bomb_range = DEFAULT_BOMB_RANGE
        self.max_bomb = DEFAULT_MAX_BOMB
        self.active_bomb = 0
        self.alive = True
        self.colour = colour
        self.margin = 4

    def rect(self):
        """Возвращает хитбокс (pygame.Rect) с учётом отступа."""
        return pygame.Rect(
            self.pixel_x + self.margin,
            self.pixel_y + self.margin,
            TILE_SIZE - 2 * self.margin,
            TILE_SIZE - 2 * self.margin
        )
    
    def _collides_with(self, x, y, game_map, obstacles):
        test_rect = pygame.Rect(
            x + self.margin, y + self.margin,
            TILE_SIZE - self.margin * 2,
            TILE_SIZE - self.margin * 2,
        )  # Это то, куда персонаж хочет пройти

        # Коллизия со стенами
        for row in range(game_map.rows):
            for col in range(game_map.cols):
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
            if test_rect.colliderect(bomb_rect):
                return True
            
        # Границы карты
        if (x < 0 or x + TILE_SIZE > game_map.cols * TILE_SIZE
            or 
            y < 0 or y + TILE_SIZE > game_map.rows * TILE_SIZE):
            return True
            
        return False


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
    
    def _snap_to_grid(self):
        if self.direction in (Direction.UP, Direction.DOWN):
            self.pixel_x = self.col * TILE_SIZE
        elif self.direction in (Direction.LEFT, Direction.RIGHT):
            self.pixel_y = self.row * TILE_SIZE

    def die(self):
        self.alive = False
    
    def render(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect())
