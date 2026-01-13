"""
User input prompts for terminal UI.
"""

from ._console import _get_console


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
    return _get_console().confirm(message, default)


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
    return _get_console().prompt(message, mask, default)


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
    return _get_console().prompt_choice(message, choices, default)
