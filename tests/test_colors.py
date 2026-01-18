"""Unit tests for spec_kit.utils.colors module."""

import pytest

from spec_kit.utils import colors


class TestColorize:
    """Tests for colorize function."""

    def test_wraps_text_with_color_codes(self):
        """Test that text is wrapped with ANSI color codes."""
        result = colors.colorize("test", colors.GREEN)

        assert result.startswith('\033[0;32m')  # GREEN code
        assert result.endswith('\033[0m')  # Reset code
        assert 'test' in result

    def test_different_colors(self):
        """Test different color codes."""
        red_text = colors.colorize("error", colors.RED)
        green_text = colors.colorize("success", colors.GREEN)
        yellow_text = colors.colorize("warning", colors.YELLOW)
        blue_text = colors.colorize("info", colors.BLUE)

        assert '\033[0;31m' in red_text  # RED
        assert '\033[0;32m' in green_text  # GREEN
        assert '\033[1;33m' in yellow_text  # YELLOW
        assert '\033[0;34m' in blue_text  # BLUE


class TestSuccessMessage:
    """Tests for success function."""

    def test_prints_success_with_checkmark(self, capsys):
        """Test that success message includes green checkmark."""
        colors.success("Test passed")

        captured = capsys.readouterr()
        assert "✓" in captured.out
        assert "Test passed" in captured.out
        assert '\033[0;32m' in captured.out  # GREEN color


class TestErrorMessage:
    """Tests for error function."""

    def test_prints_error_with_x_mark(self, capsys):
        """Test that error message includes red X."""
        colors.error("Test failed")

        captured = capsys.readouterr()
        assert "✗" in captured.out
        assert "Test failed" in captured.out
        assert '\033[0;31m' in captured.out  # RED color


class TestWarningMessage:
    """Tests for warning function."""

    def test_prints_warning_with_symbol(self, capsys):
        """Test that warning message includes yellow warning symbol."""
        colors.warning("Be careful")

        captured = capsys.readouterr()
        assert "⚠" in captured.out
        assert "Be careful" in captured.out
        assert '\033[1;33m' in captured.out  # YELLOW color


class TestInfoMessage:
    """Tests for info function."""

    def test_prints_info_with_symbol(self, capsys):
        """Test that info message includes blue info symbol."""
        colors.info("Note this")

        captured = capsys.readouterr()
        assert "ℹ" in captured.out
        assert "Note this" in captured.out
        assert '\033[0;34m' in captured.out  # BLUE color


class TestPrintHeader:
    """Tests for print_header function."""

    def test_prints_header_with_title(self, capsys):
        """Test that header is printed with border and title."""
        colors.print_header("Test Title")

        captured = capsys.readouterr()
        assert "Test Title" in captured.out
        assert "╔" in captured.out  # Top border
        assert "╚" in captured.out  # Bottom border
        assert "║" in captured.out  # Side borders

    def test_prints_header_with_subtitle(self, capsys):
        """Test that header includes subtitle if provided."""
        colors.print_header("Main Title", "Subtitle Text")

        captured = capsys.readouterr()
        assert "Main Title" in captured.out
        assert "Subtitle Text" in captured.out


class TestPrintSeparator:
    """Tests for print_separator function."""

    def test_prints_separator_line(self, capsys):
        """Test that separator line is printed."""
        colors.print_separator()

        captured = capsys.readouterr()
        assert "━" in captured.out
        assert len([c for c in captured.out if c == "━"]) > 20  # Many dashes


class TestColorConstants:
    """Tests for color constant values."""

    def test_color_constants_are_ansi_codes(self):
        """Test that color constants contain ANSI escape sequences."""
        assert colors.RED.startswith('\033[')
        assert colors.GREEN.startswith('\033[')
        assert colors.YELLOW.startswith('\033[')
        assert colors.BLUE.startswith('\033[')
        assert colors.NC.startswith('\033[')

    def test_nc_is_reset_code(self):
        """Test that NC (No Color) is the reset code."""
        assert colors.NC == '\033[0m'
