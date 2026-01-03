"""
ANSI color codes for terminal output.
"""


class Colors:
    """ANSI color codes for terminal output."""

    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    MAGENTA = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"

    BOLD_RED = "\033[1;31m"
    BOLD_GREEN = "\033[1;32m"
    BOLD_YELLOW = "\033[1;33m"
    BOLD_BLUE = "\033[1;34m"
    BOLD_MAGENTA = "\033[1;35m"
    BOLD_CYAN = "\033[1;36m"
    BOLD_WHITE = "\033[1;37m"

    RESET = "\033[0m"


# Module-level exports for convenience
RED = Colors.RED
GREEN = Colors.GREEN
YELLOW = Colors.YELLOW
BLUE = Colors.BLUE
MAGENTA = Colors.MAGENTA
CYAN = Colors.CYAN
WHITE = Colors.WHITE
BOLD_RED = Colors.BOLD_RED
BOLD_GREEN = Colors.BOLD_GREEN
BOLD_YELLOW = Colors.BOLD_YELLOW
BOLD_BLUE = Colors.BOLD_BLUE
BOLD_MAGENTA = Colors.BOLD_MAGENTA
BOLD_CYAN = Colors.BOLD_CYAN
BOLD_WHITE = Colors.BOLD_WHITE
RESET = Colors.RESET
