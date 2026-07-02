from random import Random
from .cell import Cell
from .maze import Maze

__all__ = ["wall_map"]


def visit(maze: Maze, current: Cell, previous: Cell, rng: Random) -> None:
    if current.visited:
        return
    current.visited = True
    current.previous = previous
    if previous is not None:
        maze.remove_walls(current, previous)
    neighbors = maze.get_unvisited_neighbors(current)
    rng.shuffle(neighbors)
    for neighbor in neighbors:
        visit(maze, neighbor, current, rng)
