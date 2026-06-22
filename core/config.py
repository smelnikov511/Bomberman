from enum import Enum

TILE_SIZE = 64
COLS = 17
ROWS = 15
WINDOW_WIDTH = 1088
WINDOW_HEIGHT = 960

FPS = 60

PLAYER_SPEED = 3
SPEED_BOOST = 1
DEFAULT_BOMB_RANGE = 2
FIRE_BOOST = 1
DEFAULT_MAX_BOMB = 1
BOMB_BOOST = 1

BOMB_TIMER = 180  # 3 СЕКУНДЫ ПРИ 60 FPS
EXPLOSION_DURATION = 30
POWERUP_DROP_CHANCE = 0.3

class TileType(Enum):
    EMPTY = 0
    SOFT_WALL = 1
    HARD_WALL = 2

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    PAUSE = 3

class PowerUpType(Enum):
    SPEED = 0
    FIRE = 1
    BOMB = 2

COLOURS = {
    'RED': (255, 0, 0),
    'GREEN': (0, 100, 0),
    'BLUE': (0, 0, 255),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GREY': (128, 128, 128),
    'BROWN': (139, 69, 19),
    'ORANGE': (255, 165, 0),
    'YELLOW': (255, 255, 0),
    'PURPLE': (128, 0, 128)
}
