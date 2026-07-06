PYTHON = python3
VENV = .venv
VENV_PYTHON = $(VENV)/bin/python
VENV_PIP = $(VENV)/bin/pip

MAIN = a_maze_ing.py
CONFIG = config.txt

install:
	python3 -m venv $(VENV)
	$(VENV_PIP) install -U pip
	$(VENV_PIP) install flake8 mypy

run:
	$(VENV_PYTHON) $(MAIN) $(CONFIG)

debug:
	$(VENV_PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf dist build *.egg-info $(VENV)

lint:
	$(VENV_PYTHON) -m flake8 .
	$(VENV_PYTHON) -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(VENV_PYTHON) -m flake8 .
	$(VENV_PYTHON) -m mypy . --strict

.PHONY: install run debug clean lint lint-strict