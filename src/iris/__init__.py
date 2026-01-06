"""
Iris - Terminal UI library for CLI tools.

Provides consistent formatting, colors, and output functions for
Python CLI applications.

Example (stateless):
    >>> from iris import header, success, error, info
    >>> header("Creating Backup")
    >>> info("Running: pg_dump ...")
    >>> success("Backup complete")

Example (stateful):
    >>> from iris import UI
    >>> ui = UI(interactive=True, verbose=True)
    >>> ui.header("Creating Backup")
    >>> if ui.confirm("Continue?"):
    ...     ui.success("Done")
"""

# Stateless output functions
# Colors (for advanced usage)
from .colors import Colors
from .output import (
    command,
    debug,
    dry_run,
    duration,
    error,
    header,
    hint,
    info,
    secure,
    step,
    success,
    warning,
)

# User prompts
from .prompts import confirm, prompt, prompt_choice

# Table rendering
from .table import Table

# Stateful UI class
from .ui import UI, StatusListContext

# Utilities
from .utils import format_age, format_duration, format_size

__version__ = "1.0.0"

__all__ = [
    # Output functions
    "header",
    "success",
    "error",
    "warning",
    "info",
    "hint",
    "command",
    "debug",
    "secure",
    "dry_run",
    "step",
    "duration",
    # Classes
    "UI",
    "StatusListContext",
    "Table",
    "Colors",
    # Prompts
    "confirm",
    "prompt",
    "prompt_choice",
    # Utils
    "format_duration",
    "format_size",
    "format_age",
]
