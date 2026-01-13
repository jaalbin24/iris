"""
Thread-safe output functions for terminal UI.
"""

from ._console import _get_console


def header(message: str) -> None:
    """
    Print a section header with decorative lines spanning terminal width.

    Args:
        message: Header text to display

    Example:
        >>> header("Creating Backup")
        ════════════════════════════════════════════════════════════════════════════════
          Creating Backup
        ════════════════════════════════════════════════════════════════════════════════
    """
    _get_console().header(message)


def success(message: str) -> None:
    """
    Print success message with checkmark.

    Args:
        message: Success message to display

    Example:
        >>> success("Backup complete")
        [✓] Backup complete
    """
    _get_console().success(message)


def error(message: str) -> None:
    """
    Print error message with X mark.

    Args:
        message: Error message to display

    Example:
        >>> error("Connection failed")
        [x] Connection failed
    """
    _get_console().error(message)


def warning(message: str) -> None:
    """
    Print warning message with exclamation mark.

    Args:
        message: Warning message to display

    Example:
        >>> warning("Disk space low")
        [!] Disk space low
    """
    _get_console().warning(message)


def info(message: str) -> None:
    """
    Print informational message with info sign.

    Args:
        message: Info message to display

    Example:
        >>> info("Using default configuration")
        [i] Using default configuration
    """
    _get_console().info(message)


def hint(message: str) -> None:
    """
    Print a hint message with plus sign.

    Args:
        message: Hint text to display

    Example:
        >>> hint("Try: osiris --help")
        [+] Try: osiris --help
    """
    _get_console().hint(message)


def command(cmd: str) -> None:
    """
    Print a command being executed.

    Args:
        cmd: Command string to display

    Example:
        >>> command("restic backup --stdin")
        [>] Running: restic backup --stdin
    """
    _get_console().command(cmd)


def debug(message: str, enabled: bool = False) -> None:
    """
    Print debug message (only if enabled).

    Args:
        message: Debug message to display
        enabled: Whether debug mode is active

    Example:
        >>> debug("Variable value: foo", enabled=True)
        [DEBUG] Variable value: foo
    """
    if enabled:
        _get_console().debug(message)


def secure(message: str) -> None:
    """
    Print security-related message with lock indicator.

    Args:
        message: Security message to display

    Example:
        >>> secure("Encryption key loaded")
        [S] Encryption key loaded
    """
    _get_console().secure(message)


def dry_run(message: str) -> None:
    """
    Print dry-run action indicator.

    Args:
        message: Action description

    Example:
        >>> dry_run("Would delete 5 old backups")
        [DRY-RUN] Would: Would delete 5 old backups
    """
    _get_console().dry_run(message)


def step(current: int | str, total: int | str, message: str) -> None:
    """
    Print workflow step indicator.

    Args:
        current: Current step number
        total: Total number of steps
        message: Step description

    Example:
        >>> step(1, 3, "Backing up PostgreSQL")
        [1/3] Backing up PostgreSQL
    """
    _get_console().step(current, total, message)


def duration(seconds: float) -> None:
    """
    Print elapsed time.

    Args:
        seconds: Duration in seconds

    Example:
        >>> duration(42.5)
        [TIME] Completed in 42.5s
    """
    _get_console().duration(seconds)


def box(message: str, bg_color: str = "", fg_color: str = "") -> None:
    """
    Print a full-width box with double-line borders.

    Args:
        message: Text to display (supports multi-line via newlines).
        bg_color: Background ANSI code (e.g., BG_RED). Empty for no background.
        fg_color: Foreground ANSI code. Defaults to bold white.

    Example:
        >>> box("ALERT")
        ╔════════════════════════════════════════════╗
        ║                   ALERT                    ║
        ╚════════════════════════════════════════════╝

        >>> box("WARNING", bg_color=BG_RED)
        # Same but with red background
    """
    from .colors import BOLD_WHITE

    _get_console().box(message, bg_color, fg_color if fg_color else BOLD_WHITE)


def danger_banner(message: str) -> None:
    """
    Print a full-width danger banner with red background and border.

    Args:
        message: Message to display. Supports multi-line via newlines.

    Example:
        >>> danger_banner("ALL HOSTS TARGETED")
        # Outputs red bordered banner spanning terminal width

        >>> danger_banner("WARNING\\nThis cannot be undone")
        # Outputs multi-line red bordered banner
    """
    _get_console().danger_banner(message)
