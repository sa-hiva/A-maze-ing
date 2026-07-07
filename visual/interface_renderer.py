import curses
from mazegen import Maze, Cell
from .maze_renderer import build_ascii_maze
from .colors import get_wall_color_pair, is_wall_char


BYE_MESSAGE = [
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡞⠋⠉⠳⡄⠀⠀⠀⠀⢠⠴⠒⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀                                 ",
    "⠀⠀⢀⡶⢶⡀⠀⠀⠀⠀⠀⠀⠀⢠⠏⠀⠀⠀⠀⢹⡄⠀⠀⣰⠋⠀⠀⠀⠸⣆⠀⠀⠀⠀⠀⠀⠀⠀                                ",
    "⠀⣀⡼⠀⠀⠛⠒⠒⡦⠀⠀⠀⠀⡟⠀⠀⠀⠀⠀⠀⣷⠀⢰⡏⠀⠀⠀⠀⠀⣹⠀⠀⠀⠀⠀⠀⠀⠀                                ",
    "⣏⠁⠀⠀⠀⠀⠀⣼⠁⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⣹⠀⢸⠀⠀⠀⠀⠀⠀⢸⠁⠀⠀⠀⠀⠀⠀⠀                                 ",
    "⠀⠉⡶⠀⠀⠀⠀⠈⡆⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⢽⠀⢸⠀⠀⠀⠀⠀⠀⣽⠀⠀⠀⠀⠀⠀                                    ",
    "⠀⠀⢷⡤⠞⠉⠉⠉⠁⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⢸⡆⢸⠀⠀⠀⠀⠀⢀⡏⠀⠀⠀⠀                                     ",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣆⠀⠀⠀⠀⠀⠈⠛⠋⠀⠀⠀⠀⠀⣸⠃⠀⠀⠀⠀⠀⠀⠀⠀                                  ",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠳⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀                                  ",
    "           ⢠⡞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡠⠤⠤⠤⠤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣦⠀⠀⠀⠀⠀⠀⢀⠴⠋⢡⣦⣤⣀⠀⠀⠀⠀⠈⠉⠻⢵⡲⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀ ",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡇⠀⠀⠀⠀⣰⠃⠀⠀⣾⣿⠛⠻⣿⡆⠀⠀⠀⠀⠀⠀⠀⠈⠻⣝⣢⣄⠀⠀⠀⡀⠀ ",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⣠⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇⠀⠀⠀⠀⡇⠀⠀⣸⣿⣷⣶⣶⠿⠃⣤⡀⠀⠀⠀⠀⠀⠀⠀⠈⡟⣎⣳⣴⠊⠁⠀",
    "⠀⠀⠀⠀⠀⠀⠀⣀⣤⣾⠁⠈⣧⠀⠰⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣄⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⢧⠀⢠⣿⡏⠀⠈⣿⡦⠀⣿⡇⢀⣼⣶⢄⣀⣀⡀⠀⣻⣯⣧⡌⢣ ",
    "⠀⠀⠀⠀⠀⠀⠐⡇⠀⠘⠁⠀⠘⠲⢤⡀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⢠⠇⠀⠀⠀⠀⠈⢦⠘⠻⠿⣶⣾⡿⠃⠀⣿⣥⣾⠟⢡⣾⡟⠛⢿⣧⢧⣿⣿⣷⠀⢳",
    "⠀⠀⠀⠀⠀⠀⠀⠙⢦⣄⠀⣠⠤⠤⠄⠙⡇⠀⠀⢨⠷⢶⡋⠀⠀⠀⠀⠀⢀⣴⠋⠀⠀⠀⠀⠀⠀⠀⠳⣄⠀⠀⠀⠀⠀⣠⣿⡿⠃⠀⣾⣿⠛⠻⣿⡿⢰⣿⣯⠎⡟⢸ ",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⢷⣀⡴⠂⢠⣇⡀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀ ⠀⠈⠑⢦⣀⠀⠼⠿⠋⠀⠀⠀⠈⠻⢷⣶⡎⢠⣬⣝⡿⢴⢃⡾  ",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⠤⣤⣤⡴⠋⠀⠹⣽⣛⣛⣿⠋⠉⠉⢁⡴⢋⣳⠀⠀⠀⠀⠀   ⠀⠀⠀⠀⠈⢑⡶⠀⠀⠀⠀⠀⠀⠀⠠⡐⠀⠘⠛⠓⣚⡶⠟⠀⠀  ",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⣄⡀⠀⠀⠉⠁⠀⠀⠀⣠⡞⠓⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⠋⠀⠀⣄⣠⡴⠞⠒⠢⡤⠂⠑⠒⠚⠋⠉⠀⠀⠀    ",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡍⠓⠦⢤⠤⠴⠶⣺⠟⠀⠀⠀⠀⠀⠀⢀⣀⡰⢲⠀⠀⠀ ⠑⠒⠊⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀              ",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠒⠛⠲⠶⠚⠁⠀⠀⠀⠀⠀⠀⠀⣏⠉⠁⠈⠲⣤                                 ",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⣁⡀⠀⡞⠁                                  ",
    "⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠈⠙⠁⠀                                   "
]


