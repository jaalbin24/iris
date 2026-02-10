"""
Internal console class for thread-safe terminal I/O.

This module is private and should not be imported directly by external code.
"""

import getpass
import shutil
import sys
import threading
from typing import IO

from .colors import (
    BG_RED,
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


class _Console:
    """
    Internal console class that manages all terminal I/O with a single lock.

    This class is not part of the public API. External code should use the
    functions in output.py, prompts.py, etc.
    """

    def __init__(self):
        self._lock = threading.RLock()

    def _print(self, message: str, file: IO[str] | None = None) -> None:
        """Thread-safe print with lock."""
        with self._lock:
            print(message, file=file or sys.stdout, flush=True)

    # =========================================================================
    # Output Methods
    # =========================================================================

    def header(self, message: str) -> None:
        """Print a section header with decorative lines spanning terminal width."""
        width = shutil.get_terminal_size().columns
        line = "═" * width
        output = (
            f"\n"
            f"{BOLD_BLUE}{line}{RESET}\n"
            f"{BOLD_BLUE}  {message}{RESET}\n"
            f"{BOLD_BLUE}{line}{RESET}\n"
        )
        self._print(output)

    def success(self, message: str) -> None:
        """Print success message with checkmark."""
        output = f"{BOLD_WHITE}[{BOLD_GREEN}✓{BOLD_WHITE}]{GREEN} {message}{RESET}"
        self._print(output)

    def error(self, message: str) -> None:
        """Print error message with X mark."""
        output = f"{BOLD_WHITE}[{BOLD_RED}x{BOLD_WHITE}]{RED} {message}{RESET}"
        self._print(output, file=sys.stderr)

    def warning(self, message: str) -> None:
        """Print warning message with exclamation mark."""
        output = f"{BOLD_WHITE}[{BOLD_YELLOW}!{BOLD_WHITE}]{YELLOW} {message}{RESET}"
        self._print(output)

    def info(self, message: str) -> None:
        """Print informational message with info sign."""
        output = f"{BOLD_WHITE}[{BOLD_CYAN}i{BOLD_WHITE}]{CYAN} {message}{RESET}"
        self._print(output)

    def hint(self, message: str) -> None:
        """Print a hint message with plus sign."""
        output = f"{BOLD_WHITE}[{BOLD_MAGENTA}+{BOLD_WHITE}]{MAGENTA} {message}{RESET}"
        self._print(output)

    def command(self, cmd: str) -> None:
        """Print a command being executed."""
        output = f"{BOLD_CYAN}[>] Running: {cmd}{RESET}"
        self._print(output)

    def debug(self, message: str) -> None:
        """Print debug message."""
        output = f"{CYAN}[DEBUG] {message}{RESET}"
        self._print(output, file=sys.stderr)

    def secure(self, message: str) -> None:
        """Print security-related message with lock indicator."""
        output = f"{BOLD_WHITE}[{BOLD_GREEN}S{BOLD_WHITE}]{GREEN} {message}{RESET}"
        self._print(output)

    def dry_run(self, message: str) -> None:
        """Print dry-run action indicator."""
        output = f"{MAGENTA}[DRY-RUN] Would: {message}{RESET}"
        self._print(output)

    def step(self, current: int | str, total: int | str, message: str) -> None:
        """Print workflow step indicator."""
        output = f"{BOLD_WHITE}[{current}/{total}]{BOLD_BLUE} {message}{RESET}"
        self._print(output)

    def duration(self, seconds: float) -> None:
        """Print elapsed time."""
        output = f"{CYAN}[TIME] Completed in {seconds:.1f}s{RESET}"
        self._print(output)

    def box(self, message: str, bg_color: str = "", fg_color: str = BOLD_WHITE) -> None:
        """Print a full-width box with double-line borders."""
        width = shutil.get_terminal_size().columns
        lines = message.split("\n")
        style = f"{bg_color}{fg_color}"

        inner_width = width - 2
        output_lines = []

        output_lines.append(f"{style}╔{'═' * inner_width}╗{RESET}")
        for line in lines:
            output_lines.append(f"{style}║{line.center(inner_width)}║{RESET}")
        output_lines.append(f"{style}╚{'═' * inner_width}╝{RESET}")

        self._print("\n".join(output_lines))

    def danger_banner(self, message: str) -> None:
        """Print a full-width danger banner with red background and border."""
        self.box(message, bg_color=BG_RED)

    # =========================================================================
    # Prompt Methods
    # =========================================================================

    def confirm(self, message: str, default: bool = False) -> bool:
        """Ask a yes/no question."""
        if default:
            prompt_suffix = "[Y/n]"
        else:
            prompt_suffix = "[y/N]"

        prompt_text = (
            f"{BOLD_WHITE}[{BOLD_YELLOW}?{BOLD_WHITE}]{YELLOW} "
            f"{message} {prompt_suffix}: {RESET}"
        )

        with self._lock:
            print(prompt_text, end="", file=sys.stdout, flush=True)

        try:
            response = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return default

        if response == "":
            return default
        elif response in ("y", "yes"):
            return True
        elif response in ("n", "no"):
            return False
        else:
            return default

    def prompt(self, message: str, mask: bool = False, default: str = "") -> str:
        """Ask for text input."""
        prompt_text = (
            f"{BOLD_WHITE}[{BOLD_YELLOW}?{BOLD_WHITE}]{YELLOW} {message}: {RESET}"
        )

        with self._lock:
            print(prompt_text, end="", file=sys.stdout, flush=True)

        try:
            if mask:
                response = getpass.getpass(prompt="")
            else:
                response = input()
        except (EOFError, KeyboardInterrupt):
            print()
            return default

        if response == "":
            return default

        return response

    def prompt_choice(self, message: str, choices: list[str], default: int = 0) -> int:
        """Ask user to choose from a list of options."""
        prompt_header = (
            f"{BOLD_WHITE}[{BOLD_YELLOW}?{BOLD_WHITE}]{YELLOW} {message}{RESET}"
        )

        with self._lock:
            print(prompt_header, file=sys.stdout, flush=True)
            for i, choice in enumerate(choices):
                marker = "*" if i == default else " "
                print(f"   {marker}{i + 1}) {choice}", file=sys.stdout, flush=True)
            print(
                f"{YELLOW}Choice [{default + 1}]: {RESET}",
                end="",
                file=sys.stdout,
                flush=True,
            )

        try:
            response = input().strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return default

        if response == "":
            return default

        try:
            idx = int(response) - 1
            if 0 <= idx < len(choices):
                return idx
            return default
        except ValueError:
            return default


# =============================================================================
# Singleton Management
# =============================================================================

_instance: _Console | None = None


def _get_console() -> _Console:
    """Get the singleton console instance."""
    global _instance
    if _instance is None:
        _instance = _Console()
    return _instance
