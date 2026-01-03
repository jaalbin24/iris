"""
Stateful UI context for CLI applications.
"""

from collections.abc import Iterator
from contextlib import contextmanager

from . import output
from . import prompts as prompts_module
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

    def prompt_choice(
        self, message: str, choices: list[str], default: int = 0
    ) -> int:
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
