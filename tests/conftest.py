import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
import pytest

from core.config import COLS, ROWS, TileType, TILE_SIZE
from core.map import Map
from core.sprites import Sprites
from core.entities import Entity
from core.player import Player
from core.bomb import Bomb


@pytest.fixture(scope='session', autouse=True)
def pygame_init():
    pygame.init()
    _ = pygame.display.set_mode((1, 1))
    Sprites.ensure()
    yield
    pygame.quit()


class FakeBomb:
    def __init__(self, col, row, exploded=False):
        self.col = col
        self.row = row
        self.exploded = exploded
        self.owner = None
        self.owner_can_pass = False
        self.bomb_range = 2


def _empty_map():
    m = Map.__new__(Map)
    m.cols = COLS
    m.rows = ROWS
    m.grid = [
        [TileType.EMPTY for _ in range(COLS)]
        for _ in range(ROWS)
    ]
    for row in range(ROWS):
        m.grid[row][0] = TileType.HARD_WALL
        m.grid[row][COLS - 1] = TileType.HARD_WALL
    for col in range(COLS):
        m.grid[0][col] = TileType.HARD_WALL
        m.grid[ROWS - 1][col] = TileType.HARD_WALL
    for row in range(2, ROWS - 1, 2):
        for col in range(2, COLS - 1, 2):
            m.grid[row][col] = TileType.HARD_WALL
    return m


@pytest.fixture
def empty_map():
    return _empty_map()


@pytest.fixture
def entity():
    return Entity(5, 5, (255, 0, 0))


@pytest.fixture
def player():
    return Player(5, 5)


@pytest.fixture
def bomb(entity):
    return Bomb(5, 5, 2, entity)
