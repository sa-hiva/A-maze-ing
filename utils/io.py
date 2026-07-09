from mazegen import Maze


def parse_config(file_path: str) -> dict[str, str]:
    """Reads a configuration file containing one KEY=VALUE pair per line.
    Blank lines and comments starting with '#' are ignored.

    Args:
        file_path: Path to the configuration file.

    Returns:
        A dictionary mapping configuration keys to their values.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        PermissionError: If the configuration file cannot be read.
        ValueError: If the configuration file contains invalid syntax,
            duplicate keys, or empty parameter names.
    """
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
        raise FileNotFoundError(
            f"Error: Configuration file '{file_path}' not found") from error
    except PermissionError as error:
        raise PermissionError(
            f"Error: Permission denied reading configuration file "
            f"'{file_path}'") from error

    return content


def save_maze_output(file_path: str, maze: Maze, solution: str) -> None:
    """Save a generated maze to an output file.

    Args:
        file_path: Destination output file.
        maze: Maze to save.
        solution: Shortest path encoded as movement directions.

    Raises:
        PermissionError: If the output file cannot be written.
        FileNotFoundError: If the output file cannot be found
    """

    try:
        with open(file_path, "w") as file:
            file.write(maze.to_hex_str())
            file.write("\n")
            file.write(f"{maze.entry[1]},{maze.entry[0]}")
            file.write("\n")
            file.write(f"{maze.exit[1]},{maze.exit[0]}")
            file.write("\n")
            file.write(solution)
            file.write("\n")

    except PermissionError as error:
        raise PermissionError(
            f"Error: Permission denied writing output file "
            f"'{file_path}'") from error
    except FileNotFoundError:
        raise FileNotFoundError("Output file not found")
