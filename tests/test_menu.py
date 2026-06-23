import pygame


def test_default_config():
    from core.menu import Menu
    menu = Menu()
    assert menu.slot == 0
    assert menu.get_config() == ['player', 'player', 'ai', None]
    menu.selections = [0, 0, 0, 0]
    assert all(v is None for v in menu.get_config())


def test_navigation():
    from core.menu import Menu
    menu = Menu()
    for _ in range(3):
        menu.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))
    assert menu.slot == 3
    menu.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}))
    assert menu.slot == 2


def test_cycle_selection():
    from core.menu import Menu
    menu = Menu()
    menu.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT}))
    assert menu.selections[0] == 2
    assert menu.get_config()[0] == 'ai'


def test_space_starts():
    from core.menu import Menu
    assert Menu().handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})) == 'start'


def test_esc_quits():
    from core.menu import Menu
    assert Menu().handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})) == 'quit'


def test_other_key_returns_none():
    from core.menu import Menu
    assert Menu().handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a})) is None
