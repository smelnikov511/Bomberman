import pygame

from core.bomb import Bomb
from core.config import *
from core.explosion import Explosion
from core.game_over import GameOver
from core.map import Map
from core.menu import Menu
from core.player import Player


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def reset_game():
    return Map(), Player(1, 1), [], []

def main():

    state = GameState.MENU
    menu = Menu()
    game_over = GameOver()
    game_map = player = bombs = explosions = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if state == GameState.MENU and event.key == pygame.K_SPACE:
                    state = GameState.PLAYING
                    game_map, player, bombs, explosions = reset_game()
                elif state == GameState.MENU and event.key == pygame.K_ESCAPE:
                    running = False
                elif state == GameState.PLAYING and event.key == pygame.K_ESCAPE:
                    state = GameState.PAUSE
                elif state == GameState.PAUSE and event.key == pygame.K_ESCAPE:
                    state = GameState.PLAYING

                elif state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        state = GameState.PLAYING
                        game_map, player, bombs, explosions = reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        state = GameState.MENU
                
                elif state == GameState.PLAYING and event.key == pygame.K_SPACE:
                    bomb = player.place_bomb()
                    if bomb:
                        bombs.append(bomb)

        if state == GameState.MENU:
            menu.render(screen)

        elif state == GameState.PLAYING or state == GameState.PAUSE:
            if state == GameState.PLAYING:
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

                if not player.alive:
                    state = GameState.GAME_OVER

            screen.fill(COLOURS['GREEN'])
            game_map.render(screen)
            for bomb in bombs:
                bomb.render(screen)
            for explosion in explosions:
                explosion.render(screen)
            player.render(screen)

            if state == GameState.PAUSE:
                s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                s.set_alpha(128)
                s.fill((0, 0, 0))
                screen.blit(s, (0, 0))
                font = pygame.font.Font(None, 72)
                text = font.render("PAUSED", True, COLOURS['WHITE'])
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                screen.blit(text, text_rect)

        elif state == GameState.GAME_OVER:
            game_over.render(screen)

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == '__main__':
    main()
