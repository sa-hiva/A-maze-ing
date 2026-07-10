from mazegen import Maze, Cell


def cell_label(
        maze: Maze, row: int, col: int,
        path: list[Cell], solved: bool) -> str:
    """Returns the display symbol for a maze cell.

    Args:
        maze: Maze instance containing the cell.
        row: Cell row position.
        col: Cell column position.
        path: Cells belonging to the solution path.
        solved: Whether the maze has been solved.

    Returns:
        The text representation displayed for the cell."""

    if (row, col) == maze.entry:
        return "⋆S✮"
    elif (row, col) == maze.exit:
        return "✮E⋆"
    elif (maze.matrix[row][col] in path):
        if solved is True:
            return " ✧ "
        return "   "
    elif (maze.matrix[row][col].is_pattern):
        return " ♥ "
    return "   "


def top_border(maze: Maze) -> str:
    """Builds the top border line of the ASCII maze.

    Args:
        maze: Maze instance to render.

    Returns:
        A string representing the maze top border."""

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
    """Builds the content line for a maze row.

    Args:
        maze: Maze instance to render.
        row: Row index to generate.
        path: Cells belonging to the solution path.
        solved: Whether the maze has been solved.

    Returns:
        A string representing the row contents."""

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
    """Builds the bottom wall section of a maze row.

    Args:
        maze: Maze instance to render.
        row: Row index to generate.

    Returns:
        A string representing the row bottom walls."""

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
    """Adds the left bottom character for a row bottom border.

    Args:
        cell: Current maze cell.
        maze: Maze instance containing the cell.
        row: Current row index.
        parts: List collecting border characters."""

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
    """Adds the rightt bottom character for a row bottom border.

    Args:
        cell: Current maze cell.
        maze: Maze instance containing the cell.
        row: Current row index.
        parts: List collecting border characters."""

    if row == maze.height - 1:
        parts.append("╝")
        return

    if cell.is_wall_open("S"):
        parts.append("║")
    else:
        parts.append("╣")


def bottom_border(maze: Maze) -> str:
    """Builds the bottom border of the maze.

    Args:
        maze: Maze instance to render.

    Returns:
        A string representing the maze bottom border."""
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
    """Adds the correct character between 4 maze cells.

    Args:
        cell: Current maze cell.
        maze: Maze instance containing the cell.
        row: Current row index.
        col: Current column index.
        parts: List collecting border characters."""

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
    """Builds the complete ASCII representation of a maze.

    Args:
        maze: Maze instance to render.
        path: Cells belonging to the solution path.
        solved: Whether the maze has been solved.

    Returns:
        The maze rendered as a multiline string."""

    lines: list[str] = [top_border(maze)]

    for row in range(maze.height):
        lines.append(row_content(maze, row, path, solved))
        if row < maze.height - 1:
            lines.append(row_bottom(maze, row))
        else:
            lines.append(bottom_border(maze))
    return "\n".join(lines)
