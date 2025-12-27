# pysrt

[![Build Status](https://secure.travis-ci.org/byroot/pysrt.png?branch=master)](http://travis-ci.org/byroot/pysrt)
[![Coverage Status](https://coveralls.io/repos/byroot/pysrt/badge.png?branch=master)](https://coveralls.io/r/byroot/pysrt?branch=master)
[![PyPI](https://img.shields.io/pypi/v/pysrt.svg)](https://crate.io/packages/pysrt/)

pysrt is a Python library used to edit or create SubRip files.

## Foreword

pysrt is mainly designed as a library, but if you are experiencing troubles with bad
subtitles you can first try to use [ruby-osdb](https://github.com/byroot/ruby-osdb)
which will try to find the best subtitle for your movie. If you are still unlucky
pysrt also provides an `srt` command useful for shifting, splitting, rescaling, or
breaking long lines in `.srt` files.

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

# Set output encoding
srt -e iso-8859-1 shift 2s movie.srt > output.srt
```

Notes:

- `-i/--in-place` edits files in-place and creates a `.bak` backup (not supported for `split`).
- `-e/--output-encoding` sets the output encoding for the written subtitles.

## Installation

pysrt is available on PyPI:

```bash
pip install pysrt
```

Requires Python 3.11+.

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
