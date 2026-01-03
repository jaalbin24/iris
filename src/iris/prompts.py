"""
User input prompts for terminal UI.
"""

import getpass
import threading

from .colors import BOLD_WHITE, BOLD_YELLOW, RESET, YELLOW

# Thread lock for safe parallel printing
_print_lock = threading.Lock()


def confirm(message: str, default: bool = False) -> bool:
    """
    Ask a yes/no question.

    Args:
        message: Question to ask
        default: Default answer if user presses Enter

    Returns:
        True for yes, False for no

    Example:
        >>> if confirm("Continue with restore?", default=False):
        ...     do_restore()
        [?] Continue with restore? [y/N]: y
    """
    if default:
        prompt_suffix = "[Y/n]"
    else:
        prompt_suffix = "[y/N]"

    prompt_text = (
        f"{BOLD_WHITE}[{BOLD_YELLOW}?{BOLD_WHITE}]{YELLOW} "
        f"{message} {prompt_suffix}: {RESET}"
    )

    with _print_lock:
        print(prompt_text, end="", flush=True)

    try:
        response = input().strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()  # Newline after interrupted input
        return default

    if response == "":
        return default
    elif response in ("y", "yes"):
        return True
    elif response in ("n", "no"):
        return False
    else:
        return default


def prompt(message: str, mask: bool = False, default: str = "") -> str:
    """
    Ask for text input.

    Args:
        message: Prompt message
        mask: If True, hide input (for passwords)
        default: Default value if user presses Enter

    Returns:
        User's input string, or default if empty

    Example:
        >>> password = prompt("Repository password", mask=True)
        [?] Repository password: ********
    """
    prompt_text = f"{BOLD_WHITE}[{BOLD_YELLOW}?{BOLD_WHITE}]{YELLOW} {message}: {RESET}"

    with _print_lock:
        print(prompt_text, end="", flush=True)

    try:
        if mask:
            # getpass doesn't work well with our prompt already printed
            # So we need to handle it differently
            response = getpass.getpass(prompt="")
        else:
            response = input()
    except (EOFError, KeyboardInterrupt):
        print()  # Newline after interrupted input
        return default

    if response == "":
        return default

    return response


def prompt_choice(message: str, choices: list[str], default: int = 0) -> int:
    """
    Ask user to choose from a list of options.

    Args:
        message: Prompt message
        choices: List of choices to display
        default: Index of default choice (0-based)

    Returns:
        Index of selected choice

    Example:
        >>> idx = prompt_choice("Select target", ["postgres", "minio", "all"])
        [?] Select target
            1) postgres
            2) minio
            3) all
        Choice [1]: 2
    """
    prompt_header = f"{BOLD_WHITE}[{BOLD_YELLOW}?{BOLD_WHITE}]{YELLOW} {message}{RESET}"

    with _print_lock:
        print(prompt_header, flush=True)
        for i, choice in enumerate(choices):
            marker = "*" if i == default else " "
            print(f"   {marker}{i + 1}) {choice}", flush=True)
        print(
            f"{YELLOW}Choice [{default + 1}]: {RESET}",
            end="",
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
