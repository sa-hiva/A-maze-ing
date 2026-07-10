import curses

WALL_COLOR_PAIRS: list[int] = [0, 1, 2, 3, 4]
WALL_CHARS: set[str] = set("═║╔╗╚╝╠╣╦╩╬")


def init_colors() -> None:
    """Initialize the curses color pairs used for maze walls."""
    curses.init_pair(1, curses.COLOR_BLUE, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_MAGENTA, -1)
    curses.init_pair(4, curses.COLOR_CYAN, -1)


def next_wall_color_index(current_index: int) -> int:
    """Return the next wall color index.

    Args:
        current_index: Current wall color index.

    Returns:
        The next wall color index.
    """
    return (current_index + 1) % len(WALL_COLOR_PAIRS)


def get_wall_color_pair(color_index: int) -> int:
    """Return the curses color pair for a wall.

    Args:
        color_index: Wall color index.

    Returns:
        The corresponding curses color pair.
    """
    safe_index = color_index % len(WALL_COLOR_PAIRS)
    return WALL_COLOR_PAIRS[safe_index]


def is_wall_char(char: str) -> bool:
    """Check whether a character is a maze wall.

    Args:
        char: Character to check.

    Returns:
        True if the character is a wall, False otherwise.
    """
    return char in WALL_CHARS
