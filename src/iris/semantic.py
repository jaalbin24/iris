"""
Semantic color system for consistent UX across CLI tools.

This module defines the semantic categories used for coloring output.
Tools should use these semantics instead of raw colors to ensure
consistent meaning across all Iris-based applications.
"""

from enum import Enum

from .colors import (
    BOLD_CYAN,
    BOLD_GREEN,
    BOLD_MAGENTA,
    BOLD_RED,
    BOLD_YELLOW,
    RESET,
    WHITE,
)


class Semantic(Enum):
    """Semantic categories for colored output.

    Each semantic has a defined meaning and associated color:
    - SUCCESS: Good, healthy, complete (green)
    - ERROR: Problem, failure (red)
    - WARNING: Attention needed, degraded (yellow)
    - INFO: Neutral information (cyan)
    - HINT: Suggestions, tips (magenta)
    - MUTED: Inactive, not applicable (white/dim)
    """

    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"
    MUTED = "muted"


SEMANTIC_COLORS: dict[Semantic, str] = {
    Semantic.SUCCESS: BOLD_GREEN,
    Semantic.ERROR: BOLD_RED,
    Semantic.WARNING: BOLD_YELLOW,
    Semantic.INFO: BOLD_CYAN,
    Semantic.HINT: BOLD_MAGENTA,
    Semantic.MUTED: WHITE,
}


def apply_semantic(text: str, semantic: Semantic) -> str:
    """Wrap text with semantic color.

    Args:
        text: The text to color
        semantic: The semantic category to apply

    Returns:
        Text wrapped with appropriate ANSI color codes
    """
    color = SEMANTIC_COLORS[semantic]
    return f"{color}{text}{RESET}"
