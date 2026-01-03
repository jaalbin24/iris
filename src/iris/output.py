"""
Thread-safe output functions for terminal UI.
"""

import sys
import threading

from .colors import (
    BOLD_BLUE,
    BOLD_CYAN,
    BOLD_GREEN,
    BOLD_MAGENTA,
    BOLD_RED,
    BOLD_WHITE,
    BOLD_YELLOW,
    CYAN,
    GREEN,
    MAGENTA,
    RED,
    RESET,
    YELLOW,
)

# Thread lock for safe parallel printing
_print_lock = threading.Lock()


def _safe_print(message: str, file=None) -> None:
    """Thread-safe print function with lock."""
    with _print_lock:
        print(message, file=file if file else sys.stdout, flush=True)


def header(message: str) -> None:
    """
    Print a section header with decorative lines.

    Args:
        message: Header text to display

    Example:
        >>> header("Creating Backup")
        ═══════════════════════════════════════════════════════════════════
          Creating Backup
        ═══════════════════════════════════════════════════════════════════
    """
    output = (
        f"\n"
        f"{BOLD_BLUE}═══════════════════════════════════════════════════════════════════{RESET}\n"
        f"{BOLD_BLUE}  {message}{RESET}\n"
        f"{BOLD_BLUE}═══════════════════════════════════════════════════════════════════{RESET}\n"
    )
    _safe_print(output)


def success(message: str) -> None:
    """
    Print success message with checkmark.

    Args:
        message: Success message to display

    Example:
        >>> success("Backup complete")
        [✓] Backup complete
    """
    output = f"{BOLD_WHITE}[{BOLD_GREEN}✓{BOLD_WHITE}]{GREEN} {message}{RESET}"
    _safe_print(output)


def error(message: str) -> None:
    """
    Print error message with X mark.

    Args:
        message: Error message to display

    Example:
        >>> error("Connection failed")
        [x] Connection failed
    """
    output = f"{BOLD_WHITE}[{BOLD_RED}x{BOLD_WHITE}]{RED} {message}{RESET}"
    _safe_print(output, file=sys.stderr)


def warning(message: str) -> None:
    """
    Print warning message with exclamation mark.

    Args:
        message: Warning message to display

    Example:
        >>> warning("Disk space low")
        [!] Disk space low
    """
    output = f"{BOLD_WHITE}[{BOLD_YELLOW}!{BOLD_WHITE}]{YELLOW} {message}{RESET}"
    _safe_print(output)


def info(message: str) -> None:
    """
    Print informational message with info sign.

    Args:
        message: Info message to display

    Example:
        >>> info("Using default configuration")
        [i] Using default configuration
    """
    output = f"{BOLD_WHITE}[{BOLD_CYAN}i{BOLD_WHITE}]{CYAN} {message}{RESET}"
    _safe_print(output)


def hint(message: str) -> None:
    """
    Print a hint message with plus sign.

    Args:
        message: Hint text to display

    Example:
        >>> hint("Try: osiris --help")
        [+] Try: osiris --help
    """
    output = f"{BOLD_WHITE}[{BOLD_MAGENTA}+{BOLD_WHITE}]{MAGENTA} {message}{RESET}"
    _safe_print(output)


def command(cmd: str) -> None:
    """
    Print a command being executed.

    Args:
        cmd: Command string to display

    Example:
        >>> command("restic backup --stdin")
        [>] Running: restic backup --stdin
    """
    output = f"{BOLD_CYAN}[>] Running: {cmd}{RESET}"
    _safe_print(output)


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
        output = f"{CYAN}[DEBUG] {message}{RESET}"
        _safe_print(output, file=sys.stderr)


def secure(message: str) -> None:
    """
    Print security-related message with lock indicator.

    Args:
        message: Security message to display

    Example:
        >>> secure("Encryption key loaded")
        [S] Encryption key loaded
    """
    output = f"{BOLD_WHITE}[{BOLD_GREEN}S{BOLD_WHITE}]{GREEN} {message}{RESET}"
    _safe_print(output)


def dry_run(message: str) -> None:
    """
    Print dry-run action indicator.

    Args:
        message: Action description

    Example:
        >>> dry_run("Would delete 5 old backups")
        [DRY-RUN] Would: Would delete 5 old backups
    """
    output = f"{MAGENTA}[DRY-RUN] Would: {message}{RESET}"
    _safe_print(output)


def step(
    current: int | str, total: int | str, message: str
) -> None:
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
    output = f"{BOLD_WHITE}[{current}/{total}]{BOLD_BLUE} {message}{RESET}"
    _safe_print(output)


def duration(seconds: float) -> None:
    """
    Print elapsed time.

    Args:
        seconds: Duration in seconds

    Example:
        >>> duration(42.5)
        [TIME] Completed in 42.5s
    """
    output = f"{CYAN}[TIME] Completed in {seconds:.1f}s{RESET}"
    _safe_print(output)
