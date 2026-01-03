"""Tests for iris.ui module."""

from unittest.mock import patch

from iris import UI


class TestUIContext:
    """Test UI class."""

    def test_ui_defaults(self):
        """Test default UI settings."""
        ui = UI()
        assert ui.interactive is True
        assert ui.verbose is False
        assert ui._debug is False

    def test_ui_custom_settings(self):
        """Test custom UI settings."""
        ui = UI(interactive=False, verbose=True, debug=True)
        assert ui.interactive is False
        assert ui.verbose is True
        assert ui._debug is True


class TestUIOutput:
    """Test UI output methods."""

    def test_header(self, capsys):
        """Test UI header output."""
        ui = UI()
        ui.header("Test")
        captured = capsys.readouterr()
        assert "Test" in captured.out
        assert "═" in captured.out

    def test_success(self, capsys):
        """Test UI success output."""
        ui = UI()
        ui.success("Done")
        captured = capsys.readouterr()
        assert "✓" in captured.out
        assert "Done" in captured.out

    def test_error(self, capsys):
        """Test UI error output."""
        ui = UI()
        ui.error("Failed")
        captured = capsys.readouterr()
        assert "Failed" in captured.err

    def test_command_verbose(self, capsys):
        """Test command output when verbose."""
        ui = UI(verbose=True)
        ui.command("ls -la")
        captured = capsys.readouterr()
        assert "ls -la" in captured.out

    def test_command_not_verbose(self, capsys):
        """Test command output when not verbose."""
        ui = UI(verbose=False)
        ui.command("ls -la")
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_debug_enabled(self, capsys):
        """Test debug output when enabled."""
        ui = UI(debug=True)
        ui.debug("Debug info")
        captured = capsys.readouterr()
        assert "Debug info" in captured.err

    def test_debug_disabled(self, capsys):
        """Test debug output when disabled."""
        ui = UI(debug=False)
        ui.debug("Debug info")
        captured = capsys.readouterr()
        assert captured.err == ""


class TestUIPrompts:
    """Test UI prompt methods."""

    def test_confirm_interactive(self):
        """Test confirm in interactive mode."""
        ui = UI(interactive=True)
        with patch("builtins.input", return_value="y"):
            result = ui.confirm("Continue?")
            assert result is True

    def test_confirm_non_interactive(self):
        """Test confirm in non-interactive mode returns default."""
        ui = UI(interactive=False)
        result = ui.confirm("Continue?", default=True)
        assert result is True

        result = ui.confirm("Continue?", default=False)
        assert result is False

    def test_prompt_interactive(self):
        """Test prompt in interactive mode."""
        ui = UI(interactive=True)
        with patch("builtins.input", return_value="hello"):
            result = ui.prompt("Enter value")
            assert result == "hello"

    def test_prompt_non_interactive(self):
        """Test prompt in non-interactive mode returns default."""
        ui = UI(interactive=False)
        result = ui.prompt("Enter value", default="fallback")
        assert result == "fallback"


class TestUIProgress:
    """Test UI progress context manager."""

    def test_progress_context(self, capsys):
        """Test progress context manager."""
        ui = UI()
        with ui.progress(["Step1", "Step2"]) as p:
            p.start("Step1")
            p.complete("Step1", "done")
            p.start("Step2")
            p.complete("Step2")

        captured = capsys.readouterr()
        assert "[1/2]" in captured.out
        assert "[2/2]" in captured.out
        assert "Step1" in captured.out
        assert "Step2" in captured.out

    def test_progress_fail(self, capsys):
        """Test progress failure."""
        ui = UI()
        with ui.progress(["Step1"]) as p:
            p.start("Step1")
            p.fail("Step1", "connection refused")

        captured = capsys.readouterr()
        assert "failed" in captured.err
        assert "connection refused" in captured.err

    def test_progress_unknown_step(self):
        """Test starting unknown step raises error."""
        ui = UI()
        with ui.progress(["Step1"]) as p:
            try:
                p.start("UnknownStep")
                raise AssertionError("Should have raised ValueError")
            except ValueError as e:
                assert "Unknown step" in str(e)


class TestUITable:
    """Test UI table helper."""

    def test_table_creation(self):
        """Test creating table via UI."""
        ui = UI()
        table = ui.table(["Col1", "Col2"])
        assert table._columns == ["Col1", "Col2"]
