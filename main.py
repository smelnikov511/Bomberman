import pygame

from core.config import *
from core.map import Map
from core.player import Player


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def main():

    game_map = Map()
    player = Player(1, 1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        screen.fill(COLOURS['GREEN'])
        bombs = []
        player.update(game_map, bombs)
        game_map.render(screen)
        player.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == '__main__':
    main()
