"""Tests for iris.ui module."""

from unittest.mock import patch

import pytest

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

    def test_danger_banner(self, capsys):
        """Test UI danger_banner output."""
        ui = UI()
        ui.danger_banner("CRITICAL")
        captured = capsys.readouterr()
        assert "CRITICAL" in captured.out
        assert "\033[41m" in captured.out  # BG_RED


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


class TestStatusList:
    """Test status_list context manager."""

    def test_initial_render(self, capsys):
        """Test initial pending state render."""
        ui = UI()
        with ui.status_list(["item1", "item2"]):
            pass
        captured = capsys.readouterr()
        assert "item1" in captured.out
        assert "item2" in captured.out
        assert "pending" in captured.out

    def test_update_success(self, capsys):
        """Test updating to success state."""
        ui = UI()
        with ui.status_list(["item1"]) as status:
            status.update("item1", "success")
        captured = capsys.readouterr()
        assert "✓" in captured.out
        assert "success" in captured.out

    def test_update_with_detail(self, capsys):
        """Test update with detail string."""
        ui = UI()
        with ui.status_list(["item1"]) as status:
            status.update("item1", "success", detail="10.0.0.5")
        captured = capsys.readouterr()
        assert "10.0.0.5" in captured.out

    def test_update_error(self, capsys):
        """Test error state."""
        ui = UI()
        with ui.status_list(["item1"]) as status:
            status.update("item1", "error", detail="timeout")
        captured = capsys.readouterr()
        assert "✘" in captured.out
        assert "timeout" in captured.out

    def test_update_warning(self, capsys):
        """Test warning state."""
        ui = UI()
        with ui.status_list(["item1"]) as status:
            status.update("item1", "warning")
        captured = capsys.readouterr()
        assert "!" in captured.out
        assert "warning" in captured.out

    def test_update_skipped(self, capsys):
        """Test skipped state."""
        ui = UI()
        with ui.status_list(["item1"]) as status:
            status.update("item1", "skipped")
        captured = capsys.readouterr()
        assert "⊘" in captured.out
        assert "skipped" in captured.out

    def test_unknown_item_raises(self):
        """Test unknown item raises ValueError."""
        ui = UI()
        with (
            ui.status_list(["item1"]) as status,
            pytest.raises(ValueError, match="Unknown item"),
        ):
            status.update("unknown", "success")

    def test_invalid_state_raises(self):
        """Test invalid state raises ValueError."""
        ui = UI()
        with (
            ui.status_list(["item1"]) as status,
            pytest.raises(ValueError, match="Invalid state"),
        ):
            status.update("item1", "invalid_state")

    def test_all_states(self, capsys):
        """Test all valid states render without error."""
        ui = UI()
        states = ["pending", "running", "success", "error", "warning", "skipped"]
        with ui.status_list(["item"]) as status:
            for state in states:
                status.update("item", state)
        # Verify no exceptions raised and output contains expected content
        captured = capsys.readouterr()
        assert "item" in captured.out

    def test_multiple_items(self, capsys):
        """Test multiple items with different states."""
        ui = UI()
        with ui.status_list(["vm-web", "vm-db", "vm-cache"]) as status:
            status.update("vm-web", "success")
            status.update("vm-db", "running")
            status.update("vm-cache", "error", detail="timeout")
        captured = capsys.readouterr()
        assert "vm-web" in captured.out
        assert "vm-db" in captured.out
        assert "vm-cache" in captured.out

    def test_spinner_stops_on_exception(self):
        """Test spinner thread stops even if exception raised."""
        ui = UI()
        try:
            with ui.status_list(["item"]) as status:
                status.update("item", "running")
                raise RuntimeError("test error")
        except RuntimeError:
            pass
        # If spinner thread didn't stop, test would hang or leave zombie thread

    def test_empty_list(self):
        """Test empty items list."""
        ui = UI()
        with ui.status_list([]):
            pass
        # Should not crash with empty list
