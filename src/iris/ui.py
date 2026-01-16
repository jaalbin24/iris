"""
Stateful UI context for CLI applications.
"""

import sys
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from typing import ClassVar

from . import output
from . import prompts as prompts_module
from ._console import _get_console
from .colors import (
    CLEAR_LINE,
    CURSOR_HIDE,
    CURSOR_SHOW,
    CURSOR_UP,
    RESET,
)
from .semantic import SEMANTIC_COLORS, Semantic
from .table import Table


class ProgressContext:
    """
    Context for tracking multi-step operations.

    Used with UI.progress() context manager.
    """

    def __init__(self, steps: list[str], ui: "UI"):
        self._steps = steps
        self._ui = ui
        self._current_index = 0
        self._completed: dict[str, str] = {}  # step -> status message

    def start(self, step: str) -> None:
        """
        Mark a step as starting.

        Args:
            step: Name of the step (must be in the steps list)
        """
        if step not in self._steps:
            raise ValueError(f"Unknown step: {step}")

        self._current_index = self._steps.index(step)
        output.step(
            self._current_index + 1,
            len(self._steps),
            f"{step}...",
        )

    def complete(self, step: str, status: str = "") -> None:
        """
        Mark a step as complete.

        Args:
            step: Name of the step
            status: Optional status message (e.g., "1.2 GB")
        """
        self._completed[step] = status
        if status:
            output.success(f"{step} complete ({status})")
        else:
            output.success(f"{step} complete")

    def fail(self, step: str, error: str = "") -> None:
        """
        Mark a step as failed.

        Args:
            step: Name of the step
            error: Optional error message
        """
        if error:
            output.error(f"{step} failed: {error}")
        else:
            output.error(f"{step} failed")


class StatusListContext:
    """
    Context for live-updating status list.

    Displays multiple items with status indicators that update in place.
    Used with UI.status_list() context manager.

    Example:
        >>> with ui.status_list(["vm-web", "vm-db"]) as status:
        ...     status.update("vm-web", "running")
        ...     status.update("vm-web", "success", detail="10.0.0.5")
    """

    STATES: ClassVar[set[str]] = {
        "pending",
        "running",
        "success",
        "error",
        "warning",
        "skipped",
    }
    SPINNER_FRAMES: ClassVar[str] = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    ICONS: ClassVar[dict[str, str]] = {
        "pending": "○",
        "success": "✓",
        "error": "✘",
        "warning": "!",
        "skipped": "⊘",
    }
    STATE_SEMANTICS: ClassVar[dict[str, Semantic]] = {
        "pending": Semantic.MUTED,
        "running": Semantic.INFO,
        "success": Semantic.SUCCESS,
        "error": Semantic.ERROR,
        "warning": Semantic.WARNING,
        "skipped": Semantic.MUTED,
    }

    def __init__(self, items: list[str], ui: "UI"):
        """
        Initialize status list context.

        Args:
            items: List of item names to track
            ui: Parent UI instance
        """
        self._items = items
        self._ui = ui
        self._states: dict[str, str] = {item: "pending" for item in items}
        self._details: dict[str, str] = {}
        self._spinner_index = 0
        self._spinner_thread: threading.Thread | None = None
        self._stop_spinner = threading.Event()
        self._is_tty = sys.stdout.isatty()
        self._rendered = False
        self._max_item_width = max(len(item) for item in items) if items else 0

    def update(self, item: str, state: str, detail: str = "") -> None:
        """
        Update an item's state.

        Args:
            item: Name of the item (must be in the items list)
            state: New state (pending, running, success, error, warning, skipped)
            detail: Optional detail string (e.g., IP address, error message)

        Raises:
            ValueError: If item is unknown or state is invalid
        """
        if item not in self._states:
            raise ValueError(f"Unknown item: {item}")
        if state not in self.STATES:
            raise ValueError(f"Invalid state: {state}. Must be one of {self.STATES}")

        self._states[item] = state
        if detail:
            self._details[item] = detail
        elif item in self._details and state != "running":
            # Clear detail when state changes (except for running)
            pass  # Keep existing detail

        if self._is_tty:
            self._render_all()
        else:
            # Non-TTY: print each state change as a new line
            line = self._render_line(item)
            with _get_console()._lock:
                print(line, flush=True)

    def _render_all(self) -> None:
        """Redraw all lines (TTY mode only)."""
        with _get_console()._lock:
            # Move cursor up if we've rendered before
            if self._rendered:
                print(CURSOR_UP.format(len(self._items)), end="", flush=True)

            # Clear and reprint each line
            for item in self._items:
                line = self._render_line(item)
                print(f"{CLEAR_LINE}\r{line}", flush=True)

            self._rendered = True

    def _render_line(self, item: str) -> str:
        """Format a single status line."""
        state = self._states[item]
        semantic = self.STATE_SEMANTICS[state]
        color = SEMANTIC_COLORS[semantic]

        # Get icon (spinner for running state)
        if state == "running":
            icon = self.SPINNER_FRAMES[self._spinner_index]
        else:
            icon = self.ICONS[state]

        # Build line with consistent formatting
        detail = self._details.get(item, "")
        if detail:
            if state == "error":
                detail_str = f": {detail}"
            else:
                detail_str = f"  ({detail})"
        else:
            detail_str = ""

        return f"{color}{icon}{RESET} {item:<{self._max_item_width}}  {color}{state}{RESET}{detail_str}"

    def _start_spinner(self) -> None:
        """Start background spinner animation thread."""
        if not self._is_tty:
            return

        # Hide cursor during animation
        with _get_console()._lock:
            print(CURSOR_HIDE, end="", flush=True)

        self._spinner_thread = threading.Thread(target=self._spinner_loop, daemon=True)
        self._spinner_thread.start()

    def _stop_spinner_thread(self) -> None:
        """Stop spinner thread and show cursor."""
        self._stop_spinner.set()
        if self._spinner_thread is not None:
            self._spinner_thread.join(timeout=0.2)

        if self._is_tty:
            # Show cursor and do final render
            with _get_console()._lock:
                print(CURSOR_SHOW, end="", flush=True)

    def _spinner_loop(self) -> None:
        """Background thread: update spinner frame every 80ms."""
        while not self._stop_spinner.wait(0.08):
            # Check if any items are in running state
            has_running = any(s == "running" for s in self._states.values())
            if has_running:
                self._spinner_index = (self._spinner_index + 1) % len(
                    self.SPINNER_FRAMES
                )
                self._render_all()


