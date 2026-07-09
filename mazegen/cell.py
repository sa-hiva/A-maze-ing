WALL_MAP: dict[str, int] = {"N": 0, "E": 1, "S": 2, "W": 3}


class Cell:
    """Represents a single cell of a maze.

    A cell stores its position, wall state and generation metadata.
    Walls are encoded as a 4-bit integer where each bit represents a
    cardinal direction:
        - Bit 0: North
        - Bit 1: East
        - Bit 2: South
        - Bit 3: West

    Args:
        row: Row index of the cell in the maze grid.
        col: Column index of the cell in the maze grid.
    """

    def __init__(self, row: int, col: int) -> None:
        """Initialize a maze cell.

        Args:
            row: Row position of the cell.
            col: Column position of the cell.

        Raises:
            ValueError: If the cell position is invalid.
        """

        if not self.validate(row, col):
            raise ValueError("Invalid position for cell")

        self.row: int = row
        self.col: int = col
        self.visited: bool = False
        self.previous: Cell | None = None

        # All walls are closed by default (1111 in binary).
        self.walls: int = 0xF

        # Used to preserve the mandatory "42" pattern.
        self.is_pattern: bool = False

    @staticmethod
    def validate(row: int, col: int) -> bool:
        """Validate a cell position.

        Args:
            row: Row index to validate.
            col: Column index to validate.

        Returns:
            True if both coordinates are non-negative, otherwise False.
        """

        if row < 0 or col < 0:
            return False
        return True

    def remove_wall(self, pos: str) -> None:
        """Open a wall in the specified direction.

        Args:
            pos: Wall direction to remove. Must be one of:
                'N', 'E', 'S' or 'W'.

        Raises:
            ValueError: If the provided direction is invalid.
        """

        if pos not in WALL_MAP:
            raise ValueError("Invalid wall submitted for deletion. "
                             "Must be N, E, S or W")

        self.walls &= ~(1 << WALL_MAP[pos])

    def is_wall_open(self, pos: str) -> bool:
        """Check whether a wall is open in a given direction.

        Args:
            pos: Wall direction to check. Must be one of:
                'N', 'E', 'S' or 'W'.

        Returns:
            True if the wall is open, False if it is closed.

        Raises:
            ValueError: If the provided direction is invalid.
        """

        if pos not in WALL_MAP:
            raise ValueError("Invalid wall submitted for deletion. "
                             "Must be N, E, S or W")

        if (self.walls & (1 << WALL_MAP[pos])) == 0:
            return True
        return False
