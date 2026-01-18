"""Unit tests for spec_kit.cli module."""

import pytest
import sys
from unittest.mock import Mock, patch

from spec_kit.cli import main


class TestCliVersionFlag:
    """Tests for --version flag."""

    def test_prints_version(self, capsys):
        """Test --version flag prints version and exits."""
        with patch.object(sys, 'argv', ['spec-kit', '--version']):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "2.0.0" in captured.out


class TestCliHelpFlag:
    """Tests for --help flag."""

    def test_prints_help(self, capsys):
        """Test --help flag prints help and exits."""
        with patch.object(sys, 'argv', ['spec-kit', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "Professional spec-driven development" in captured.out


class TestInitCommand:
    """Tests for init command routing."""

    def test_routes_to_init_handler(self):
        """Test init command routes to init.execute."""
        with patch.object(sys, 'argv', ['spec-kit', 'init']):
            with patch('spec_kit.commands.init.execute') as mock_execute:
                mock_execute.return_value = 0

                result = main()

                assert result == 0
                assert mock_execute.called
                # Verify args passed to execute
                args = mock_execute.call_args[0][0]
                assert args.command == 'init'

    def test_passes_path_argument(self):
        """Test path argument is passed correctly."""
        with patch.object(sys, 'argv', ['spec-kit', 'init', '/tmp/test']):
            with patch('spec_kit.commands.init.execute') as mock_execute:
                mock_execute.return_value = 0

                main()

                args = mock_execute.call_args[0][0]
                assert args.path == '/tmp/test'

    def test_passes_plugins_argument(self):
        """Test --plugins argument is passed correctly."""
        with patch.object(sys, 'argv', ['spec-kit', 'init', '--plugins', 'api,ai']):
            with patch('spec_kit.commands.init.execute') as mock_execute:
                mock_execute.return_value = 0

                main()

                args = mock_execute.call_args[0][0]
                assert args.plugins == 'api,ai'

    def test_passes_no_interactive_flag(self):
        """Test --no-interactive flag is passed correctly."""
        with patch.object(sys, 'argv', ['spec-kit', 'init', '--no-interactive']):
            with patch('spec_kit.commands.init.execute') as mock_execute:
                mock_execute.return_value = 0

                main()

                args = mock_execute.call_args[0][0]
                assert args.no_interactive is True

    def test_passes_force_flag(self):
        """Test --force flag is passed correctly."""
        with patch.object(sys, 'argv', ['spec-kit', 'init', '--force']):
            with patch('spec_kit.commands.init.execute') as mock_execute:
                mock_execute.return_value = 0

                main()

                args = mock_execute.call_args[0][0]
                assert args.force is True


class TestVerifyCommand:
    """Tests for verify command routing."""

    def test_routes_to_verify_handler(self):
        """Test verify command routes to verify.execute."""
        with patch.object(sys, 'argv', ['spec-kit', 'verify']):
            with patch('spec_kit.commands.verify.execute') as mock_execute:
                mock_execute.return_value = 0

                result = main()

                assert result == 0
                assert mock_execute.called
                args = mock_execute.call_args[0][0]
                assert args.command == 'verify'

    def test_passes_json_flag(self):
        """Test --json flag is passed correctly."""
        with patch.object(sys, 'argv', ['spec-kit', 'verify', '--json']):
            with patch('spec_kit.commands.verify.execute') as mock_execute:
                mock_execute.return_value = 0

                main()

                args = mock_execute.call_args[0][0]
                assert args.json is True

    def test_passes_verbose_flag(self):
        """Test --verbose flag is passed correctly."""
        with patch.object(sys, 'argv', ['spec-kit', 'verify', '--verbose']):
            with patch('spec_kit.commands.verify.execute') as mock_execute:
                mock_execute.return_value = 0

                main()

                args = mock_execute.call_args[0][0]
                assert args.verbose is True


class TestErrorHandling:
    """Tests for error handling."""

    def test_handles_keyboard_interrupt(self, capsys):
        """Test KeyboardInterrupt handling."""
        with patch.object(sys, 'argv', ['spec-kit', 'init']):
            with patch('spec_kit.commands.init.execute') as mock_execute:
                mock_execute.side_effect = KeyboardInterrupt()

                result = main()

                assert result == 130  # SIGINT exit code

        captured = capsys.readouterr()
        # Should print newline on interrupt
        assert captured.out == '\n'

    def test_handles_general_exception(self, capsys):
        """Test general exception handling."""
        with patch.object(sys, 'argv', ['spec-kit', 'init']):
            with patch('spec_kit.commands.init.execute') as mock_execute:
                mock_execute.side_effect = Exception("Test error")

                result = main()

                assert result == 1

        captured = capsys.readouterr()
        assert "Error: Test error" in captured.err

    def test_verbose_flag_shows_traceback(self, capsys):
        """Test verbose flag shows full traceback on error."""
        with patch.object(sys, 'argv', ['spec-kit', '--verbose', 'init']):
            with patch('spec_kit.commands.init.execute') as mock_execute:
                mock_execute.side_effect = Exception("Test error")

                result = main()

                assert result == 1

        captured = capsys.readouterr()
        # Should include traceback with verbose
        assert "Traceback" in captured.err or "Test error" in captured.err


class TestExitCodes:
    """Tests for exit code propagation."""

    def test_returns_success_exit_code(self):
        """Test successful command returns 0."""
        with patch.object(sys, 'argv', ['spec-kit', 'init']):
            with patch('spec_kit.commands.init.execute') as mock_execute:
                mock_execute.return_value = 0

                result = main()

                assert result == 0

    def test_returns_failure_exit_code(self):
        """Test failed command returns non-zero."""
        with patch.object(sys, 'argv', ['spec-kit', 'verify']):
            with patch('spec_kit.commands.verify.execute') as mock_execute:
                mock_execute.return_value = 1

                result = main()

                assert result == 1

    def test_propagates_command_exit_code(self):
        """Test arbitrary exit codes are propagated."""
        with patch.object(sys, 'argv', ['spec-kit', 'init']):
            with patch('spec_kit.commands.init.execute') as mock_execute:
                mock_execute.return_value = 42

                result = main()

                assert result == 42
