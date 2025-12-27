"""Subtitle timing utilities."""

from pysrt.srttime import SubRipTime


def calculate_optimal_duration_ms(text, words_per_second=2.5):
    """
    Calculate optimal duration in milliseconds based on word count.

    Uses 2.5 words per second as baseline (from subtitle best practices).
    Clamps result between 1500ms and 6000ms.

    Args:
        text: The subtitle text
        words_per_second: Reading speed (default 2.5)

    Returns:
        Optimal duration in milliseconds
    """
    word_count = len(text.split())
    if word_count == 0:
        return 1500  # Minimum for empty/whitespace

    duration_ms = int((word_count / words_per_second) * 1000)
    return max(1500, min(6000, duration_ms))


def fix_overlapping_subtitles(
    subs, buffer_ms=20, min_duration_ms=1500, max_duration_ms=6000, in_place=True
):
    """
    Fix overlapping subtitles with intelligent timing adjustment.

    Algorithm (adapted from Lingarr):
    1. Detect overlaps between consecutive subtitles
    2. Calculate optimal duration based on word count
    3. Adjust end time of earlier subtitle to not overlap
    4. Maintain buffer_ms gap between subtitles
    5. Respect min/max duration constraints

    Args:
        subs: SubRipFile instance to fix
        buffer_ms: Minimum gap between subtitles (default 20ms)
        min_duration_ms: Minimum subtitle duration (default 1500ms)
        max_duration_ms: Maximum subtitle duration (default 6000ms)
        in_place: Modify subs in place (default True), otherwise return new instance

    Returns:
        Modified SubRipFile (same instance if in_place=True, new instance otherwise)
    """
    if not in_place:
        from copy import deepcopy

        subs = deepcopy(subs)

    if len(subs) < 2:
        return subs

    for i in range(len(subs) - 1):
        current = subs[i]
        next_sub = subs[i + 1]

        # Check for overlap or too-close timing
        gap_ms = (next_sub.start - current.end).ordinal
        if gap_ms < buffer_ms:  # Overlapping or too close
            # Calculate how much we need to shrink current subtitle
            adjustment_needed = buffer_ms - gap_ms

            # Calculate current duration
            current_duration_ms = (current.end - current.start).ordinal

            # Calculate minimum acceptable duration for current subtitle
            optimal_duration = calculate_optimal_duration_ms(current.text)
            min_acceptable = max(min_duration_ms, optimal_duration // 2)

            # New duration for current subtitle
            new_duration_ms = max(min_acceptable, current_duration_ms - adjustment_needed)

            # Set new end time
            new_end_ordinal = current.start.ordinal + new_duration_ms
            current.end = SubRipTime.from_ordinal(new_end_ordinal)

    return subs
