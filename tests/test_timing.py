import pytest

from pysrt import SubRipFile, SubRipItem
from pysrt.timing import calculate_optimal_duration_ms


def test_optimal_duration_calculation():
    # 10 words at 2.5 words/sec = 4000ms
    text = "one two three four five six seven eight nine ten"
    duration = calculate_optimal_duration_ms(text)
    assert duration == 4000


def test_optimal_duration_clamps_min():
    # 1 word should clamp to 1500ms minimum
    duration = calculate_optimal_duration_ms("word")
    assert duration == 1500


def test_optimal_duration_clamps_max():
    # 20 words would be 8000ms, but clamped to 6000ms
    text = " ".join(["word"] * 20)
    duration = calculate_optimal_duration_ms(text)
    assert duration == 6000


def test_fix_overlaps_non_overlapping_unchanged():
    subs = SubRipFile(
        [
            SubRipItem(1, start="00:00:01,000", end="00:00:03,000", text="First"),
            SubRipItem(2, start="00:00:04,000", end="00:00:06,000", text="Second"),
        ]
    )
    original_end = subs[0].end
    subs.fix_overlaps()
    assert subs[0].end == original_end  # Should be unchanged


def test_fix_overlaps_fixes_overlap():
    subs = SubRipFile(
        [
            SubRipItem(1, start="00:00:01,000", end="00:00:05,000", text="First subtitle"),
            SubRipItem(2, start="00:00:04,000", end="00:00:06,000", text="Overlapping"),
        ]
    )
    subs.fix_overlaps(buffer_ms=20)

    # After fixing, first subtitle should end before second starts (with buffer)
    gap_ms = (subs[1].start - subs[0].end).ordinal
    assert gap_ms >= 20


def test_fix_overlaps_returns_self():
    subs = SubRipFile(
        [
            SubRipItem(1, start="00:00:01,000", end="00:00:03,000", text="First"),
            SubRipItem(2, start="00:00:04,000", end="00:00:06,000", text="Second"),
        ]
    )
    result = subs.fix_overlaps()
    assert result is subs  # Should return self for method chaining


def test_fix_overlaps_close_timing():
    subs = SubRipFile(
        [
            SubRipItem(1, start="00:00:01,000", end="00:00:03,000", text="First"),
            SubRipItem(2, start="00:00:03,010", end="00:00:05,000", text="Too close"),
        ]
    )
    subs.fix_overlaps(buffer_ms=20)

    # Should adjust to have at least 20ms buffer
    gap_ms = (subs[1].start - subs[0].end).ordinal
    assert gap_ms >= 20