class UI:
    """
    Stateful UI context for CLI applications.

    Manages non-interactive mode, verbosity, and scoped operations.

    Example:
        >>> ui = UI(interactive=True, verbose=True)
        >>> ui.header("Creating Backup")
        >>> with ui.progress(["PostgreSQL", "MinIO"]) as p:
        ...     p.start("PostgreSQL")
        ...     # do backup
        ...     p.complete("PostgreSQL", "1.2 GB")
    """

    def __init__(
        self,
        interactive: bool = True,
        verbose: bool = False,
        debug: bool = False,
    ):
        """
        Initialize UI context.

        Args:
            interactive: If False, skip prompts and use defaults
            verbose: If True, show additional output (commands, etc.)
            debug: If True, show debug messages
        """
        self.interactive = interactive
        self.verbose = verbose
        self._debug = debug

    # Output methods - delegate to output module
    def header(self, message: str) -> None:
        """Print a section header."""
        output.header(message)

    def success(self, message: str) -> None:
        """Print a success message."""
        output.success(message)

    def error(self, message: str) -> None:
        """Print an error message."""
        output.error(message)

    def warning(self, message: str) -> None:
        """Print a warning message."""
        output.warning(message)

    def info(self, message: str) -> None:
        """Print an info message."""
        output.info(message)

    def hint(self, message: str) -> None:
        """Print a hint message."""
        output.hint(message)

    def command(self, cmd: str) -> None:
        """Print a command being executed (only if verbose)."""
        if self.verbose:
            output.command(cmd)

    def debug(self, message: str) -> None:
        """Print a debug message (only if debug mode enabled)."""
        output.debug(message, enabled=self._debug)

    def secure(self, message: str) -> None:
        """Print a security-related message."""
        output.secure(message)

    def dry_run(self, message: str) -> None:
        """Print a dry-run action."""
        output.dry_run(message)

    def step(self, current: int, total: int, message: str) -> None:
        """Print a workflow step indicator."""
        output.step(current, total, message)

    def duration(self, seconds: float) -> None:
        """Print elapsed time."""
        output.duration(seconds)

    def danger_banner(self, message: str) -> None:
        """Print a danger banner with red background."""
        output.danger_banner(message)

    # Prompt methods - respect interactive mode
    def confirm(self, message: str, default: bool = False) -> bool:
        """
        Ask a yes/no question.

        Returns default immediately if non-interactive.
        """
        if not self.interactive:
            return default
        return prompts_module.confirm(message, default)

    def prompt(self, message: str, mask: bool = False, default: str = "") -> str:
        """
        Ask for text input.

        Returns default immediately if non-interactive.
        """
        if not self.interactive:
            return default
        return prompts_module.prompt(message, mask, default)

    def prompt_choice(self, message: str, choices: list[str], default: int = 0) -> int:
        """
        Ask user to choose from options.

        Returns default immediately if non-interactive.
        """
        if not self.interactive:
            return default
        return prompts_module.prompt_choice(message, choices, default)

    # Progress tracking
    @contextmanager
    def progress(self, steps: list[str]) -> Iterator[ProgressContext]:
        """
        Context manager for multi-step operations.

        Args:
            steps: List of step names

        Yields:
            ProgressContext for tracking step completion

        Example:
            >>> with ui.progress(["PostgreSQL", "MinIO"]) as p:
            ...     p.start("PostgreSQL")
            ...     do_postgres_backup()
            ...     p.complete("PostgreSQL", "1.2 GB")
        """
        ctx = ProgressContext(steps, self)
        yield ctx

    @contextmanager
    def status_list(self, items: list[str]) -> Iterator[StatusListContext]:
        """
        Context manager for live-updating status list.

        Displays multiple items with status indicators that update in place.
        In TTY mode, lines are redrawn. In non-TTY mode, each state change
        prints a new line.

        Args:
            items: List of item names to track

        Yields:
            StatusListContext for updating item states

        Example:
            >>> with ui.status_list(["vm-web", "vm-db"]) as status:
            ...     status.update("vm-web", "running")
            ...     do_work()
            ...     status.update("vm-web", "success", detail="10.0.0.5")
        """
        ctx = StatusListContext(items, self)
        ctx._render_all()
        ctx._start_spinner()
        try:
            yield ctx
        finally:
            ctx._stop_spinner_thread()

    # Table helper
    def table(self, columns: list[str]) -> Table:
        """
        Create a new table with the given columns.

        Args:
            columns: List of column header names

        Returns:
            A Table instance
        """
        return Table(columns)
