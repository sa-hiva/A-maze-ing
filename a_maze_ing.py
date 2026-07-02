import sys
from mazegen import Maze
from utils import parse_config, validate, save_maze_output
from visual import show_maze

__all__ = ["Random"]



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

        maze: Maze = Maze(width, height, entry_coords, exit_coords)
        maze.generate()
        maze.solve()
        print(maze.solution)
        save_maze_output(output_file, maze)
        show_maze(maze)

    except ValueError as error:
        print(error)
        sys.exit(1)

    # print("=== VALID CONFIG ===")
    # print(f"Width: {width}, Height: {height}")
    # print(f"Entry: {entry_coords}, Exit: {exit_coords}")
    # print(f"Output file: {output_file}")
    # print(f"Perfect maze: {perfect}")
    # print()


if __name__ == "__main__":
    main()
