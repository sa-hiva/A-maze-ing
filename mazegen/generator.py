from collections import deque
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


def solve_maze(maze: Maze) -> str:
    first: Cell = maze.matrix[maze.entry[0]][maze.entry[1]]
    explored_queue: deque[Cell] = deque()
    explored_queue.append(first)

    while len(explored_queue) > 0:
        current = explored_queue.popleft()
        current.visited = True
        if maze.is_exit(current):
            break
        neighbors: list[Cell] = maze.get_unvisited_open_neighbors(current)
        for neighbor in neighbors:
            neighbor.previous = current
            explored_queue.append(neighbor)
    if not maze.is_exit(current):
        raise ValueError("ERROR: Exit unreachable")
    cell_path: list[Cell] = []
    while current.previous is not None:
        cell_path.append(current)
        current = current.previous
    cell_path.append(current)
    cell_path.reverse()
    return get_directions_from_path(cell_path)


def get_directions_from_path(cell_path: list[Cell]) -> str:
    path: str = ""
    for i in range(len(cell_path) - 1):
        path += get_movement(cell_path[i], cell_path[i + 1])
    return path


def get_movement(old: Cell, new: Cell) -> str:
    row_diff = new.row - old.row
    col_diff = new.col - old.col
    if abs(row_diff) + abs(col_diff) != 1:
        raise ValueError("Cells are not adjacent")
    if row_diff == -1:
        return "N"
    elif row_diff == 1:
        return "S"
    elif col_diff == -1:
        return "W"
    elif col_diff == 1:
        return "E"
