import pytest

from core.pathfinding import AStar
from core.config import TileType
from .conftest import FakeBomb


def _wall_map():
    from .conftest import _empty_map
    m = _empty_map()
    for r in range(2, 9):
        m.grid[r][7] = TileType.SOFT_WALL
    return m


def test_find_path_straight(empty_map):
    path = AStar.find_path((3, 3), (8, 3), empty_map, [])
    assert path is not None
    assert path[0] == (3, 3)
    assert path[-1] == (8, 3)
    for c, r in path:
        assert empty_map.grid[r][c] == TileType.EMPTY


def test_find_path_adjacent(empty_map):
    path = AStar.find_path((3, 3), (4, 3), empty_map, [])
    assert path == [(3, 3), (4, 3)]


def test_find_path_same_cell(empty_map):
    assert AStar.find_path((5, 5), (5, 5), empty_map, []) == [(5, 5)]


def test_find_path_none_when_no_route(empty_map):
    for col in range(1, 16):
        empty_map.grid[7][col] = TileType.HARD_WALL
    assert AStar.find_path((3, 3), (3, 10), empty_map, []) is None


def test_find_path_avoids_bomb(empty_map):
    bomb = FakeBomb(5, 3)
    path = AStar.find_path((3, 3), (8, 3), empty_map, [bomb])
    assert path is not None
    for c, r in path:
        assert not (c == 5 and r == 3)


def test_find_path_around_wall():
    m = _wall_map()
    path = AStar.find_path((3, 3), (10, 3), m, [])
    assert path is not None
    assert (7, 3) not in path
