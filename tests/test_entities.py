import pytest

from core.config import TileType, TILE_SIZE, Direction
from .conftest import FakeBomb


def test_wall_collision(empty_map, entity):
    entity.pixel_x = 1 * TILE_SIZE
    entity.pixel_y = 1 * TILE_SIZE
    assert entity._collides_with(0, 1 * TILE_SIZE, empty_map, []) is True


def test_no_collision_on_empty(empty_map, entity):
    entity.pixel_x = 3 * TILE_SIZE
    entity.pixel_y = 3 * TILE_SIZE
    assert entity._collides_with(4 * TILE_SIZE, 3 * TILE_SIZE, empty_map, []) is False


def test_bomb_collision(empty_map, entity):
    bomb = FakeBomb(4, 3)
    entity.pixel_x = 3 * TILE_SIZE
    entity.pixel_y = 3 * TILE_SIZE
    assert entity._collides_with(4 * TILE_SIZE, 3 * TILE_SIZE, empty_map, [bomb]) is True


def test_owner_can_leave_own_bomb(empty_map, entity):
    from core.bomb import Bomb
    bomb = Bomb(3, 3, 2, entity)
    entity.pixel_x = 3 * TILE_SIZE
    entity.pixel_y = 3 * TILE_SIZE
    assert entity._collides_with(4 * TILE_SIZE, 3 * TILE_SIZE, empty_map, [bomb]) is False
    entity.pixel_x = 4 * TILE_SIZE
    entity.pixel_y = 3 * TILE_SIZE
    assert entity._collides_with(3 * TILE_SIZE, 3 * TILE_SIZE, empty_map, [bomb]) is True


def test_boundary_collision(empty_map, entity):
    assert entity._collides_with(-1, 5 * TILE_SIZE, empty_map, []) is True


def test_move_right(empty_map, entity):
    x0 = entity.pixel_x
    entity.move(1, 0, empty_map, [])
    assert entity.pixel_x > x0


def test_move_blocked_by_wall(empty_map, entity):
    entity.pixel_x = 1 * TILE_SIZE
    entity.pixel_y = 1 * TILE_SIZE
    entity.col = 1
    entity.move(-1, 0, empty_map, [])
    assert entity.col == 1


def test_snap_to_cell(empty_map, entity):
    entity.direction = Direction.RIGHT
    entity.pixel_y = 3 * TILE_SIZE + 10
    entity.row = 3
    entity._snap_to_grid()
    assert entity.pixel_y == 3 * TILE_SIZE
