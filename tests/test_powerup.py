import pytest

from core.powerup import PowerUp
from core.config import PowerUpType, SPEED_BOOST, FIRE_BOOST, BOMB_BOOST


def test_try_spawn_returns_none_or_powerup():
    pu = PowerUp.try_spawn(5, 5)
    assert pu is None or isinstance(pu, PowerUp)


def test_speed_applies(entity, empty_map):
    old = entity.speed
    PowerUp(5, 5, PowerUpType.SPEED).apply(entity)
    assert entity.speed == old + SPEED_BOOST


def test_all_boost_types(entity, empty_map):
    PowerUp(5, 5, PowerUpType.FIRE).apply(entity)
    assert entity.bomb_range > 2
    PowerUp(5, 5, PowerUpType.BOMB).apply(entity)
    assert entity.max_bombs > 1
