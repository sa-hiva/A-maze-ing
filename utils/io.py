import sys
from mazegen import Maze

__all__ = [sys.argc]


def parse_config(file_path: str) -> dict[str, str]:
    content: dict[str, str] = {}

    try:
        with open(file_path, "r") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError(
                        f"Error: Invalid configuration format on line "
                        f"{line_number}: '{line}'")

                key, value = line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()

                if not key:
                    raise ValueError(
                        f"Error: Empty key on line {line_number}")

                if key in content:
                    raise ValueError(
                        f"Error: Duplicate parameter '{key}' in "
                        f"configuration file")

                content[key] = value

    except FileNotFoundError as error:
        raise ValueError(
            f"Error: Configuration file '{file_path}' not found") from error
    except PermissionError as error:
        raise ValueError(
            f"Error: Permission denied reading configuration file "
            f"'{file_path}'") from error

    return content


def save_maze_output(file_path: str, maze: Maze) -> None:
    try:
        with open(file_path, "w") as file:
            file.write(maze.get_maze_as_str())
            file.write("\n")
            file.write(f"{maze.entry[0]},{maze.entry[1]}")
            file.write("\n")
            file.write(f"{maze.exit[0]},{maze.exit[1]}")

    except PermissionError as error:
        raise PermissionError(
            f"Error: Permission denied writing output file "
            f"'{file_path}'") from error
