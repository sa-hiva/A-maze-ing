from mazegen import Maze, Cell
import time


def clear_screen() -> None:
    print("\033[2J\033[H", end="")


def get_path_symbol(maze: Maze, row: int, col: int,
                    path: list[Cell]) -> str:
    cell: Cell = maze.matrix[row][col]
    i: int = path.index(cell)
    next: Cell = path[i + 1]
    row_diff = next.row - cell.row
    col_diff = next.col - cell.col
    if row_diff == -1:
        return " ↑ "
    elif row_diff == 1:
        return " ↓ "
    elif col_diff == -1:
        return " ← "
    elif col_diff == 1:
        return " → "
    return " * "


def cell_label(
        maze: Maze, row: int, col: int,
        path: list[Cell], solved: bool) -> str:
    if (row, col) == maze.entry:
        return " 0 "
    elif (row, col) == maze.exit:
        return " 0 "
    elif (maze.matrix[row][col] in path):
        if solved is True:
            # return get_path_symbol(maze, row, col, path)
            return " • "
        return "   "
    elif (maze.matrix[row][col].is_pattern):
        return "███"
    return "   "


def top_border(maze: Maze) -> str:
    parts = ["╔"]

    for col in range(maze.width):
        cell = maze.matrix[0][col]
        parts.append("═══")
        if col == maze.width - 1:
            parts.append("╗")
        elif cell.is_wall_open("E"):
            parts.append("═")
        else:
            parts.append("╦")

    return "".join(parts)


def row_content(maze: Maze, row: int, path: list[Cell], solved: bool) -> str:
    parts: list[str] = []

    for col in range(maze.width):
        cell = maze.matrix[row][col]

        if col == 0:
            if cell.is_wall_open("W"):
                parts.append(" ")
            else:
                parts.append("║")

        parts.append(cell_label(maze, row, col, path, solved))

        if cell.is_wall_open("E"):
            parts.append(" ")
        else:
            parts.append("║")

    return "".join(parts)


def row_bottom(maze: Maze, row: int) -> str:
    parts: list[str] = []

    for col in range(maze.width):
        cell = maze.matrix[row][col]
        if col == 0:
            manage_first_column_bottom(cell, maze, row, parts)
        if cell.is_wall_open("S"):
            parts.append("   ")
        else:
            parts.append("═══")

        if col == maze.width - 1:
            manage_last_column_bottom(cell, maze, row, parts)
        else:
            manage_connections_bottom(cell, maze, row, col, parts)

    return "".join(parts)


def manage_first_column_bottom(
    cell: Cell,
    maze: Maze,
    row: int,
    parts: list[str]
) -> None:
    if row == maze.height - 1:
        parts.append("╚")
        return

    if cell.is_wall_open("S"):
        parts.append("║")
    else:
        parts.append("╠")


def manage_last_column_bottom(
    cell: Cell,
    maze: Maze,
    row: int,
    parts: list[str]
) -> None:
    if row == maze.height - 1:
        parts.append("╝")
        return

    if cell.is_wall_open("S"):
        parts.append("║")
    else:
        parts.append("╣")


def bottom_border(maze: Maze) -> str:
    parts = ["╚"]

    last_row = maze.height - 1

    for col in range(maze.width):
        cell = maze.matrix[last_row][col]
        parts.append("═══")
        if col == maze.width - 1:
            parts.append("╝")
        elif cell.is_wall_open("E"):
            parts.append("═")
        else:
            parts.append("╩")

    return "".join(parts)


def manage_connections_bottom(cell: Cell,
                              maze: Maze,
                              row: int,
                              col: int,
                              parts: list[str]
                              ) -> None:
    right: Cell = maze.matrix[row][col + 1]
    bottom: Cell = maze.matrix[row + 1][col]
    current_south = not cell.is_wall_open("S")
    current_east = not cell.is_wall_open("E")
    bottom_east = not bottom.is_wall_open("E")
    right_south = not right.is_wall_open("S")

    key = (current_south, current_east, bottom_east, right_south)

    junctions = {
                # (CS, CE, BE, RS)
                (False, False, False, False): " ",
                (True,  False, False, False): "═",
                (False, True,  False, False): "║",
                (True,  True,  False, False): "╝",

                (False, False, True,  False): "║",
                (True,  False, True,  False): "╗",
                (False, True,  True,  False): "║",
                (True,  True,  True,  False): "╣",

                (False, False, False, True): "═",
                (True,  False, False, True): "═",
                (False, True,  False, True): "╚",
                (True,  True,  False, True): "╩",

                (False, False, True,  True): "╔",
                (True,  False, True,  True): "╦",
                (False, True,  True,  True): "╠",
                (True,  True,  True,  True): "╬",
                }

    parts.append(junctions[key])


def build_ascii_maze(maze: Maze, path: list[Cell], solved: bool) -> str:
    lines: list[str] = [top_border(maze)]

    for row in range(maze.height):
        lines.append(row_content(maze, row, path, solved))
        if row < maze.height - 1:
            lines.append(row_bottom(maze, row))
        else:
            lines.append(bottom_border(maze))
    return "\n".join(lines)


def show_maze(maze: Maze, path: list[Cell], solved: bool) -> None:
    print()
    print(build_ascii_maze(maze, path, solved))
    print()


def animate_generation(
    frames: list[Maze],
    path: list[Cell],
    solved: bool,
) -> None:

    print("\033[2J", end="")  # 2J = Delete screen
    print("\033[?25l", end="")  # ?25 = Cursor, l = hide

    try:
        for maze in frames:
            print("\033[H", end="")  # H = Home (go to 0,0)
            show_maze(maze, path, solved)
            time.sleep(0.02)
    finally:
        print("\033[?25h", end="")  # ?25 = Cursor, h = show


def animate_path(maze: Maze, path: list[Cell], solved: bool) -> None:
    path_frames: list[list[Cell]] = [path[:i+1] for i in range(len(path))]
    print("\033[2J", end="")  # 2J = Delete screen
    print("\033[?25l", end="")  # ?25 = Cursor, l = hide

    try:
        for path_frame in path_frames:
            print("\033[H", end="")  # H = Home (go to 0,0)
            show_maze(maze, path_frame, solved)
            time.sleep(0.05)
    finally:
        print("\033[?25h", end="")  # ?25 = Cursor, h = show
