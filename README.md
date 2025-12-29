# pysrt

pysrt is a Python library used to edit or create SubRip files.

## About This Fork

I needed a subtile library for [lepinkainen/subtrans](https://github.com/lepinkainen/subtrans) and used [byroot/pysrt](https://github.com/byroot/pysrt) for a while, but it was 4 years old and unmaintained, so I decided to fork it and modernize it a bit.

This fork has the following enhancements:

- **Modern tooling**: Migrated to Python 3.11+ with uv, ruff, mypy, and task-based builds
- **Subtitle validation**: Detect timing issues, overlaps, malformed entries, and control characters
- **Overlap fixing**: Intelligently adjust subtitle timing to fix overlaps with configurable buffer

## Foreword

pysrt is mainly designed as a library. But for convenience,
pysrt also provides an `srt` command useful for shifting, splitting, rescaling,
breaking long lines, validating, and fixing overlaps in `.srt` files.

## CLI Usage

Examples:

```bash
# Shifting
srt -i shift 2s500ms movie.srt

# Splitting
srt split 58m26s movie.srt

# Rescaling
srt -i rate 23.9 25 movie.srt

# Break long lines
srt break 42 movie.srt > wrapped.srt

# Validate subtitle file
srt validate movie.srt

# Fix overlapping subtitles
srt -i fix-overlaps movie.srt
srt fix-overlaps --buffer 50 movie.srt > fixed.srt

# Set output encoding
srt -e iso-8859-1 shift 2s movie.srt > output.srt
```

Notes:

- `-i/--in-place` edits files in-place and creates a `.bak` backup (not supported for `split`).
- `-e/--output-encoding` sets the output encoding for the written subtitles.

## Library Usage

Import:

```python
import pysrt
```

Parsing:

```python
subs = pysrt.open("some/file.srt")
# If you get a UnicodeDecodeError try to specify the encoding
subs = pysrt.open("some/file.srt", encoding="iso-8859-1")
```

SubRipFile objects are list-like collections of SubRipItem instances:

```python
len(subs)
first_sub = subs[0]
```

SubRipItem instances are editable just like pure Python objects:

```python
first_sub.text = "Hello World !"
first_sub.start.seconds = 20
first_sub.end.minutes = 5
```

Shifting:

```python
subs.shift(seconds=-2)  # Move all subs 2 seconds earlier
subs.shift(minutes=1)  # Move all subs 1 minute later
subs.shift(ratio=25 / 23.9)  # Convert 23.9 fps subtitles to 25 fps
first_sub.shift(seconds=1)  # Move the first sub 1 second later
first_sub.start += {"seconds": -1}  # Make the first sub start 1 second earlier
```

Removing:

```python
del subs[12]
```

Slicing:

```python
part = subs.slice(
    starts_after={"minutes": 2, "seconds": 30},
    ends_before={"minutes": 3, "seconds": 40},
)
part.shift(seconds=-2)
```

Saving changes:

```python
subs.save("other/path.srt", encoding="utf-8")
```

Validating:

```python
errors = subs.validate()
if errors:
    for error in errors:
        print(f"#{error.position} [{error.error_type}] {error.message}")
```

Fixing overlaps:

```python
subs.fix_overlaps(buffer_ms=20)  # Fix overlaps with 20ms minimum gap
subs.save("fixed.srt")
```
