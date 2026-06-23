import pygame

from core.bomb import Bomb
from core.config import *
from core.enemy import Enemy
from core.explosion import Explosion
from core.game_over import GameOver
from core.map import Map
from core.menu import Menu
from core.player import Player
from core.sprites import Sprites
from core.win import Win


pygame.init()
display_info = pygame.display.Info()
scale = min(display_info.current_w / WINDOW_WIDTH,
            display_info.current_h / WINDOW_HEIGHT)
win_w = int(WINDOW_WIDTH * scale)
win_h = int(WINDOW_HEIGHT * scale)
screen = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
render_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

SPAWNS = [(1, 1), (15, 13), (1, 11), (13, 1)]
PLAYER_COLOURS = [COLOURS['BLUE'], COLOURS['ORANGE'], COLOURS['RED'], COLOURS['PINK']]
PLAYER_KEYS = [
    (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_g),
    (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE),
    (pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_h),
    (pygame.K_KP8, pygame.K_KP5, pygame.K_KP4, pygame.K_KP6, pygame.K_KP0),
]


def reset_game(config):
    Sprites.ensure()
    players = []
    enemies = []
    for i, choice in enumerate(config):
        if choice is None:
            continue
        col, row = SPAWNS[i]
        if choice == 'ai':
            e = Enemy(col, row)
            e.sprite_index = i
            enemies.append(e)
        elif choice == 'player':
            colour = PLAYER_COLOURS[i]
            up, down, left, right, bomb = PLAYER_KEYS[i]
            p = Player(col, row, colour, up, down, left, right, bomb)
            p.sprite_index = i
            p.player_name = f"Player {i + 1}"
            players.append(p)
    return Map(), players, enemies, [], [], []


def main():
    global screen

    state = GameState.MENU
    menu = Menu()
    game_over = GameOver()
    win_screen = Win()
    game_map = players = enemies = bombs = explosions = powerups = None
    death_timer = 0
    winner_text = "ПОБЕДА!"
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if state == GameState.MENU:
                    action = menu.handle_event(event)
                    if action == 'start':
                        state = GameState.PLAYING
                        death_timer = 0
                        game_map, players, enemies, bombs, explosions, powerups = reset_game(menu.get_config())
                    elif action == 'quit':
                        running = False

                elif state == GameState.PLAYING and event.key == pygame.K_ESCAPE:
                    state = GameState.PAUSE
                elif state == GameState.PAUSE and event.key == pygame.K_ESCAPE:
                    state = GameState.PLAYING

                elif state in (GameState.GAME_OVER, GameState.WIN):
                    if event.key == pygame.K_SPACE:
                        state = GameState.PLAYING
                        death_timer = 0
                        game_map, players, enemies, bombs, explosions, powerups = reset_game(menu.get_config())
                    elif event.key == pygame.K_ESCAPE:
                        state = GameState.MENU

                elif state == GameState.PLAYING:
                    for p in players:
                        if p.alive and event.key == p.bomb_key:
                            bomb = p.place_bomb()
                            if bomb:
                                bombs.append(bomb)

        if state == GameState.MENU:
            menu.render(render_surface)

        elif state in (GameState.PLAYING, GameState.PAUSE):
            if state == GameState.PLAYING:
                if death_timer > 0:
                    death_timer -= 1
                    if death_timer == 0:
                        alive_players = [p for p in players if p.alive]
                        if alive_players:
                            state = GameState.WIN
                            winner_text = f"{alive_players[0].player_name} win!" if alive_players[0].player_name else "ПОБЕДА!"
                        else:
                            state = GameState.GAME_OVER
                else:
                    keys = pygame.key.get_pressed()
                    for p in players:
                        if p.alive:
                            p.handle_input(keys)
                            p.update(game_map, bombs, powerups)
                        elif p.death_timer > 0:
                            p.death_timer -= 1
                    for e in enemies:
                        if not e.alive:
                            if e.death_timer > 0:
                                e.death_timer -= 1
                            continue
                        enemy_bomb = e.update(game_map, bombs, players, enemies, powerups)
                        if enemy_bomb:
                            bombs.append(enemy_bomb)
                    new_explosions = []
                    entities = [*players, *enemies]
                    for bomb in bombs[:]:
                        if bomb.exploded:
                            continue
                        result = bomb.update(game_map, entities, bombs, powerups)
                        if result:
                            new_explosions.append(result)
                    explosions.extend(new_explosions)
                    bombs = [b for b in bombs if not b.exploded]
                    explosions = [e for e in explosions if not e.update()]

                    alive = [e for e in [*players, *enemies] if e.alive]
                    if len(alive) <= 1:
                        death_timer = DEATH_DELAY

            render_surface.fill(COLOURS['GREEN'])
            game_map.render(render_surface)
            for bomb in bombs:
                bomb.render(render_surface)
            for explosion in explosions:
                explosion.render(render_surface)
            for pu in powerups:
                pu.render(render_surface)
            for p in players:
                p.render(render_surface)
            for e in enemies:
                e.render(render_surface)

            if state == GameState.PAUSE:
                s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                s.set_alpha(128)
                s.fill((0, 0, 0))
                render_surface.blit(s, (0, 0))
                font = pygame.font.Font(None, 72)
                text = font.render("PAUSED", True, COLOURS['WHITE'])
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                render_surface.blit(text, text_rect)

        elif state == GameState.GAME_OVER:
            game_over.render(render_surface)
        elif state == GameState.WIN:
            win_screen.render(render_surface, winner_text)

        screen.fill((0, 0, 0))
        sw, sh = screen.get_size()
        scale = min(sw / WINDOW_WIDTH, sh / WINDOW_HEIGHT)
        scaled_w = int(WINDOW_WIDTH * scale)
        scaled_h = int(WINDOW_HEIGHT * scale)
        screen.blit(pygame.transform.scale(render_surface, (scaled_w, scaled_h)),
                    ((sw - scaled_w) // 2, (sh - scaled_h) // 2))
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == '__main__':
    main()
