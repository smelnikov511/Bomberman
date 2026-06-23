import pytest

from core.enemy import Enemy, EnemyState
from core.config import TileType, TILE_SIZE, COLOURS
from .conftest import FakeBomb


@pytest.fixture
def enemy():
    return Enemy(5, 5)


def test_init(enemy):
    assert enemy.colour == COLOURS['RED']
    assert enemy.state == EnemyState.WANDER


def test_is_safe_tile_empty(enemy, empty_map):
    assert enemy._is_safe_tile(3, 3, empty_map, []) is True


def test_is_safe_tile_under_bomb(enemy, empty_map):
    b = FakeBomb(3, 3)
    assert enemy._is_safe_tile(3, 3, empty_map, [b]) is False


def test_is_safe_tile_in_blast_radius(enemy, empty_map):
    from core.bomb import Bomb
    b = Bomb(3, 3, 2, enemy)
    assert enemy._is_safe_tile(3, 5, empty_map, [b]) is False
    assert enemy._is_safe_tile(3, 6, empty_map, [b]) is True


def test_soft_wall_blocks_blast(enemy, empty_map):
    from core.bomb import Bomb
    b = Bomb(3, 3, 3, enemy)
    empty_map.grid[5][3] = TileType.SOFT_WALL
    assert enemy._is_safe_tile(3, 6, empty_map, [b]) is True


def test_find_nearest_safe_tile(enemy, empty_map):
    assert enemy._find_nearest_safe_tile(empty_map, []) is not None
    tile = enemy._find_nearest_safe_tile(empty_map, [FakeBomb(enemy.col, enemy.row)])
    assert tile is not None
    assert tile != (enemy.col, enemy.row)


def test_choose_target(enemy, empty_map):
    from core.player import Player
    p = Player(5, 5)
    p.col, p.row = 5, 5
    enemy.col, enemy.row = 3, 3
    assert enemy._choose_target(empty_map, [p], [], []) == (5, 5)
