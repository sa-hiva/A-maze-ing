from .cell import Cell


class Maze:
    def __init__(self, width: int,
                 height: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int]
                 ) -> None:

        self.width = width
        self.height = height
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.matrix: list[list[Cell]] = [[None for _ in range(self.width)]
                                         for _ in range(self.height)]
        self.solution: str
        self.validate_input()
        self.init_maze()

    def get_maze_as_str(self) -> str:
        str_maze: str = ""
        for row in self.matrix:
            for cell in row:
                str_maze += f"{cell.walls:X}"
            str_maze += "\n"
        return str_maze

    def validate_input(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Maze dimensions must be positive")
        if not self.is_in_matrix(self.entry):
            raise ValueError("Entry is outside maze bounds")
        if not self.is_in_matrix(self.exit):
            raise ValueError("Exit is outside maze bounds")
        if self.entry == self.exit:
            raise ValueError("Entry and Exit must be different")

    def clear_visited(self) -> None:
        for row in range(self.height):
            for col in range(self.width):
                self.matrix[row][col].visited = False
                self.matrix[row][col].previous = None

    def get_cell(self, row: int, col: int) -> Cell:
        return self.matrix[row][col]

    def is_in_matrix(self, pos: tuple[int, int]) -> bool:
        row, col = pos
        return 0 <= row < self.height and 0 <= col < self.width

    def is_exit(self, cell: Cell) -> bool:
        return (cell.row, cell.col) == self.exit

    @staticmethod
    def remove_walls(new: Cell, old: Cell) -> None:
        row_diff = new.row - old.row
        col_diff = new.col - old.col
        if abs(row_diff) + abs(col_diff) != 1:
            raise ValueError("Cells are not adjacent")
        if row_diff == -1:
            old.remove_wall('N')
            new.remove_wall('S')
        elif row_diff == 1:
            old.remove_wall('S')
            new.remove_wall('N')
        elif col_diff == -1:
            old.remove_wall('W')
            new.remove_wall('E')
        elif col_diff == 1:
            old.remove_wall('E')
            new.remove_wall('W')

    @staticmethod
    def is_way_open(new: Cell, old: Cell) -> bool:
        row_diff = new.row - old.row
        col_diff = new.col - old.col
        if abs(row_diff) + abs(col_diff) != 1:
            raise ValueError("Cells are not adjacent")
        if row_diff == -1:
            return (old.is_wall_open('N') and new.is_wall_open('S'))
        elif row_diff == 1:
            return (old.is_wall_open('S') and new.is_wall_open('N'))
        elif col_diff == -1:
            return (old.is_wall_open('W') and new.is_wall_open('E'))
        elif col_diff == 1:
            return (old.is_wall_open('E') and new.is_wall_open('W'))
        return False

    def get_unvisited_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors: list[Cell] = []
        row = cell.row
        col = cell.col
        if row > 0 and not self.matrix[row - 1][col].visited:
            neighbors.append(self.matrix[row - 1][col])
        if row < self.height - 1 and not self.matrix[row + 1][col].visited:
            neighbors.append(self.matrix[row + 1][col])
        if col > 0 and not self.matrix[row][col - 1].visited:
            neighbors.append(self.matrix[row][col - 1])
        if col < self.width - 1 and not self.matrix[row][col + 1].visited:
            neighbors.append(self.matrix[row][col + 1])
        return neighbors

    def get_unvisited_open_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors: list[Cell] = self.get_unvisited_neighbors(cell)
        valid_neighbors: list[Cell] = []
        for neighbor in neighbors:
            if self.is_way_open(neighbor, cell):
                valid_neighbors.append(neighbor)
        return valid_neighbors
