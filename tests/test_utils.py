"""Tests for iris.utils module."""

from datetime import datetime, timedelta

from iris import format_age, format_duration, format_size


class TestFormatDuration:
    """Test format_duration function."""

    def test_seconds_only(self):
        """Test formatting seconds."""
        assert format_duration(45) == "45s"
        assert format_duration(0) == "0s"
        assert format_duration(59) == "59s"

    def test_minutes_and_seconds(self):
        """Test formatting minutes and seconds."""
        assert format_duration(60) == "1m 0s"
        assert format_duration(90) == "1m 30s"
        assert format_duration(125) == "2m 5s"
        assert format_duration(3599) == "59m 59s"

    def test_hours_and_minutes(self):
        """Test formatting hours and minutes."""
        assert format_duration(3600) == "1h 0m"
        assert format_duration(3661) == "1h 1m"
        assert format_duration(7200) == "2h 0m"
        assert format_duration(7320) == "2h 2m"


class TestFormatSize:
    """Test format_size function."""

    def test_bytes(self):
        """Test formatting bytes."""
        assert format_size(0) == "0 B"
        assert format_size(512) == "512 B"
        assert format_size(1023) == "1023 B"

    def test_kilobytes(self):
        """Test formatting kilobytes."""
        assert format_size(1024) == "1.0 KB"
        assert format_size(1536) == "1.5 KB"
        assert format_size(10240) == "10.0 KB"

    def test_megabytes(self):
        """Test formatting megabytes."""
        assert format_size(1024 * 1024) == "1.0 MB"
        assert format_size(1536 * 1024) == "1.5 MB"
        assert format_size(512 * 1024 * 1024) == "512.0 MB"

    def test_gigabytes(self):
        """Test formatting gigabytes."""
        assert format_size(1024 * 1024 * 1024) == "1.0 GB"
        assert format_size(int(2.3 * 1024 * 1024 * 1024)) == "2.3 GB"

    def test_terabytes(self):
        """Test formatting terabytes."""
        assert format_size(1024 * 1024 * 1024 * 1024) == "1.0 TB"


class TestFormatAge:
    """Test format_age function."""

    def test_just_now(self):
        """Test very recent timestamps."""
        now = datetime.now()
        assert format_age(now) == "just now"
        assert format_age(now - timedelta(seconds=30)) == "just now"

    def test_minutes(self):
        """Test minute-old timestamps."""
        now = datetime.now()
        assert format_age(now - timedelta(minutes=1)) == "1 minute ago"
        assert format_age(now - timedelta(minutes=5)) == "5 minutes ago"
        assert format_age(now - timedelta(minutes=59)) == "59 minutes ago"

    def test_hours(self):
        """Test hour-old timestamps."""
        now = datetime.now()
        assert format_age(now - timedelta(hours=1)) == "1 hour ago"
        assert format_age(now - timedelta(hours=4)) == "4 hours ago"
        assert format_age(now - timedelta(hours=23)) == "23 hours ago"

    def test_days(self):
        """Test day-old timestamps."""
        now = datetime.now()
        assert format_age(now - timedelta(days=1)) == "1 day ago"
        assert format_age(now - timedelta(days=3)) == "3 days ago"
        assert format_age(now - timedelta(days=6)) == "6 days ago"

    def test_weeks(self):
        """Test week-old timestamps."""
        now = datetime.now()
        assert format_age(now - timedelta(weeks=1)) == "1 week ago"
        assert format_age(now - timedelta(weeks=3)) == "3 weeks ago"

    def test_months(self):
        """Test month-old timestamps."""
        now = datetime.now()
        assert format_age(now - timedelta(days=35)) == "1 month ago"
        assert format_age(now - timedelta(days=90)) == "3 months ago"
