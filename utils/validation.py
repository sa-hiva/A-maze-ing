from pathlib import Path
import os


def validate(
    content: dict[str, str]
) -> tuple[int, int, tuple[int, int], tuple[int, int], str, bool, int]:
    """Validate the parsed configuration.

    Args:
        content: Configuration parameters read from the config file.

    Returns:
        The validated maze settings.

    Raises:
        ValueError: If any configuration value is invalid.
        PermissionError: If the output directory is not writable.
        FileExistsError: If the output file already exists.
    """

    def read_int(key: str) -> int:
        """Read an integer configuration value.

        Args:
            key: Configuration key to read.

        Returns:
            The parsed integer value.

        Raises:
            ValueError: If the parameter is missing or is not an integer.
        """
        raw_value = content.get(key)
        if raw_value is None:
            raise ValueError(f"Error: Missing required parameter '{key}'")
        try:
            return int(raw_value)
        except ValueError as error:
            raise ValueError(
                f"Error: '{key}' must be an integer") from error

    def parse_coords(key: str, width: int, height: int) -> tuple[int, int]:
        """Read and validate a coordinate pair.

        Args:
            key: Configuration key to read.
            width: Maze width.
            height: Maze height.

        Returns:
            The coordinates as (row, column).
        """
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
        """Read a boolean configuration value.

        Args:
            key: Configuration key to read.
            default: Value to return if the parameter is missing.

        Returns:
            The parsed boolean value.

        Raises:
            ValueError: If the value is not True or False.
        """
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

    def read_seed() -> int | None:
        """Read the random seed from the configuration.

        Returns:
            The seed value, or None if no seed was provided.
        """
        raw_value = content.get("SEED")
        if not raw_value:
            return None
        return read_int("SEED")

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

    path = Path(output_filename)

    if not path.parent.exists():
        raise ValueError("Error: Output directory does not exist.")
    if not os.access(path.parent, os.W_OK):
        raise PermissionError("Error: Cannot write to output directory.")
    if path.exists():
        raise FileExistsError("Error: Output file already exists.")

    perfect = parse_bool("PERFECT", False)
    seed = read_seed()

    return (
        width,
        height,
        entry_coords,
        exit_coords,
        output_filename,
        perfect,
        seed)
