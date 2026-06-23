import random
import pygame

from .config import TILE_SIZE, COLOURS, POWERUP_DROP_CHANCE, SPEED_BOOST, FIRE_BOOST, BOMB_BOOST, PowerUpType
from .sprites import Sprites


POWERUP_COLOURS = {
    PowerUpType.SPEED: COLOURS['GREEN'],
    PowerUpType.FIRE:  COLOURS['RED'],
    PowerUpType.BOMB:  COLOURS['BLUE'],
}


class PowerUp:

    def __init__(self, col, row, ptype):
        self.col = col
        self.row = row
        self.ptype = ptype
        self.pixel_x = col * TILE_SIZE
        self.pixel_y = row * TILE_SIZE

    @classmethod
    def try_spawn(cls, col, row):
        if random.random() < POWERUP_DROP_CHANCE:
            ptype = random.choice(list(PowerUpType))
            return cls(col, row, ptype)
        return None

    def apply(self, player):
        if self.ptype == PowerUpType.SPEED:
            player.speed += SPEED_BOOST
        elif self.ptype == PowerUpType.FIRE:
            player.bomb_range += FIRE_BOOST
        elif self.ptype == PowerUpType.BOMB:
            player.max_bombs += BOMB_BOOST

    def rect(self):
        return pygame.Rect(self.pixel_x, self.pixel_y, TILE_SIZE, TILE_SIZE)

    def render(self, screen):
        Sprites.ensure()
        spr = Sprites.powerup[self.ptype]
        if spr:
            screen.blit(spr, (self.pixel_x, self.pixel_y))
        else:
            colour = POWERUP_COLOURS[self.ptype]
            rect = self.rect()
            pygame.draw.rect(screen, colour, rect)
            pygame.draw.rect(screen, COLOURS['WHITE'], rect.inflate(-24, -24))
