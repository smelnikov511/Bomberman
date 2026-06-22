import pygame

from core.bomb import Bomb
from core.config import *
from core.enemy import Enemy
from core.explosion import Explosion
from core.game_over import GameOver
from core.map import Map
from core.menu import Menu
from core.player import Player
from core.win import Win


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def reset_game():
    return Map(), Player(1, 1), [], [], [], [Enemy(15, 13), Enemy(1, 11), Enemy(13, 1)]

def main():

    state = GameState.MENU
    menu = Menu()
    game_over = GameOver()
    win_screen = Win()
    game_map = player = bombs = explosions = powerups = enemies = None
    death_timer = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if state == GameState.MENU and event.key == pygame.K_SPACE:
                    state = GameState.PLAYING
                    death_timer = 0
                    game_map, player, bombs, explosions, powerups, enemies = reset_game()
                elif state == GameState.MENU and event.key == pygame.K_ESCAPE:
                    running = False
                elif state == GameState.PLAYING and event.key == pygame.K_ESCAPE:
                    state = GameState.PAUSE
                elif state == GameState.PAUSE and event.key == pygame.K_ESCAPE:
                    state = GameState.PLAYING

                elif state in (GameState.GAME_OVER, GameState.WIN):
                    if event.key == pygame.K_SPACE:
                        state = GameState.PLAYING
                        death_timer = 0
                        game_map, player, bombs, explosions, powerups, enemies = reset_game()
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
                if death_timer > 0:
                    death_timer -= 1
                    if death_timer == 0:
                        state = GameState.GAME_OVER if not player.alive else GameState.WIN
                else:
                    keys = pygame.key.get_pressed()
                    player.handle_input(keys)
                    player.update(game_map, bombs, powerups)
                    for enemy in enemies:
                        enemy_bomb = enemy.update(game_map, bombs, player, powerups)
                        if enemy_bomb:
                            bombs.append(enemy_bomb)
                    new_explosions = []
                    entities = [player, *enemies]
                    for bomb in bombs[:]:
                        if bomb.exploded:
                            continue
                        result = bomb.update(game_map, entities, bombs, powerups)
                        if result:
                            new_explosions.append(result)
                    explosions.extend(new_explosions)
                    bombs = [b for b in bombs if not b.exploded]
                    explosions = [e for e in explosions if not e.update()]

                    if not player.alive or all(not e.alive for e in enemies):
                        death_timer = DEATH_DELAY

            screen.fill(COLOURS['GREEN'])
            game_map.render(screen)
            for bomb in bombs:
                bomb.render(screen)
            for explosion in explosions:
                explosion.render(screen)
            for pu in powerups:
                pu.render(screen)
            player.render(screen)
            for enemy in enemies:
                enemy.render(screen)

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
        elif state == GameState.WIN:
            win_screen.render(screen)

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == '__main__':
    main()
