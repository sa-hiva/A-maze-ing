import sys
import os
from mazegen import Maze, MazeGenerator, Cell
from mazegen import solve_maze, get_directions_from_path
from utils import parse_config, validate, save_maze_output
from visual import show_maze, animate_generation, clear_screen, animate_path

__all__ = ["save_maze_output"]


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    try:
        content = parse_config(sys.argv[1])
        (
            width,
            height,
            entry_coords,
            exit_coords,
            output_file,
            perfect,
        ) = validate(content)

        generator = MazeGenerator()
        (maze, frames) = generator.generate(width, height, entry_coords,
                                            exit_coords, perfect)

        path = solve_maze(maze)
        save_maze_output(output_file, maze, get_directions_from_path(path))
        solved = False
        animate_gen: bool = False
        animate_sol: bool = True
        if animate_gen:
            animate_generation(frames, path, solved)
        else:
            show_maze(maze, path, solved)
        os.system("clear")

    except ValueError as error:
        print(error)
        sys.exit(1)

    while True:
        draw_interface(maze, path, solved)

        try:
            choice = input("Select an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("[ERROR] Bye!")
            sys.exit(0)

        if choice == "1":
            clear_screen()
            maze, frames = generator.generate(width, height, entry_coords,
                                              exit_coords, perfect)
            path = solve_maze(maze)
            solved = False

        elif choice == "2":
            clear_screen()
            solved = not solved
            if animate_sol and solved:
                animate_path(maze, path, solved)

        elif choice == "3":
            print("nada")

        elif choice == "4":
            print("Bye bitch!\n")
            break

        else:
            print("Invalid option, please try again.")


def draw_interface(maze: Maze, path: list[Cell], solved: bool) -> None:
    print("\033[2J\033[H", end="")
    show_maze(maze, path, solved)

    print()
    print("=== MENU ===")
    print()
    print("1. New maze")
    print("2. Show/Hide path")
    print("3. Some other shit I'm forgetting")
    print("4. Exit\n")


if __name__ == "__main__":
    main()
