import pytest

from core.bomb import Bomb
from core.config import TileType, BOMB_TIMER, TILE_SIZE
from .conftest import FakeBomb


def test_init(empty_map, player):
    b = Bomb(3, 5, 2, player)
    assert b.row == 3 and b.col == 5
    assert b.bomb_range == 2
    assert b.owner is player
    assert b.timer == BOMB_TIMER
    assert not b.exploded
    assert b.owner_can_pass


def test_explodes_when_timer_expires(empty_map, player):
    b = Bomb(3, 5, 2, player)
    b.timer = 1
    result = b.update(empty_map, [player], [b], [])
    assert b.exploded
    assert result is not None


def test_explosion_blocked_by_hard_wall(empty_map, player):
    b = Bomb(5, 5, 3, player)
    empty_map.grid[5][8] = TileType.HARD_WALL
    explosion = b.explode(empty_map, [player], [b], [])
    assert (8, 5) not in explosion.segments


def test_explosion_stops_at_soft_wall(empty_map, player):
    b = Bomb(5, 5, 3, player)
    empty_map.grid[5][7] = TileType.SOFT_WALL
    explosion = b.explode(empty_map, [player], [b], [])
    assert (7, 5) in explosion.segments
    assert (8, 5) not in explosion.segments


def test_explosion_kills_entity(empty_map, player, entity):
    b = Bomb(5, 5, 2, player)
    entity.pixel_x = 5 * TILE_SIZE
    entity.pixel_y = 5 * TILE_SIZE
    b.explode(empty_map, [player, entity], [b], [])
    assert not entity.alive


def test_chain_reaction(empty_map, player):
    b1 = Bomb(5, 5, 2, player)
    b2 = Bomb(7, 5, 2, player)
    b1.explode(empty_map, [player], [b1, b2], [])
    assert b2.exploded
