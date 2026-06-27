from random import Random
from cell import Cell, wall_map

class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.matrix: list[list[Cell]] = []
        self.cells: list[Cell] = []
    
    def get_hex_maze(self) -> list[list[int]]:
        return [
            [cell.walls for cell in row]
            for row in self.matrix
            ]
    
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
        if col < self.width -1 and not self.matrix[row][col + 1].visited:
            neighbors.append(self.matrix[row][col + 1])
        
        return neighbors