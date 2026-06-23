import os
import pygame

from .config import PowerUpType, TILE_SIZE

SPRITE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites")


class Sprites:
    _loaded = False
    PLAYER_COLOURS = ['blue', 'orange', 'red', 'pink']
    DIRS = ['down', 'left', 'right', 'up']

    @classmethod
    def ensure(cls):
        if cls._loaded:
            return
        cls.hard_wall = cls._load("hard_wall.png")
        cls.soft_wall = cls._load("soft_wall.png")
        cls.empty_wall = cls._load("empty_wall.png")
        cls.bomb = cls._load("bomb.png")
        cls.explosion = cls._load("explosion.png")
        cls.player_dead = cls._load("player_dead.png")
        cls.powerup = {
            PowerUpType.SPEED: cls._load("powerup_speed.png"),
            PowerUpType.FIRE: cls._load("powerup_fire.png"),
            PowerUpType.BOMB: cls._load("powerup_bomb.png"),
        }

        cls.player_stand = [cls._load(f"player_{c}_stand.png") for c in cls.PLAYER_COLOURS]
        cls.player_walk = []
        for c in cls.PLAYER_COLOURS:
            dir_frames = []
            for d in cls.DIRS:
                dir_frames.append([cls._load(f"player_{c}_{d}1.png"), cls._load(f"player_{c}_{d}2.png")])
            cls.player_walk.append(dir_frames)
        cls._loaded = True

    @classmethod
    def _load(cls, path):
        full = os.path.join(SPRITE_DIR, path)
        if os.path.exists(full):
            img = pygame.image.load(full).convert_alpha()
            if img.get_width() != TILE_SIZE:
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            return img
        return None
