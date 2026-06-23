import pygame

from core.config import Direction, TILE_SIZE, COLOURS


class _KeyState:
    def __init__(self):
        self._keys = {}
    def __setitem__(self, key, value):
        self._keys[key] = value
    def __getitem__(self, key):
        return self._keys.get(key, False)


def _make_keys():
    return _KeyState()


def test_default_keys(player):
    assert player.up_key == pygame.K_UP
    assert player.bomb_key == pygame.K_SPACE


def test_colour_default(player):
    assert player.colour == COLOURS['BLUE']


def test_handle_input_direction(player, empty_map):
    keys = _make_keys()
    keys[pygame.K_UP] = True
    player.handle_input(keys)
    assert player.direction == Direction.UP
    keys[pygame.K_UP] = False
    player.handle_input(keys)
    assert player.direction == Direction.NONE


def test_custom_key_bindings():
    from core.player import Player
    p = Player(5, 5, COLOURS['ORANGE'],
               up=pygame.K_w, bomb_key=pygame.K_g)
    keys = _make_keys()
    keys[pygame.K_w] = True
    p.handle_input(keys)
    assert p.direction == Direction.UP


def test_place_bomb(player, empty_map):
    b = player.place_bomb()
    assert b is not None
    assert b.row == player.row
    assert b.owner is player


def test_place_bomb_at_max(player, empty_map):
    player.max_bombs = 1
    player.place_bomb()
    assert player.place_bomb() is None


def test_update_moves(player, empty_map):
    x0 = player.pixel_x
    player.direction = Direction.RIGHT
    player.update(empty_map, [], [])
    assert player.pixel_x > x0


def test_update_dead(player, empty_map):
    player.die()
    x0 = player.pixel_x
    player.update(empty_map, [], [])
    assert player.pixel_x == x0
