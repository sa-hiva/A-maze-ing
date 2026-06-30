import sys


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


def validate(
    content: dict[str, str]
) -> tuple[int, int, tuple[int, int], tuple[int, int], str, bool]:

    def read_int(key: str) -> int:
        raw_value = content.get(key)
        if raw_value is None:
            raise ValueError(f"Error: Missing required parameter '{key}'")
        try:
            return int(raw_value)
        except ValueError as error:
            raise ValueError(
                f"Error: '{key}' must be an integer") from error

    def parse_coords(key: str, width: int, height: int) -> tuple[int, int]:
        raw_value = content.get(key)
        if raw_value is None:
            raise ValueError(f"Error: Missing required parameter '{key}'")

        try:
            x_str, y_str = raw_value.split(",", 1)
            x = int(x_str.strip())
            y = int(y_str.strip())
        except ValueError as error:
            raise ValueError(
                f"Error: '{key}' must have format x,y") from error

        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(
                f"Error: {key} coordinates are out of maze bounds")

        return (y, x)

    def parse_bool(key: str, default: bool) -> bool:
        raw_value = content.get(key)
        if raw_value is None or raw_value == "":
            return default

        normalized = raw_value.strip().upper()
        if normalized == "TRUE":
            return True
        if normalized == "FALSE":
            return False

        raise ValueError(
            f"Error: '{key}' must be either True or False")

    width = read_int("WIDTH")
    height = read_int("HEIGHT")

    if width < 5 or height < 5:
        raise ValueError("Error: Min dimensions are 5x5")
    if width > 52 or height > 20:
        raise ValueError("Error: Max dimensions are WIDTH=52 and HEIGHT=20")

    entry_coords = parse_coords("ENTRY", width, height)
    exit_coords = parse_coords("EXIT", width, height)

    if entry_coords == exit_coords:
        raise ValueError("Error: ENTRY and EXIT cannot be the same")

    output_filename = content.get("OUTPUT_FILE", "maze.txt").strip()

    if not output_filename:
        output_filename = "maze.txt"

    if not output_filename.endswith(".txt"):
        raise ValueError("Error: OUTPUT_FILE must end with '.txt'")

    perfect = parse_bool("PERFECT", True)

    return (
        width,
        height,
        entry_coords,
        exit_coords,
        output_filename,
        perfect)


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
    except ValueError as error:
        print(error)
        sys.exit(1)

    print("=== VALID CONFIG ===")
    print(f"Width: {width}, Height: {height}")
    print(f"Entry: {entry_coords}, Exit: {exit_coords}")
    print(f"Output file: {output_file}")
    print(f"Perfect maze: {perfect}")


if __name__ == "__main__":
    main()
