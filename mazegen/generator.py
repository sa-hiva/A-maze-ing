from random import Random
from .cell import Cell
from .maze import Maze


class MazeGenerator:
    def __init__(self, seed: int | None = None) -> None:
        self.seed = seed
        self.rng: Random = Random(seed) if seed is not None else Random()

    def reset(self) -> None:
        self.rng = Random(self.seed) if self.seed is not None else Random()

    def generate(self, width: int,
                 height: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int],
                 perfect: bool
                 ) -> tuple[Maze, list[Maze]]:
        maze: Maze = Maze(width, height, entry, exit, perfect)
        frames: list[Maze] = []
        add_pattern(maze)
        row = self.rng.randrange(height)
        col = self.rng.randrange(width)
        first = maze.matrix[row][col]
        while first.is_pattern:
            row = self.rng.randrange(height)
            col = self.rng.randrange(width)
            first = maze.matrix[row][col]
        visit(maze, first, None, self.rng, frames)
        if not perfect:
            pacmanify(maze, frames, self.rng)
        maze.clear_visited()
        return maze, frames


def add_pattern(maze: Maze) -> None:
    if maze.height < 7 or maze.width < 9:
        print("Maze size too small: 42 pattern will be ommited")
        return
    row: int = maze.height // 2 + maze.height % 2 - 3
    col: int = maze.width // 2 - 3
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


def visit(maze: Maze,
          current: Cell,
          previous: Cell | None,
          rng: Random,
          frames: list[Maze]
          ) -> None:
    if current.visited:
        return
    current.visited = True
    current.previous = previous
    if previous is not None:
        maze.remove_walls(current, previous)
        frames.append(maze.clone())
    neighbors = maze.get_unvisited_neighbors(current)
    rng.shuffle(neighbors)
    for neighbor in neighbors:
        visit(maze, neighbor, current, rng, frames)


def pacmanify(maze: Maze, frames: list[Maze], rng: Random) -> None:
    """Convert a perfect maze into a Pac-Man-like maze by opening
    additional random connections.
    """
    dead_ends = get_dead_ends(maze)

    for cell in dead_ends:
        neighbors = maze.get_closed_neighbors(cell)

        if neighbors:
            neighbor = rng.choice(neighbors)
            maze.remove_walls(cell, neighbor)
            frames.append(maze.clone())


def get_dead_ends(maze: Maze) -> list[Cell]:
    dead_ends = []

    for row in maze.matrix:
        for cell in row:
            if cell.is_pattern:
                continue

            exits = 0

            for direction in "NESW":
                if cell.is_wall_open(direction):
                    exits += 1

            if exits == 1:
                dead_ends.append(cell)

    return dead_ends
