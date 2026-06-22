import pygame

from core.bomb import Bomb
from core.config import *
from core.explosion import Explosion
from core.map import Map
from core.player import Player


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def main():

    game_map = Map()
    player = Player(1, 1)
    bombs = []
    explosions = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bomb = player.place_bomb()
                    if bomb:
                        bombs.append(bomb)

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.update(game_map, bombs)
        new_explosions = []
        for bomb in bombs[:]:
            if bomb.exploded:
                continue
            result = bomb.update(game_map, [player], bombs)
            if result:
                new_explosions.append(result)
        explosions.extend(new_explosions)
        bombs = [b for b in bombs if not b.exploded]
        explosions = [e for e in explosions if not e.update()]

        screen.fill(COLOURS['GREEN'])
        game_map.render(screen)
        for bomb in bombs:
            bomb.render(screen)
        for explosion in explosions:
            explosion.render(screen)
        player.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == '__main__':
    main()
