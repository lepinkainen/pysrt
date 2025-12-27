"""pysrt - SubRip (.srt) subtitle parser and writer."""

from pysrt.srtexc import Error, InvalidItem, InvalidTimeString
from pysrt.srtfile import SubRipFile
from pysrt.srtitem import SubRipItem
from pysrt.srttime import SubRipTime
from pysrt.validation import ValidationError, ValidationOptions
from pysrt.version import VERSION, VERSION_STRING

__all__ = [
    "SubRipFile",
    "SubRipItem",
    "SubRipTime",
    "Error",
    "InvalidItem",
    "InvalidTimeString",
    "ValidationError",
    "ValidationOptions",
    "VERSION",
    "VERSION_STRING",
]

ERROR_PASS = SubRipFile.ERROR_PASS
ERROR_LOG = SubRipFile.ERROR_LOG
ERROR_RAISE = SubRipFile.ERROR_RAISE

open = SubRipFile.open
stream = SubRipFile.stream
from_string = SubRipFile.from_string
