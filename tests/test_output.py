"""Tests for iris.output module."""

from iris import (
    box,
    command,
    danger_banner,
    debug,
    dry_run,
    duration,
    error,
    header,
    hint,
    info,
    secure,
    step,
    subheading,
    success,
    warning,
)


class TestOutputFunctions:
    """Test output formatting functions."""

    def test_success_format(self, capsys):
        """Test success message format."""
        success("Test message")
        captured = capsys.readouterr()
        assert "✓" in captured.out
        assert "Test message" in captured.out

    def test_error_format(self, capsys):
        """Test error message format (goes to stderr)."""
        error("Error message")
        captured = capsys.readouterr()
        assert "x" in captured.err
        assert "Error message" in captured.err

    def test_warning_format(self, capsys):
        """Test warning message format."""
        warning("Warning message")
        captured = capsys.readouterr()
        assert "!" in captured.out
        assert "Warning message" in captured.out

    def test_info_format(self, capsys):
        """Test info message format."""
        info("Info message")
        captured = capsys.readouterr()
        assert "i" in captured.out
        assert "Info message" in captured.out

    def test_hint_format(self, capsys):
        """Test hint message format."""
        hint("Hint message")
        captured = capsys.readouterr()
        assert "+" in captured.out
        assert "Hint message" in captured.out

    def test_command_format(self, capsys):
        """Test command message format."""
        command("restic backup")
        captured = capsys.readouterr()
        assert ">" in captured.out
        assert "Running:" in captured.out
        assert "restic backup" in captured.out

    def test_debug_disabled(self, capsys):
        """Test debug message when disabled."""
        debug("Debug message", enabled=False)
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == ""

    def test_debug_enabled(self, capsys):
        """Test debug message when enabled."""
        debug("Debug message", enabled=True)
        captured = capsys.readouterr()
        assert "DEBUG" in captured.err
        assert "Debug message" in captured.err

    def test_secure_format(self, capsys):
        """Test secure message format."""
        secure("Key loaded")
        captured = capsys.readouterr()
        assert "S" in captured.out
        assert "Key loaded" in captured.out

    def test_dry_run_format(self, capsys):
        """Test dry-run message format."""
        dry_run("delete old backups")
        captured = capsys.readouterr()
        assert "DRY-RUN" in captured.out
        assert "delete old backups" in captured.out

    def test_step_format(self, capsys):
        """Test step indicator format."""
        step(1, 3, "First step")
        captured = capsys.readouterr()
        assert "[1/3]" in captured.out
        assert "First step" in captured.out

    def test_duration_format(self, capsys):
        """Test duration message format."""
        duration(42.5)
        captured = capsys.readouterr()
        assert "TIME" in captured.out
        assert "42.5s" in captured.out

    def test_header_format(self, capsys):
        """Test header format."""
        header("Test Header")
        captured = capsys.readouterr()
        assert "═" in captured.out
        assert "Test Header" in captured.out

    def test_subheading_format(self, capsys):
        """Test subheading format."""
        subheading("Test Subheading")
        captured = capsys.readouterr()
        assert "─" in captured.out
        assert "Test Subheading" in captured.out

    def test_box_format(self, capsys):
        """Test box format with double-line borders."""
        box("Test Box")
        captured = capsys.readouterr()
        assert "╔" in captured.out
        assert "╗" in captured.out
        assert "║" in captured.out
        assert "╚" in captured.out
        assert "╝" in captured.out
        assert "═" in captured.out
        assert "Test Box" in captured.out

    def test_box_multiline(self, capsys):
        """Test box with multiple lines."""
        box("Line 1\nLine 2")
        captured = capsys.readouterr()
        assert "Line 1" in captured.out
        assert "Line 2" in captured.out
        # Should have exactly 2 content lines between borders
        lines = captured.out.strip().split("\n")
        assert len(lines) == 4  # top border + 2 content + bottom border

    def test_danger_banner_format(self, capsys):
        """Test danger_banner uses box with red background."""
        danger_banner("ALERT")
        captured = capsys.readouterr()
        assert "╔" in captured.out
        assert "ALERT" in captured.out
        assert "\033[41m" in captured.out  # BG_RED