def safe_addstr(
    stdscr,
    row: int,
    col: int,
    text: str,
    color_pair: int = 0
) -> None:
    """Write text safely on screen, ignoring harmless curses edge errors."""
    try:
        if color_pair > 0:
            stdscr.addstr(row, col, text, curses.color_pair(color_pair))
        else:
            stdscr.addstr(row, col, text)
    except curses.error:
        pass


def build_all_lines(
    maze: Maze,
    path: list[Cell],
    solved: bool,
    menu_lines: list[str]
) -> list[str]:
    """Combine maze lines with menu lines into one scrollable view."""
    maze_lines = build_ascii_maze(maze, path, solved).split("\n")

    if not menu_lines:
        return maze_lines
    return maze_lines + [""] + menu_lines


def draw_maze_line(
    stdscr,
    row: int,
    text: str,
    wall_color_index: int
) -> None:
    """Draw one maze line, coloring only wall characters."""
    wall_color_pair = get_wall_color_pair(wall_color_index)

    for col, char in enumerate(text):
        if is_wall_char(char):
            safe_addstr(stdscr, row, col, char, wall_color_pair)
        else:
            safe_addstr(stdscr, row, col, char)


def draw_interface(
    stdscr,
    maze: Maze,
    path: list[Cell],
    solved: bool,
    menu_lines: list[str],
    wall_color_index: int,
    offset_row: int = 0,
    offset_col: int = 0
) -> tuple[int, int]:
    """Draw maze and menu inside stdscr with scroll support."""
    stdscr.erase()
    max_y, max_x = stdscr.getmaxyx()

    all_lines = build_all_lines(maze, path, solved, menu_lines)
    maze_lines = build_ascii_maze(maze, path, solved).split("\n")
    maze_line_count = len(maze_lines)
    visible_width = max(0, max_x - 1)

    for i in range(max_y):
        src_row = offset_row + i
        if src_row >= len(all_lines):
            break

        line = all_lines[src_row][offset_col:offset_col + visible_width]

        if src_row < maze_line_count:
            draw_maze_line(stdscr, i, line, wall_color_index)
        else:
            safe_addstr(stdscr, i, 0, line)

    stdscr.refresh()

    max_offset_row = max(0, len(all_lines) - max_y)
    max_line_width = max((len(line) for line in all_lines), default=0)
    max_offset_col = max(0, max_line_width - visible_width)
    return max_offset_row, max_offset_col


def animate_generation_curses(
    stdscr,
    frames: list[Maze],
    path: list[Cell],
    solved: bool,
    wall_color_index: int
) -> None:
    """Animate maze generation inside curses."""
    stdscr.nodelay(True)
    for maze in frames:
        draw_interface(
            stdscr,
            maze,
            path,
            solved,
            menu_lines=[],
            wall_color_index=wall_color_index,
        )
        curses.napms(20)
    stdscr.nodelay(False)
    stdscr.getch()


def animate_path_curses(
    stdscr,
    maze: Maze,
    path: list[Cell],
    solved: bool,
    wall_color_index: int
) -> None:
    """Animate the solution path inside curses."""
    stdscr.nodelay(True)
    for i in range(len(path)):
        partial_path = path[:i + 1]
        draw_interface(
            stdscr,
            maze,
            partial_path,
            solved,
            menu_lines=[],
            wall_color_index=wall_color_index,
        )
        curses.napms(50)
    stdscr.nodelay(False)
    stdscr.getch()


def print_bye_message(stdscr, offset_row: int = 0,
                      offset_col: int = 0) -> None:
    stdscr.erase()  # Clean screen
    max_y, max_x = stdscr.getmaxyx()  # Max screen size
    visible_width = max(0, max_x - 1)

    for i in range(max_y):
        src_row = offset_row + i  # We offset to start painting from scroll
        if src_row >= len(BYE_MESSAGE):
            break
        full_line = BYE_MESSAGE[src_row]
        end_col = offset_col + visible_width
        visible_line = full_line[offset_col:end_col]  # Print from offset col
        safe_addstr(stdscr, i, 0, visible_line)

    stdscr.refresh()  # This is when we print!
