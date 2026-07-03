import sys
from mazegen import Maze, MazeGenerator
from mazegen.solver import solve_maze
from utils import parse_config, validate, save_maze_output
from visual import show_maze

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
        maze: Maze = generator.generate(width, height, 
                                        entry_coords, exit_coords)
        save_maze_output(output_file, maze)
        path = solve_maze(maze)
        solved = False
        show_maze(maze, path, solved)

    except ValueError as error:
        print(error)
        sys.exit(1)

    while True:
        print()
        print("=== MENU ===")
        print()
        print("1. New maze")
        print("2. Show/Hide path")
        print("3. Some other shit I'm forgetting")
        print("4. Exit")
        print()

        try:
            choice = input("Select an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("[ERROR] Bye!")
            sys.exit(0)

        if choice == "1":
            print("WIP")

        elif choice == "2":
            solved = not solved
            show_maze(maze, path, solved)

        elif choice == "3":
            print("nada")

        elif choice == "4":
            print("Bye bitch!")
            break

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
