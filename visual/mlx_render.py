from mazegen import Maze, Cell


def cell_label(maze: Maze, row: int, col: int, path: list[Cell]) -> str:
    if (row, col) == maze.entry:
        return " 0 "
    elif (row, col) == maze.exit:
        return " 0 "
    elif (maze.matrix[row][col] in path):
        return " · "
    return "   "


def top_border(maze: Maze) -> str:
    parts: list[str] = ["+"]

    for col in range(maze.width):
        cell = maze.matrix[0][col]
        if cell.is_wall_open("N"):
            parts.append("   +")
        else:
            parts.append("---+")

    return "".join(parts)


def row_content(maze: Maze, row: int, path: list[Cell]) -> str:
    parts: list[str] = []

    for col in range(maze.width):
        cell = maze.matrix[row][col]

        if col == 0:
            if cell.is_wall_open("W"):
                parts.append(" ")
            else:
                parts.append("|")

        parts.append(cell_label(maze, row, col, path))

        if cell.is_wall_open("E"):
            parts.append(" ")
        else:
            parts.append("|")

    return "".join(parts)


def row_bottom(maze: Maze, row: int) -> str:
    parts: list[str] = ["+"]

    for col in range(maze.width):
        cell = maze.matrix[row][col]

        if cell.is_wall_open("S"):
            parts.append("   +")
        else:
            parts.append("---+")

    return "".join(parts)


def build_ascii_maze(maze: Maze, path: list[Cell]) -> str:
    lines: list[str] = [top_border(maze)]

    for row in range(maze.height):
        lines.append(row_content(maze, row, path))
        lines.append(row_bottom(maze, row))

    return "\n".join(lines)


def show_maze(maze: Maze, path: list[Cell]) -> None:
    print()
    print(build_ascii_maze(maze, path))
    print()
