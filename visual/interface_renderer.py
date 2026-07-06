import curses
from mazegen import Maze, Cell
from .maze_renderer import build_ascii_maze


def safe_addstr(stdscr, row: int, col: int, text: str) -> None:
    """Method to ignore the error thrown by curses when
    writing on the last cell of the screen, since in
    this case it does not represent a problem, as we are
    already handling the other possible edge cases."""

    try:
        stdscr.addstr(row, col, text)
    except curses.error:
        pass


def build_all_lines(maze: Maze, path: list[Cell], solved: bool,
                    menu_lines: list[str]) -> list[str]:
    """Combines the rendered maze with the already-formatted menu lines.
    If menu_lines is empty, only the maze is returned (used during
    animations, where no menu should be shown)."""

    maze_lines = build_ascii_maze(maze, path, solved).split("\n")

    if not menu_lines:
        return maze_lines
    return maze_lines + [""] + menu_lines


def draw_interface(stdscr, maze: Maze, path: list[Cell], solved: bool,
                   menu_lines: list[str],
                   offset_row: int = 0, offset_col: int = 0
                   ) -> tuple[int, int]:
    """Draws the maze (and optionally a menu below it) inside stdscr,
    cropped according to offset_row/offset_col. Returns the maximum
    valid offsets, so the caller can clamp scrolling to the content size."""

    # Supose that stdr is the camera. max_y and max_x represent the maximum
    # of the screen (terminal window). Offsets represent the starting point
    # on each axis in relation to the viewport (in order to be able to scroll)

    stdscr.erase()  # Clean screen
    max_y, max_x = stdscr.getmaxyx()  # Get max screen size 

    all_lines = build_all_lines(maze, path, solved, menu_lines)
    visible_width = max(0, max_x - 1) 

    for i in range(max_y):
        src_row = offset_row + i  # We offset to start painting from scroll
        if src_row >= len(all_lines):
            break
        full_line = all_lines[src_row]
        end_col = offset_col + visible_width
        visible_line = full_line[offset_col:end_col] # Only print from offset col
        safe_addstr(stdscr, i, 0, visible_line)

    stdscr.refresh() # This is when we print! 

    max_scroll_row = max(0, len(all_lines) - max_y) # Max row that can be on top
    max_line_width = max((len(line) for line in all_lines), default=0)
    max_scroll_col = max(0, max_line_width - visible_width)
    return max_scroll_row, max_scroll_col


def animate_generation_curses(stdscr, frames: list[Maze],
                              path: list[Cell], solved: bool) -> None:
    for maze in frames:
        draw_interface(stdscr, maze, path, solved, menu_lines=[])
        curses.napms(20)


def animate_path_curses(stdscr, maze: Maze, path: list[Cell],
                        solved: bool) -> None:
    for i in range(len(path)):
        partial_path = path[:i + 1]
        draw_interface(stdscr, maze, partial_path, solved, menu_lines=[])
        curses.napms(50)
