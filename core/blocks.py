import pygame

from .config import TileType, COLOURS

def render(screen, tile_type, x, y, tile_size, colours):
    rect = (x, y, tile_size, tile_size)
    if tile_type == TileType.HARD_WALL:
        pygame.draw.rect(screen, COLOURS['RED'], pygame.Rect(rect))
    elif tile_type == TileType.SOFT_WALL:
        pygame.draw.rect(screen, COLOURS['BLUE'], pygame.Rect(rect))