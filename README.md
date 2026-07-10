*This project has been created as part of the 42 curriculum by shierro, valmoral.*

# A-Maze-ing

## Description

A-Maze-ing is a Python 3.10+ maze generator and solver driven by a configuration file. The program reads maze parameters, generates a maze, computes a shortest valid path from entry to exit, writes the result in the required hexadecimal format, and displays the maze in a terminal interface with scrolling and interaction controls.

The project is organized around a reusable maze-generation module and a terminal application. The reusable module exposes the maze structure, generation logic, and solving logic, while the main script handles configuration parsing, validation, output writing, and the interactive curses-based display.

Main features include:

- Configuration-driven maze generation and export.
- Reusable `MazeGenerator`, `Maze`, `Cell`, and solver utilities.
- Shortest-path computation using breadth-first search.
- Hexadecimal wall encoding written row by row to an output file, followed by entry, exit, and path data.
- Terminal visualization with scroll support, path toggling, generation/path animation toggles, and wall-color cycling.
- A centered `42` pattern embedded in the maze when the dimensions allow it.

## Instructions

### Requirements

- Python 3.10 or later.
- A terminal compatible with Python's `curses` module.
- Recommended: a virtual environment for local development.

### Installation

The project includes a `Makefile` for common tasks such as install, run, debug, clean, and lint. A typical local setup is:

```bash
make install
```

If you prefer to run the project directly without the Makefile, the required command is:

```bash
python3 a_maze_ing.py config.txt
```

### Execution

The mandatory execution format is:

```bash
python3 a_maze_ing.py config.txt
```

`a_maze_ing.py` is the main program file, and `config.txt` is the configuration file passed as the only argument.

### Interactive controls

The terminal interface is based on a curses event loop and supports these actions:

- `1`: Generate a new maze.
- `2`: Show or hide the shortest path.
- `3`: Cycle the maze wall color without changing other rendered elements.
- `4`: Enable or disable generation animation.
- `5`: Enable or disable path animation.
- `6`: Exit the program.
- Arrow keys: Scroll when the maze and menu are larger than the terminal window.

## Configuration file format

The configuration file uses one `KEY=VALUE` pair per line, and lines starting with `#` are treated as comments. The subject defines these mandatory keys:

| Key | Description |
|---|---|
| `WIDTH` | Maze width in cells |
| `HEIGHT` | Maze height in cells |
| `ENTRY` | Entry coordinates as `x,y` |
| `EXIT` | Exit coordinates as `x,y` |
| `OUTPUT_FILE` | Output filename |
| `PERFECT` | Whether perfect-maze mode is requested |

The subject also allows additional keys such as a random seed or display-related options.

### Example configuration

```txt
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

## Output file format

The output file stores one hexadecimal digit per cell, where each bit encodes whether a wall is closed on the north, east, south, or west side. Rows are written line by line, and after an empty line the file contains the entry coordinates, exit coordinates, and the shortest valid path using the letters `N`, `E`, `S`, and `W`.

This format allows the result to be checked by automated tools and by the provided analysis script.

## Algorithms

### Maze generation

The maze is generated with a `MazeGenerator` class using recursive backtracking, a randomized depth-first approach. Starting from one cell, it explores an unvisited neighbor, removes the wall between them, and continues until the maze is fully carved. This creates a connected maze with a natural winding structure and supports the project’s perfect-maze mode.

The generator also supports an optional seed for reproducibility and inserts the `42` pattern when the board is large enough.

### Pathfinding

The shortest path from the entry to the exit is found with breadth-first search in `solver.py`. Unlike the depth-first generation step, breadth-first search explores the maze level by level, which guarantees the first time it reaches the exit is through the shortest valid path.

### Why this algorithm

Recursive backtracking is simple and efficient because it naturally carves passages between adjacent cells. Breadth-first search complements it by guaranteeing the shortest path without extra validations.

## Visual representation

The project uses terminal rendering through a curses-based interface. The renderer builds an ASCII maze using Unicode box-drawing characters, then displays only the visible viewport so the user can scroll when the content exceeds terminal size.

The visual output currently includes walls, the `42` pattern, the optional shortest path, and menu controls. Wall colors can be cycled independently from the other rendered elements, which satisfies the required interaction to change maze wall colors.

## Reusable module

The subject requires the maze generation logic to be reusable through a standalone module and packaged as a distributable `mazegen-*` archive or wheel at the repository root. The current codebase already separates core concepts into reusable components such as `Cell`, `Maze`, `MazeGenerator`, and the solver utilities.

### Basic usage example

```python
from mazegen import MazeGenerator
from mazegen import solve_maze, get_directions_from_path

entry = (0, 0)
exit_ = (19, 14)

generator = MazeGenerator()
maze, frames = generator.generate(20, 15, entry, exit_, perfect=True)
path = solve_maze(maze)
directions = get_directions_from_path(path)
```

### Custom parameters

The generator currently accepts custom maze size, entry and exit coordinates, and perfect-mode behavior through the generation call. If seed-based reproducibility and additional generation modes are added later, they can be exposed here in the same style and kept consistent with the configuration parser.

### Accessing the structure and a solution

The generated maze structure is stored in a `Maze` object containing the matrix of `Cell` instances, entry and exit coordinates, wall states, and helper methods for neighbor and wall logic. A valid shortest solution can be retrieved by running `solve_maze(maze)` and then turning the resulting path into movement directions with `get_directions_from_path(path)`.

## Repository structure

A simplified view of the current project organization is:

```text
.
├── a_maze_ing.py
├── config.txt
├── LICENSE.md
├── Makefile
├── mazegen-1.0.0-py3-none-any.whl
├── pyproject.toml
├── README.md
├── mazegen/
│   ├── __init__.py
│   ├── cell.py
│   ├── generator.py
│   ├── maze.py
│   └── solver.py
└── utils/
    ├── __init__.py
    ├── io.py
    └── validation.py
    └── visual/
        ├── __init__.py
        ├── bad_usage.py
        ├── colors.py
        ├── interface_renderer.py
        └── maze_renderer.py
```

This structure separates core maze logic, utility functions, and rendering responsibilities, which is consistent with the reusability objective of the subject.

## Team and project management

### Roles of each team member

Both `shierro` and `valmoral` participated meaningfully in the full project, including ideation, logic, documentation, design, coding, debugging, polishing and *prettifying*.

### Planning and evolution

The project started with a focus on the core maze pipeline: parse configuration, generate the maze, solve it, and write the output file. Over time, the implementation was extended with a curses interface, scrolling, animations, reusable module structure, and wall-color selection.

The work evolved through multiple rounds of testing and refinement, especially around output format, rendering behavior, and subject compliance. The current version reflects a shared effort to keep the code understandable, modular, and practical for submission.

### What worked well and what could be improved

The separation between generation, solving, output, and rendering worked well because each piece can be understood and tested independently. The reusable maze module is also a strong point because it exposes the maze structure and solver in a way that can be reused later.

What could still be improved is final packaging polish, and further simplification of presentation code if more visual modes are added later.

### Tools used

The team used Python 3.10+, the standard library, `curses` for terminal rendering, and development tools such as `flake8` and `mypy`. AI was used for explanations of concepts, debugging support, and documentation assistance. All generated suggestions were reviewed, tested, and adapted before being integrated into the project.

## Resources

- 42 A-Maze-ing subject PDF for the project specification *(version 1 and 2)*
- Python `curses` documentation for terminal rendering patterns.
- ChatGPT and Perplexity as AI assistance, for uses listed above.