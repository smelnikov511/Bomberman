import pygame

from .config import TileType, COLOURS


def render_tile(screen, tile_type, x, y, tile_size):
    rect = (x, y, tile_size, tile_size)
    if tile_type == TileType.HARD_WALL:
        pygame.draw.rect(screen, COLOURS['GREY'], pygame.Rect(rect))
    elif tile_type == TileType.SOFT_WALL:
        pygame.draw.rect(screen, COLOURS['BROWN'], pygame.Rect(rect))