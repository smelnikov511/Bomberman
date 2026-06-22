"""A* pathfinding on tile grid"""

import heapq

from .config import TileType


class AStar:

    @staticmethod
    def find_path(start, goal, game_map, bombs, max_cells=256):
        if start == goal:
            return [start]

        bomb_set = {(b.col, b.row) for b in bombs if not b.exploded}
        open_set = [(0, start)]
        came_from = {start: None}
        g_score = {start: 0}

        while open_set and len(came_from) < max_cells:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return AStar._reconstruct(came_from, current)

            for neighbor in AStar._neighbors(current, game_map, bomb_set):
                tentative = g_score[current] + 1
                if tentative < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative
                    f = tentative + AStar._manhattan(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))

        return None

    @staticmethod
    def _manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def _neighbors(node, game_map, bomb_set):
        c, r = node
        for dc, dr in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nc, nr = c + dc, r + dr
            if not game_map.is_within_bounds(nc, nr):
                continue
            if game_map.grid[nr][nc] != TileType.EMPTY:
                continue
            if (nc, nr) in bomb_set:
                continue
            yield (nc, nr)

    @staticmethod
    def _reconstruct(came_from, current):
        path = [current]
        while came_from[current] is not None:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
