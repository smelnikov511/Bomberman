import random
import pygame

from .config import TILE_SIZE, COLS, ROWS, WINDOW_HEIGHT, WINDOW_WIDTH, TileType
from .blocks import render_tile

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
tile_size = TILE_SIZE

class Map():

    def __init__(self):
        self.cols = COLS
        self.rows = ROWS
        self.grid = [
            [TileType.EMPTY for _ in range(self.cols)]
            for _ in range(self.rows)
        ]
        self.generate_layout()

    def generate_layout(self):
        for x in range(self.rows):
            for y in range(self.cols):
                if x == 0 or x == self.rows - 1 or y == 0 or y == self.cols - 1:
                    self.grid[x][y] = TileType.HARD_WALL
                elif x % 2 == 0  and y % 2 == 0:
                    self.grid[x][y] = TileType.HARD_WALL

        box_density = 0.65
        for x in range(1, self.rows - 1):
            for y in range(1, self.cols - 1):
                if (
                    self.grid[x][y] == TileType.EMPTY
                    and
                    (x, y) != (1, 1) and (x, y) != (15, 13)
                ):
                    if random.random() < box_density:
                        self.grid[x][y] = TileType.SOFT_WALL

    def destroy_soft_wall(self, col, row):
        if self.grid[row][col] == TileType.SOFT_WALL:
            self.grid[row][col] = TileType.EMPTY
            return True
        return False
    
    def render(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.grid[row][col]
                if tile != TileType.EMPTY:
                    px = col * tile_size
                    py = row * tile_size
                    render_tile(screen, tile, px, py, tile_size)


