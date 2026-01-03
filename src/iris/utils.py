"""
Utility functions for formatting values.
"""

from datetime import datetime


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (e.g., "1m 30s", "45s")

    Examples:
        >>> format_duration(45)
        '45s'
        >>> format_duration(90)
        '1m 30s'
        >>> format_duration(3661)
        '1h 1m'
    """
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def format_size(bytes_count: int) -> str:
    """
    Format bytes as human-readable size.

    Args:
        bytes_count: Size in bytes

    Returns:
        Formatted size string (e.g., "2.3 GB", "512 MB")

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536 * 1024 * 1024)
        '1.5 GB'
    """
    if bytes_count < 1024:
        return f"{bytes_count} B"
    elif bytes_count < 1024 * 1024:
        return f"{bytes_count / 1024:.1f} KB"
    elif bytes_count < 1024 * 1024 * 1024:
        return f"{bytes_count / (1024 * 1024):.1f} MB"
    elif bytes_count < 1024 * 1024 * 1024 * 1024:
        return f"{bytes_count / (1024 * 1024 * 1024):.1f} GB"
    else:
        return f"{bytes_count / (1024 * 1024 * 1024 * 1024):.1f} TB"


def format_age(timestamp: datetime) -> str:
    """
    Format timestamp as relative age.

    Args:
        timestamp: The timestamp to format

    Returns:
        Formatted age string (e.g., "4 hours ago", "2 days ago")

    Examples:
        >>> from datetime import datetime, timedelta
        >>> now = datetime.now()
        >>> format_age(now - timedelta(hours=4))
        '4 hours ago'
    """
    now = datetime.now()
    delta = now - timestamp

    seconds = delta.total_seconds()

    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        unit = "minute" if minutes == 1 else "minutes"
        return f"{minutes} {unit} ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        unit = "hour" if hours == 1 else "hours"
        return f"{hours} {unit} ago"
    elif seconds < 604800:
        days = int(seconds // 86400)
        unit = "day" if days == 1 else "days"
        return f"{days} {unit} ago"
    elif seconds < 2592000:
        weeks = int(seconds // 604800)
        unit = "week" if weeks == 1 else "weeks"
        return f"{weeks} {unit} ago"
    else:
        months = int(seconds // 2592000)
        unit = "month" if months == 1 else "months"
        return f"{months} {unit} ago"
