"""Subtitle file validation."""

import re
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Validation error for a subtitle item."""

    position: int
    error_type: str  # "timing", "duration", "length", "overlap", "control_char", "sequence"
    message: str


@dataclass
class ValidationOptions:
    """Configuration for subtitle validation."""

    min_subtitle_count: int = 2
    min_text_length: int = 2
    max_text_length: int = 500
    min_duration_ms: float = 500
    max_duration_secs: float = 10.0
    check_sequence: bool = True
    check_overlaps: bool = True


def validate_subtitles(subs, options=None):
    """
    Validate subtitle file integrity.

    Args:
        subs: SubRipFile instance to validate
        options: ValidationOptions instance (uses defaults if None)

    Returns:
        List of ValidationError objects (empty = valid)

    Validation checks:
    1. Minimum subtitle count
    2. Sequential position numbering (if check_sequence)
    3. Timing validity (start < end)
    4. Text length constraints
    5. Duration constraints
    6. Overlap detection (if check_overlaps)
    7. Control character detection
    """
    if options is None:
        options = ValidationOptions()

    errors = []

    # Check minimum subtitle count
    if len(subs) < options.min_subtitle_count:
        errors.append(
            ValidationError(
                position=0,
                error_type="content",
                message=f"File has only {len(subs)} subtitles, minimum is {options.min_subtitle_count}",
            )
        )
        return errors  # Can't continue validation

    prev_end = None
    for i, sub in enumerate(subs):
        position = i + 1

        # Check sequence numbering
        if options.check_sequence and sub.index != position:
            errors.append(
                ValidationError(
                    position=position,
                    error_type="sequence",
                    message=f"Expected index {position}, got {sub.index}",
                )
            )

        # Check timing validity
        if sub.start >= sub.end:
            errors.append(
                ValidationError(
                    position=position,
                    error_type="timing",
                    message=f"Start time ({sub.start}) >= end time ({sub.end})",
                )
            )

        # Check duration constraints
        duration_ms = (sub.end - sub.start).ordinal
        if duration_ms < options.min_duration_ms:
            errors.append(
                ValidationError(
                    position=position,
                    error_type="duration",
                    message=f"Duration {duration_ms}ms below minimum {options.min_duration_ms}ms",
                )
            )
        if duration_ms > options.max_duration_secs * 1000:
            errors.append(
                ValidationError(
                    position=position,
                    error_type="duration",
                    message=f"Duration {duration_ms}ms exceeds maximum {options.max_duration_secs}s",
                )
            )

        # Check text length
        text = sub.text.strip()
        if len(text) < options.min_text_length:
            errors.append(
                ValidationError(
                    position=position,
                    error_type="length",
                    message=f"Text length {len(text)} below minimum {options.min_text_length}",
                )
            )
        if len(text) > options.max_text_length:
            errors.append(
                ValidationError(
                    position=position,
                    error_type="length",
                    message=f"Text length {len(text)} exceeds maximum {options.max_text_length}",
                )
            )

        # Check for overlap with previous subtitle
        if options.check_overlaps and prev_end is not None and sub.start < prev_end:
            overlap_ms = (prev_end - sub.start).ordinal
            errors.append(
                ValidationError(
                    position=position,
                    error_type="overlap",
                    message=f"Overlaps with previous subtitle by {overlap_ms}ms",
                )
            )

        # Check for control characters (except common ones like \n, \r, \t)
        if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", text):
            errors.append(
                ValidationError(
                    position=position,
                    error_type="control_char",
                    message="Contains invalid control characters",
                )
            )

        prev_end = sub.end

    return errors
