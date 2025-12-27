# Repository Guidelines

## Project Structure & Module Organization
Source lives in `pysrt/`, with the core types in `srtfile.py` (SubRipFile),
`srtitem.py` (SubRipItem), and `srttime.py` (SubRipTime). The CLI entry point
is `pysrt/commands.py` and is exposed as the `srt` script. Tests are in `tests/`,
with fixture subtitle files under `tests/static/`. Build and tooling settings
are defined in `pyproject.toml` and `Taskfile.yml`. The `llm-shared/` directory
is a git submodule used for shared tooling/templates and is not imported by the
library.

## Build, Test, and Development Commands
- `uv sync --extra dev`: install runtime and dev dependencies.
- `task test`: run the pytest suite (quiet mode).
- `uv run python -m pytest tests/test_srtfile.py::TestOpen::test_utf8`: run a
  single test.
- `task lint`: run Ruff checks, format code, and run mypy.
- `task lint-check`: lint without auto-fix (CI parity).
- `task build`: build wheel/sdist into `build/`.
- `task clean`: remove build/test artifacts and caches.

## Coding Style & Naming Conventions
Python 3.11+ is required. Use 4-space indentation, snake_case for modules and
functions, CapWords for classes, and `test_*.py` for test files. Formatting is
handled by `ruff format` with a 100-character line length. Keep Ruff and mypy
clean; add type hints for new public APIs and for non-trivial internal helpers.

## Testing Guidelines
Tests use pytest and live under `tests/`. Use descriptive `test_` function names
and keep sample `.srt` files in `tests/static/`. For coverage runs (CI), use
`task test-ci`, which emits XML and terminal reports.

## Commit & Pull Request Guidelines
Recent history follows a conventional style like `feat: ...` or `fix: ...`.
Keep messages short and imperative. Pull requests should include a summary, the
commands used to test, and links to relevant issues. If behavior changes, update
`README.rst` or CLI examples as needed.

## Architecture Notes
The library centers on list-like `SubRipFile` collections of `SubRipItem`
entries, with `SubRipTime` handling time arithmetic and parsing. The public
entry points are `pysrt.open()`, `pysrt.from_string()`, and `pysrt.stream()`.
