from core.config import COLS, ROWS, TileType


def test_grid_dimensions(empty_map):
    assert empty_map.cols == COLS == 17
    assert empty_map.rows == ROWS == 15


def test_border_and_pillar_walls(empty_map):
    for row in range(ROWS):
        assert empty_map.grid[row][0] == TileType.HARD_WALL
        assert empty_map.grid[row][COLS - 1] == TileType.HARD_WALL
    for col in range(COLS):
        assert empty_map.grid[0][col] == TileType.HARD_WALL
        assert empty_map.grid[ROWS - 1][col] == TileType.HARD_WALL
    for row in range(2, ROWS - 1, 2):
        for col in range(2, COLS - 1, 2):
            assert empty_map.grid[row][col] == TileType.HARD_WALL


def test_is_within_bounds(empty_map):
    assert empty_map.is_within_bounds(0, 0) is True
    assert empty_map.is_within_bounds(16, 14) is True
    assert empty_map.is_within_bounds(-1, 0) is False
    assert empty_map.is_within_bounds(17, 0) is False


def test_destroy_soft_wall(empty_map):
    empty_map.grid[5][5] = TileType.SOFT_WALL
    assert empty_map.destroy_soft_wall(5, 5) is True
    assert empty_map.grid[5][5] == TileType.EMPTY
    assert empty_map.destroy_soft_wall(5, 5) is False


def test_safe_zone_empty(empty_map):
    assert empty_map.grid[1][1] == TileType.EMPTY
    assert empty_map.grid[13][14] == TileType.EMPTY
    assert empty_map.grid[11][1] == TileType.EMPTY
    assert empty_map.grid[1][13] == TileType.EMPTY
