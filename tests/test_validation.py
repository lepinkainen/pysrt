import pytest

from pysrt import SubRipFile, SubRipItem
from pysrt.validation import ValidationError, ValidationOptions


def test_valid_file_passes():
    subs = SubRipFile(
        [
            SubRipItem(1, start="00:00:01,000", end="00:00:03,000", text="Hello"),
            SubRipItem(2, start="00:00:04,000", end="00:00:06,000", text="World"),
        ]
    )
    errors = subs.validate()
    assert errors == []


def test_minimum_subtitle_count():
    subs = SubRipFile([SubRipItem(1, start="00:00:01,000", end="00:00:03,000", text="Only one")])
    errors = subs.validate()
    assert len(errors) == 1
    assert errors[0].error_type == "content"


def test_timing_validity():
    subs = SubRipFile(
        [
            SubRipItem(1, start="00:00:03,000", end="00:00:01,000", text="Backwards"),
            SubRipItem(2, start="00:00:04,000", end="00:00:06,000", text="Normal"),
        ]
    )
    errors = subs.validate()
    timing_errors = [e for e in errors if e.error_type == "timing"]
    assert len(timing_errors) >= 1


def test_overlap_detection():
    subs = SubRipFile(
        [
            SubRipItem(1, start="00:00:01,000", end="00:00:05,000", text="First"),
            SubRipItem(2, start="00:00:04,000", end="00:00:06,000", text="Overlaps"),
        ]
    )
    errors = subs.validate()
    overlap_errors = [e for e in errors if e.error_type == "overlap"]
    assert len(overlap_errors) == 1


def test_duration_too_short():
    subs = SubRipFile(
        [
            SubRipItem(1, start="00:00:01,000", end="00:00:01,100", text="Too fast"),
            SubRipItem(2, start="00:00:02,000", end="00:00:04,000", text="Normal"),
        ]
    )
    errors = subs.validate()
    duration_errors = [e for e in errors if e.error_type == "duration"]
    assert len(duration_errors) >= 1


def test_text_length_too_long():
    long_text = "a" * 600
    subs = SubRipFile(
        [
            SubRipItem(1, start="00:00:01,000", end="00:00:03,000", text=long_text),
            SubRipItem(2, start="00:00:04,000", end="00:00:06,000", text="Normal"),
        ]
    )
    errors = subs.validate()
    length_errors = [e for e in errors if e.error_type == "length"]
    assert len(length_errors) >= 1


def test_custom_validation_options():
    subs = SubRipFile(
        [
            SubRipItem(1, start="00:00:01,000", end="00:00:02,000", text="Hi"),
            SubRipItem(2, start="00:00:03,000", end="00:00:04,000", text="Bye"),
        ]
    )
    # With lenient options, should pass
    errors = subs.validate(min_duration_ms=100, max_text_length=1000)
    assert errors == []

    # With strict options, should fail on duration
    errors = subs.validate(min_duration_ms=2000)
    assert len(errors) >= 1
    duration_errors = [e for e in errors if e.error_type == "duration"]
    assert len(duration_errors) >= 1
