import pygame

from .config import TileType, COLOURS
from .sprites import Sprites


# O(1)
def render_tile(screen, tile_type, x, y, tile_size):
    Sprites.ensure()
    if tile_type == TileType.HARD_WALL:
        spr = Sprites.hard_wall
    elif tile_type == TileType.SOFT_WALL:
        spr = Sprites.soft_wall
    elif tile_type == TileType.EMPTY:
        spr = Sprites.empty_wall
    else:
        return
    if spr:
        screen.blit(spr, (x, y))
    elif tile_type != TileType.EMPTY:
        colour = COLOURS['GREY'] if tile_type == TileType.HARD_WALL else COLOURS['BROWN']
        pygame.draw.rect(screen, colour, (x, y, tile_size, tile_size))
