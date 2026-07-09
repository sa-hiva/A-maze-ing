from random import Random, randint
from .cell import Cell
from .maze import Maze


class MazeGenerator:
    """Generates maze structures using randomized algorithms."""

    def __init__(self, seed: int | None = None) -> None:
        """Initializes the maze generator.

        Args:
            seed: Optional seed used to make generation reproducible.
        """
        self.reset(seed)

    def reset(self, seed: int | None = None) -> None:
        """Resets the random generator with a new seed if it
        was not given by the config file.

        Args:
            seed: Optional seed for deterministic generation.
                If omitted, a random seed is generated.
        """
        self.maze_seed = seed if seed is not None else randint(0, 9999)
        self.rng = Random(self.maze_seed)

    def generate(self, width: int,
                 height: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int],
                 perfect: bool
                 ) -> tuple[Maze, list[Maze], str]:
        """Generates a new maze.

        Args:
            width: Number of cells horizontally.
            height: Number of cells vertically.
            entry: Entry coordinates of the maze.
            exit: Exit coordinates of the maze.
            perfect: Whether to generate a perfect maze without loops.

        Returns:
            A tuple containing the generated maze, animation frames,
            and a message related to the "42" pattern generation.
        """

        maze: Maze = Maze(width, height, entry, exit, perfect)
        frames: list[Maze] = []
        pattern_message: str = add_pattern(maze)
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
        return maze, frames, pattern_message


def add_pattern(maze: Maze) -> str:
    """Adds the mandatory 42 pattern to the maze.

    Args:
        maze: Maze where the pattern will be placed.

    Returns:
        An error message if the maze is too small for the pattern,
        otherwise an empty string.
    """

    if maze.height < 7 or maze.width < 9:
        return "Maze size too small: 42 pattern will be ommited"
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
    return ""


def visit(maze: Maze,
          current: Cell,
          previous: Cell | None,
          rng: Random,
          frames: list[Maze]
          ) -> None:
    """Generates maze paths using recursive backtracking.

    Args:
        maze: Maze being generated.
        current: Current cell being visited.
        previous: Previously visited cell.
        rng: Random generator used to shuffle directions.
        frames: List storing intermediate maze states.
    """

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
    additional connections.

    Args:
        maze: Maze to modify.
        frames: List storing intermediate maze states.
        rng: Random generator used to select random connections.
    """
    dead_ends = get_dead_ends(maze)

    for cell in dead_ends:
        neighbors = maze.get_closed_neighbors(cell)

        if neighbors:
            neighbor = rng.choice(neighbors)
            maze.remove_walls(cell, neighbor)
            frames.append(maze.clone())


def get_dead_ends(maze: Maze) -> list[Cell]:
    """Find all cells that are dead ends.

    Args:
        maze: Maze to analyze.

    Returns:
        List of cells with exactly one open passage.
    """
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
