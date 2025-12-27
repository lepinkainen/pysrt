"""Compatibility module - Python 3.11+ only."""

# For backward compatibility with code that imports from compat
basestring = (str, bytes)
str = str
open = open
is_py2 = False
is_py3 = True
