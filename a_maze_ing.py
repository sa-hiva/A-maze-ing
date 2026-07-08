import sys
import curses
import time
from mazegen import MazeGenerator
from mazegen import solve_maze, get_directions_from_path
from utils import parse_config, validate, save_maze_output
from visual import draw_interface, animate_generation_curses
from visual import animate_path_curses, print_bye_message, init_colors
from visual import next_wall_color_index
from utils.io import boom
from visual import animate_invalid_key_spam

__all__ = ["save_maze_output"]

MENU_TEMPLATE = [
    "*✧:･ﾟ✧*:･ﾟ✧*･ﾟ✧*:･ﾟ✧*",
    "*✧      MENU       ✧*",
    "*✧:･ﾟ✧*:･ﾟ✧*･ﾟ✧*:･ﾟ✧*",
    "",
    "1. New maze",
    "2. Show/Hide path",
    "3. Change wall color",
    "4. Enable/Disable generator animations",
    "5. Enable/Disable path animations",
    "6. Exit",
    "",
]


def build_menu_lines(animate_gen: bool, animate_sol: bool,
                     status_message: str,
                     generator: MazeGenerator) -> list[str]:
    menu_lines = []
    for line in MENU_TEMPLATE:
        if line.startswith("1. "):
            line = (f"1. New maze (Current: maze n.{generator.maze_seed})")
        if line.startswith("4."):
            line = (f"4. Enable/Disable generator animations "
                    f"(Current: {'On' if animate_gen else 'Off'})")
        elif line.startswith("5."):
            line = (f"5. Enable/Disable path animations "
                    f"(Current: {'On' if animate_sol else 'Off'})")
        menu_lines.append(line)
    menu_lines.append("Select an option: ")
    if status_message:
        menu_lines[-1] += status_message
    return menu_lines


def run(stdscr, config_path: str) -> None:
    curses.curs_set(0)     # Hides curses
    stdscr.keypad(True)    # activates detection of keypad
    curses.start_color()
    curses.use_default_colors()
    init_colors()

    content = parse_config(config_path)
    (
        width,
        height,
        entry_coords,
        exit_coords,
        output_file,
        perfect,
        seed
    ) = validate(content)

    invalid_key_count = 0
    status_message = ""
    generator = MazeGenerator(seed)
    maze, frames, pattern_msg = generator.generate(width, height, entry_coords,
                                                   exit_coords, perfect)
    if pattern_msg:
        MENU_TEMPLATE[:0] = [pattern_msg, ""]

    path = solve_maze(maze)
    save_maze_output(output_file, maze, get_directions_from_path(path))

    solved = False
    animate_gen = False
    animate_sol = False
    offset_row, offset_col = 0, 0
    wall_color_index = 0

    if animate_gen:
        animate_generation_curses(stdscr, frames, path,
                                  solved, wall_color_index)

    while True:
        menu_lines = build_menu_lines(animate_gen, animate_sol,
                                      status_message, generator)
        max_scroll_row, max_scroll_col = draw_interface(
            stdscr, maze, path, solved, menu_lines,
            wall_color_index, offset_row, offset_col)

        try:
            key = stdscr.getch()  # Detects pressed key!

            if key == curses.KEY_UP:
                offset_row = max(0, offset_row - 1)
            elif key == curses.KEY_DOWN:
                offset_row = min(max_scroll_row, offset_row + 1)
            elif key == curses.KEY_LEFT:
                offset_col = max(0, offset_col - 1)
            elif key == curses.KEY_RIGHT:
                offset_col = min(max_scroll_col, offset_col + 1)
            elif key == curses.KEY_RESIZE:
                pass  # resize is managed by draw_interface

            elif key == ord("1"):
                solved = False
                offset_row, offset_col = 0, 0
                generator.reset(seed)
                (maze,
                 frames,
                 pattern_msg) = generator.generate(width, height, entry_coords,
                                                   exit_coords, perfect)
                if pattern_msg and MENU_TEMPLATE[0].startswith("*✧:･ﾟ"):
                    MENU_TEMPLATE[:0] = [pattern_msg, ""]
                elif not pattern_msg and MENU_TEMPLATE[0].startswith("Maze"):
                    del MENU_TEMPLATE[:2]

                if animate_gen:
                    animate_generation_curses(stdscr, frames, path,
                                              solved, wall_color_index)
                path = solve_maze(maze)
                status_message = ""

            elif key == ord("2"):
                solved = not solved
                if animate_sol and solved:
                    animate_path_curses(stdscr, maze, path,
                                        solved, wall_color_index)
                status_message = ""

            elif key == ord("3"):
                wall_color_index = next_wall_color_index(wall_color_index)

            elif key == ord("4"):
                animate_gen = not animate_gen
                status_message = ""

            elif key == ord("5"):
                animate_sol = not animate_sol
                status_message = ""

            elif key == ord("6"):
                print_bye_message(stdscr, offset_row, offset_col)
                time.sleep(1)
                break
            else:
                status_message = "Invalid option"
                invalid_key_count += 1
                if invalid_key_count > 0 and invalid_key_count % 3 == 0:
                    animate_invalid_key_spam(stdscr,)
                    status_message = ""
        except (EOFError, KeyboardInterrupt):
            stdscr.addstr("\n[ERROR, INVALID KEY]")
            stdscr.refresh()
            # boom()
            # sys.exit(1)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    try:
        # Wrapper sets up curses instead of doing it manually
        curses.wrapper(run, sys.argv[1])
    except (ValueError, PermissionError, FileExistsError) as error:
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
