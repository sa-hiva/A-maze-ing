from random import Random
from .cell import Cell, wall_map
from .maze import Maze


def visit(maze: Maze, current: Cell, previous: Cell, rng: Random):
    if current.visited:
        return
    current.visited = True
    current.previous = previous
    if previous is not None:
        maze.remove_walls(current, previous)
    neighbors = maze.get_unvisited_neighbors(current)
    rng.shuffle(neighbors)
    for neighbor in neighbors:
        visit(maze,neighbor, current, rng)