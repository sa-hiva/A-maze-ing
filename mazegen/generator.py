from random import Random
from .cell import Cell
from .maze import Maze


class MazeGenerator():
    def __init__(self, seed: int | None = None) -> None:
        self.rng: Random = Random(seed) if seed else Random()

    def generate(self, width: int,
                 height: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int]
                 ) -> None:
        maze: Maze = Maze(width, height, entry, exit)
        add_pattern(maze)
        row = self.rng.randrange(height)
        col = self.rng.randrange(width)
        first = maze.matrix[row][col]
        while first.is_pattern:
            row = self.rng.randrange(height)
            col = self.rng.randrange(width)
            first = maze.matrix[row][col]
        visit(maze, first, None, self.rng)
        maze.clear_visited()
        return maze


def add_pattern(maze: Maze) -> None:
    if maze.height < 7 or maze.width < 9:
        print("Maze size too small: 42 pattern will be ommited")
        return
    row: int = maze.height // 2 + maze.height % 2 - 3
    col: int = maze.width // 2 + maze.height % 2 - 4
    pattern = ("  # ###",
               " #    #",
               "###  # ",
               "  # #  ",
               "  # ###")
    for i in range(5):
        for j in range(7):
            cell: Cell = maze.matrix[row + i][col + j]
            cell.is_pattern = pattern[i][j] == "#"
            if cell.is_pattern:
                cell.visited = True


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
