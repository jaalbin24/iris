"""Tests for iris.prompts module."""

from unittest.mock import patch

from iris import confirm, prompt, prompt_choice


class TestConfirm:
    """Test confirm function."""

    def test_confirm_yes(self):
        """Test confirming with 'y'."""
        with patch("builtins.input", return_value="y"):
            result = confirm("Continue?")
            assert result is True

    def test_confirm_yes_full(self):
        """Test confirming with 'yes'."""
        with patch("builtins.input", return_value="yes"):
            result = confirm("Continue?")
            assert result is True

    def test_confirm_no(self):
        """Test declining with 'n'."""
        with patch("builtins.input", return_value="n"):
            result = confirm("Continue?")
            assert result is False

    def test_confirm_no_full(self):
        """Test declining with 'no'."""
        with patch("builtins.input", return_value="no"):
            result = confirm("Continue?")
            assert result is False

    def test_confirm_default_false(self):
        """Test empty input with default=False."""
        with patch("builtins.input", return_value=""):
            result = confirm("Continue?", default=False)
            assert result is False

    def test_confirm_default_true(self):
        """Test empty input with default=True."""
        with patch("builtins.input", return_value=""):
            result = confirm("Continue?", default=True)
            assert result is True

    def test_confirm_invalid_uses_default(self):
        """Test invalid input falls back to default."""
        with patch("builtins.input", return_value="maybe"):
            result = confirm("Continue?", default=False)
            assert result is False

    def test_confirm_case_insensitive(self):
        """Test case insensitive input."""
        with patch("builtins.input", return_value="Y"):
            result = confirm("Continue?")
            assert result is True


class TestPrompt:
    """Test prompt function."""

    def test_prompt_returns_input(self):
        """Test prompt returns user input."""
        with patch("builtins.input", return_value="hello"):
            result = prompt("Enter value")
            assert result == "hello"

    def test_prompt_empty_returns_default(self):
        """Test empty input returns default."""
        with patch("builtins.input", return_value=""):
            result = prompt("Enter value", default="fallback")
            assert result == "fallback"

    def test_prompt_shows_default_in_text(self, capsys):
        """Test that the default value appears in the prompt text."""
        with patch("builtins.input", return_value=""):
            prompt("Enter value", default="fallback")
        output = capsys.readouterr().out
        assert "[fallback]" in output

    def test_prompt_masked_hides_default(self, capsys):
        """Test that masked prompts do not show the default."""
        with patch("getpass.getpass", return_value=""):
            prompt("Password", mask=True, default="secret")
        output = capsys.readouterr().out
        assert "[secret]" not in output

    def test_prompt_masked(self):
        """Test masked prompt uses getpass."""
        with patch("getpass.getpass", return_value="secret"):
            result = prompt("Password", mask=True)
            assert result == "secret"


class TestPromptChoice:
    """Test prompt_choice function."""

    def test_prompt_choice_selection(self):
        """Test selecting a choice."""
        with patch("builtins.input", return_value="2"):
            result = prompt_choice("Pick one", ["a", "b", "c"])
            assert result == 1  # 0-indexed

    def test_prompt_choice_default(self):
        """Test empty input uses default."""
        with patch("builtins.input", return_value=""):
            result = prompt_choice("Pick one", ["a", "b", "c"], default=2)
            assert result == 2

    def test_prompt_choice_invalid(self):
        """Test invalid input falls back to default."""
        with patch("builtins.input", return_value="invalid"):
            result = prompt_choice("Pick one", ["a", "b", "c"], default=0)
            assert result == 0

    def test_prompt_choice_out_of_range(self):
        """Test out of range selection uses default."""
        with patch("builtins.input", return_value="99"):
            result = prompt_choice("Pick one", ["a", "b", "c"], default=0)
            assert result == 0
