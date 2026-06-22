import random
import pygame

from .config import TILE_SIZE, COLS, ROWS, WINDOW_HEIGHT, WINDOW_WIDTH, TileType
from .blocks import render_tile


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
        for row in range(self.rows):
            for col in range(self.cols):
                if row == 0 or row == self.rows - 1 or col == 0 or col == self.cols - 1:
                    self.grid[row][col] = TileType.HARD_WALL
                elif row % 2 == 0 and col % 2 == 0:
                    self.grid[row][col] = TileType.HARD_WALL

        box_density = 0.5
        for row in range(1, self.rows - 1):
            for col in range(1, self.cols - 1):
                if (
                    self.grid[row][col] == TileType.EMPTY
                    and
                    (row, col) != (1, 1) and (row, col) != (13, 15)
                ):
                    if random.random() < box_density:
                        self.grid[row][col] = TileType.SOFT_WALL

    def destroy_soft_wall(self, col, row):
        if self.grid[row][col] == TileType.SOFT_WALL:
            self.grid[row][col] = TileType.EMPTY
            return True
        return False
    
    def is_within_bounds(self, col, row):
        return 0 <= col < self.cols and 0 <= row < self.rows

    def render(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.grid[row][col]
                if tile != TileType.EMPTY:
                    px = col * tile_size
                    py = row * tile_size
                    render_tile(screen, tile, px, py, tile_size)


