import sys
import curses
from mazegen import MazeGenerator
from mazegen import solve_maze, get_directions_from_path
from utils import parse_config, validate, save_maze_output
from visual import draw_interface, animate_generation_curses
from visual import animate_path_curses

__all__ = ["save_maze_output"]

MENU_TEMPLATE = [
    "=== MENU ===",
    "",
    "1. New maze",
    "2. Show/Hide path",
    "3. Some other shit I'm forgetting",
    "4. Enable/Disable generator animations",
    "5. Enable/Disable path animations",
    "6. Exit",
]


def build_menu_lines(animate_gen: bool, animate_sol: bool) -> list[str]:
    menu_lines = []
    for line in MENU_TEMPLATE:
        if line.startswith("4."):
            line = (f"4. Enable/Disable generator animations "
                    f"Current: {'On' if animate_gen else 'Off'})")
        elif line.startswith("5."):
            line = (f"5. Enable/Disable path animations "
                    f"Current: {'On' if animate_sol else 'Off'})")
        menu_lines.append(line)
    menu_lines.append("")
    menu_lines.append("Select an option: ")
    return menu_lines


def run(stdscr, config_path: str) -> None:
    curses.curs_set(0)     # Hides cursos
    stdscr.keypad(True)    # activates detection of keypad
    curses.start_color()
    curses.use_default_colors()

    content = parse_config(config_path)
    (
        width,
        height,
        entry_coords,
        exit_coords,
        output_file,
        perfect,
    ) = validate(content)

    generator = MazeGenerator()
    maze, frames = generator.generate(width, height, entry_coords,
                                      exit_coords, perfect)
    path = solve_maze(maze)
    save_maze_output(output_file, maze, get_directions_from_path(path))

    solved = False
    animate_gen = False
    animate_sol = True
    offset_row, offset_col = 0, 0

    if animate_gen:
        animate_generation_curses(stdscr, frames, path, solved)

    while True:
        menu_lines = build_menu_lines(animate_gen, animate_sol)
        max_offset_row, max_offset_col = draw_interface(
            stdscr, maze, path, solved, menu_lines,
            offset_row, offset_col
        )
        key = stdscr.getch()  # Detects pressed key!

        if key == curses.KEY_UP:
            offset_row = max(0, offset_row - 1)
        elif key == curses.KEY_DOWN:
            offset_row = min(max_offset_row, offset_row + 1)
        elif key == curses.KEY_LEFT:
            offset_col = max(0, offset_col - 1)
        elif key == curses.KEY_RIGHT:
            offset_col = min(max_offset_col, offset_col + 1)
        elif key == curses.KEY_RESIZE:
            pass  # resize is managed by draw_interface

        elif key == ord("1"):
            solved = False
            offset_row, offset_col = 0, 0
            maze, frames = generator.generate(width, height, entry_coords,
                                              exit_coords, perfect)
            if animate_gen:
                animate_generation_curses(stdscr, frames, path, solved)
            path = solve_maze(maze)

        elif key == ord("2"):
            solved = not solved
            if animate_sol and solved:
                animate_path_curses(stdscr, maze, path, solved)

        elif key == ord("3"):
            pass

        elif key == ord("4"):
            animate_gen = not animate_gen

        elif key == ord("5"):
            animate_sol = not animate_sol

        elif key == ord("6"):
            break


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    try:
        # Wrapper sets up curses instead of doing it manually
        curses.wrapper(run, sys.argv[1])
    except ValueError as error:
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
