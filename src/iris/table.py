"""
Table rendering for terminal output.
"""

import re

from ._console import _get_console
from .colors import BOLD_WHITE, RESET
from .semantic import Semantic, apply_semantic

# Regex to match ANSI escape codes
_ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text for width calculation."""
    return _ANSI_PATTERN.sub("", text)


class Table:
    """
    Simple table renderer for terminal output.

    Example:
        >>> table = Table(["Name", "Status", "Size"])
        >>> table.add_row("backup-01", "OK", "2.3 GB")
        >>> table.add_row("backup-02", "OK", "1.8 GB")
        >>> table.render()
        Name       Status   Size
        ─────────────────────────────
        backup-01  OK       2.3 GB
        backup-02  OK       1.8 GB

    With semantic coloring:
        >>> from iris import Semantic
        >>> table = Table(["Host", "Status"])
        >>> table.set_column_semantics(1, {
        ...     "running": Semantic.SUCCESS,
        ...     "stopped": Semantic.WARNING,
        ... })
        >>> table.add_row("web-01", "running")
        >>> table.render()  # "running" will be green
    """

    def __init__(self, columns: list[str]):
        """
        Initialize a table with column headers.

        Args:
            columns: List of column header names
        """
        self._columns = columns
        self._rows: list[list[str]] = []
        self._column_semantics: dict[int, dict[str, Semantic]] = {}

    def set_column_semantics(
        self, column: int, mapping: dict[str, Semantic]
    ) -> None:
        """
        Set semantic coloring for values in a column.

        Args:
            column: Column index (0-based)
            mapping: Dict mapping cell values to Semantic enum values

        Example:
            >>> table.set_column_semantics(1, {
            ...     "running": Semantic.SUCCESS,
            ...     "stopped": Semantic.WARNING,
            ...     "error": Semantic.ERROR,
            ... })
        """
        self._column_semantics[column] = mapping

    def add_row(self, *values: str) -> None:
        """
        Add a row of values to the table.

        Args:
            *values: Values for each column

        Raises:
            ValueError: If number of values doesn't match columns
        """
        if len(values) != len(self._columns):
            raise ValueError(f"Expected {len(self._columns)} values, got {len(values)}")
        self._rows.append(list(values))

    def _apply_semantics(self, col: int, value: str) -> str:
        """Apply semantic coloring to a cell value if configured."""
        if col in self._column_semantics:
            semantic = self._column_semantics[col].get(value)
            if semantic:
                return apply_semantic(value, semantic)
        return value

    def _calculate_widths(self) -> list[int]:
        """Calculate the width needed for each column."""
        widths = [len(col) for col in self._columns]
        for row in self._rows:
            for i, value in enumerate(row):
                # Use stripped length for width calculation
                visible_len = len(_strip_ansi(str(value)))
                widths[i] = max(widths[i], visible_len)
        return widths

    def render(self) -> None:
        """Print the table to stdout."""
        widths = self._calculate_widths()
        total_width = sum(widths) + (len(widths) - 1) * 2  # 2 spaces between columns

        # Header row
        header_parts = []
        for i, col in enumerate(self._columns):
            header_parts.append(f"{BOLD_WHITE}{col:<{widths[i]}}{RESET}")
        header = "  ".join(header_parts)

        # Separator line
        separator = "─" * total_width

        # Data rows
        data_lines = []
        for row in self._rows:
            row_parts = []
            for i, value in enumerate(row):
                # Apply semantic coloring
                colored_value = self._apply_semantics(i, str(value))
                # Calculate padding based on visible length
                visible_len = len(_strip_ansi(colored_value))
                padding = widths[i] - visible_len
                row_parts.append(colored_value + " " * padding)
            data_lines.append("  ".join(row_parts))

        # Print with thread safety
        with _get_console()._lock:
            print(header, flush=True)
            print(separator, flush=True)
            for line in data_lines:
                print(line, flush=True)

    def render_to_string(self) -> str:
        """
        Render the table to a string instead of printing.

        Note: Colors are not included in string output.

        Returns:
            The formatted table as a string
        """
        widths = self._calculate_widths()
        total_width = sum(widths) + (len(widths) - 1) * 2

        lines = []

        # Header row (without colors for string output)
        header_parts = [f"{col:<{widths[i]}}" for i, col in enumerate(self._columns)]
        lines.append("  ".join(header_parts))

        # Separator
        lines.append("─" * total_width)

        # Data rows (without colors)
        for row in self._rows:
            row_parts = [f"{value!s:<{widths[i]}}" for i, value in enumerate(row)]
            lines.append("  ".join(row_parts))

        return "\n".join(lines)
