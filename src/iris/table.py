"""
Table rendering for terminal output.
"""

import sys
import threading

from .colors import BOLD_WHITE, RESET

# Thread lock for safe parallel printing
_print_lock = threading.Lock()


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
    """

    def __init__(self, columns: list[str]):
        """
        Initialize a table with column headers.

        Args:
            columns: List of column header names
        """
        self._columns = columns
        self._rows: list[list[str]] = []

    def add_row(self, *values: str) -> None:
        """
        Add a row of values to the table.

        Args:
            *values: Values for each column

        Raises:
            ValueError: If number of values doesn't match columns
        """
        if len(values) != len(self._columns):
            raise ValueError(
                f"Expected {len(self._columns)} values, got {len(values)}"
            )
        self._rows.append(list(values))

    def _calculate_widths(self) -> list[int]:
        """Calculate the width needed for each column."""
        widths = [len(col) for col in self._columns]
        for row in self._rows:
            for i, value in enumerate(row):
                widths[i] = max(widths[i], len(str(value)))
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
                row_parts.append(f"{str(value):<{widths[i]}}")
            data_lines.append("  ".join(row_parts))

        # Print with thread safety
        with _print_lock:
            print(header, flush=True)
            print(separator, flush=True)
            for line in data_lines:
                print(line, flush=True)

    def render_to_string(self) -> str:
        """
        Render the table to a string instead of printing.

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

        # Data rows
        for row in self._rows:
            row_parts = [f"{str(value):<{widths[i]}}" for i, value in enumerate(row)]
            lines.append("  ".join(row_parts))

        return "\n".join(lines)
