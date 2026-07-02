
wall_map: dict[str, int] = {"N": 0, "E": 1, "S": 2, "W": 3}


class Cell:
    def __init__(self, row: int, col: int) -> None:
        if not self.validate(row, col):
            raise ValueError("Invalid position for cell")
        self.row: int = row
        self.col: int = col
        self.visited: bool = False
        self.previous: Cell | None = None
        self.walls: int = 0xF

    @staticmethod
    def validate(row: int, col: int) -> bool:
        if row < 0 or col < 0:
            return False
        return True

    def remove_wall(self, pos: str) -> None:
        if pos not in wall_map:
            raise ValueError("Invalid wall submitted for deletion."
                             " Must be N, E, S or W")
        self.walls &= ~(1 << wall_map[pos])

    def is_wall_open(self, pos: str) -> bool:
        if pos not in wall_map:
            raise ValueError("Invalid wall submitted for deletion."
                             " Must be N, E, S or W")
        if (self.walls & (1 << wall_map[pos])) == 0:
            return True
        return False
