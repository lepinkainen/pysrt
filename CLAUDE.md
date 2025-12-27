# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pysrt is a Python library for parsing and editing SubRip (.srt) subtitle files. It provides both a library API and a command-line tool (`srt`).

## Development Commands

```bash
# Install dependencies
uv sync --extra dev

# Run all tests
task test

# Run tests with verbose output
uv run python -m pytest tests/ -v

# Run a single test file
uv run python -m pytest tests/test_srtfile.py

# Run a single test
uv run python -m pytest tests/test_srtfile.py::TestOpen::test_utf8

# Lint and format code
task lint

# Check linting without auto-fix
task lint-check

# Build package
task build

# Clean build artifacts
task clean
```

## Architecture

The library is built around three core classes in `pysrt/`:

- **SubRipFile** (`srtfile.py`): List-like container of SubRipItem instances. Handles file I/O, encoding detection (including BOM), and operations on subtitle collections (shift, slice, save). Extends `UserList`.

- **SubRipItem** (`srtitem.py`): Represents a single subtitle entry with index, start/end times, text, and optional position. Supports parsing from string/lines.

- **SubRipTime** (`srttime.py`): Time representation in HH:MM:SS,mmm format. Uses an `ordinal` (milliseconds) internally. Supports arithmetic operations and coercion from strings, ints, dicts, and datetime.time objects. Uses custom descriptors (`TimeItemDescriptor`) for hours/minutes/seconds/milliseconds properties.

**Entry points:**
- Library: `pysrt.open()`, `pysrt.from_string()`, `pysrt.stream()` (all delegated to SubRipFile class methods)
- CLI: `srt` command defined in `commands.py` (shift, split, rate, break subcommands)

## Testing

Tests use pytest and are in `tests/`. Test data (.srt files) is in `tests/static/`. Tests cover encoding detection, BOM handling, serialization, slicing, and shifting.
