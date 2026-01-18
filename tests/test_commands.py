"""Unit tests for spec_kit.commands module (init and verify)."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from argparse import Namespace

from spec_kit.commands import init, verify


class TestInitExecute:
    """Tests for init.execute() function."""

    def test_executes_with_default_args(self, tmp_path):
        """Test basic execution with default arguments."""
        args = Namespace(
            path=str(tmp_path),
            plugins=None,
            no_interactive=True,
            force=False
        )

        with patch('spec_kit.commands.init.Installer') as MockInstaller:
            mock_installer = Mock()
            MockInstaller.return_value = mock_installer

            result = init.execute(args)

            assert result == 0
            assert MockInstaller.called
            assert mock_installer.run_installation.called

    def test_parses_comma_separated_plugins(self, tmp_path):
        """Test plugin parsing from comma-separated string."""
        args = Namespace(
            path=str(tmp_path),
            plugins='api,ai',
            no_interactive=True,
            force=False
        )

        with patch('spec_kit.commands.init.Installer') as MockInstaller:
            mock_installer = Mock()
            MockInstaller.return_value = mock_installer

            init.execute(args)

            # Verify plugins parsed correctly
            call_args = mock_installer.run_installation.call_args
            plugins = call_args[1]['plugins']
            assert plugins == ['api', 'ai']

    def test_parses_plugins_with_spaces(self, tmp_path):
        """Test plugin parsing handles extra whitespace."""
        args = Namespace(
            path=str(tmp_path),
            plugins='  api  ,  ai  ',
            no_interactive=True,
            force=False
        )

        with patch('spec_kit.commands.init.Installer') as MockInstaller:
            mock_installer = Mock()
            MockInstaller.return_value = mock_installer

            init.execute(args)

            call_args = mock_installer.run_installation.call_args
            plugins = call_args[1]['plugins']
            assert plugins == ['api', 'ai']

    def test_passes_force_flag(self, tmp_path):
        """Test force flag is passed to installer."""
        args = Namespace(
            path=str(tmp_path),
            plugins=None,
            no_interactive=True,
            force=True
        )

        with patch('spec_kit.commands.init.Installer') as MockInstaller:
            mock_installer = Mock()
            MockInstaller.return_value = mock_installer

            init.execute(args)

            call_args = mock_installer.run_installation.call_args
            assert call_args[1]['force'] is True

    def test_passes_interactive_flag(self, tmp_path):
        """Test interactive mode flag is inverted correctly."""
        args = Namespace(
            path=str(tmp_path),
            plugins=None,
            no_interactive=False,  # Interactive mode ON
            force=False
        )

        with patch('spec_kit.commands.init.Installer') as MockInstaller:
            mock_installer = Mock()
            MockInstaller.return_value = mock_installer

            init.execute(args)

            call_args = mock_installer.run_installation.call_args
            assert call_args[1]['interactive'] is True

    def test_handles_file_not_found_error(self, tmp_path, capsys):
        """Test FileNotFoundError handling."""
        args = Namespace(
            path=str(tmp_path),
            plugins=None,
            no_interactive=True,
            force=False
        )

        with patch('spec_kit.commands.init.Installer') as MockInstaller:
            MockInstaller.side_effect = FileNotFoundError("Directory not found")

            result = init.execute(args)

            assert result == 1

        captured = capsys.readouterr()
        assert "Directory not found" in captured.out

    def test_handles_file_exists_error(self, tmp_path, capsys):
        """Test FileExistsError handling."""
        args = Namespace(
            path=str(tmp_path),
            plugins=None,
            no_interactive=True,
            force=False
        )

        with patch('spec_kit.commands.init.Installer') as MockInstaller:
            mock_installer = Mock()
            MockInstaller.return_value = mock_installer
            mock_installer.run_installation.side_effect = FileExistsError("File exists")

            result = init.execute(args)

            assert result == 1

        captured = capsys.readouterr()
        assert "File exists" in captured.out

    def test_handles_value_error(self, tmp_path, capsys):
        """Test ValueError handling (e.g., invalid plugin)."""
        args = Namespace(
            path=str(tmp_path),
            plugins='invalid-plugin',
            no_interactive=True,
            force=False
        )

        with patch('spec_kit.commands.init.Installer') as MockInstaller:
            mock_installer = Mock()
            MockInstaller.return_value = mock_installer
            mock_installer.run_installation.side_effect = ValueError("Unknown plugin")

            result = init.execute(args)

            assert result == 1

        captured = capsys.readouterr()
        assert "Unknown plugin" in captured.out

    def test_handles_runtime_error(self, tmp_path, capsys):
        """Test RuntimeError handling."""
        args = Namespace(
            path=str(tmp_path),
            plugins=None,
            no_interactive=True,
            force=False
        )

        with patch('spec_kit.commands.init.Installer') as MockInstaller:
            MockInstaller.side_effect = RuntimeError("Cannot find spec-kit")

            result = init.execute(args)

            assert result == 1

        captured = capsys.readouterr()
        assert "Cannot find spec-kit" in captured.out

    def test_handles_keyboard_interrupt(self, tmp_path, capsys):
        """Test KeyboardInterrupt handling."""
        args = Namespace(
            path=str(tmp_path),
            plugins=None,
            no_interactive=True,
            force=False
        )

        with patch('spec_kit.commands.init.Installer') as MockInstaller:
            mock_installer = Mock()
            MockInstaller.return_value = mock_installer
            mock_installer.run_installation.side_effect = KeyboardInterrupt()

            result = init.execute(args)

            assert result == 130

        captured = capsys.readouterr()
        assert "cancelled" in captured.out

    def test_resolves_path_correctly(self, tmp_path):
        """Test that path is resolved to absolute path."""
        args = Namespace(
            path='.',
            plugins=None,
            no_interactive=True,
            force=False
        )

        with patch('spec_kit.commands.init.Installer') as MockInstaller:
            mock_installer = Mock()
            MockInstaller.return_value = mock_installer

            init.execute(args)

            # Verify Installer was called with resolved path
            call_args = MockInstaller.call_args
            target_path = call_args[1]['target_path']
            assert target_path.is_absolute()


class TestVerifyExecute:
    """Tests for verify.execute() function."""

    def test_executes_with_default_args(self, tmp_path, monkeypatch):
        """Test basic execution with default arguments."""
        monkeypatch.chdir(tmp_path)

        args = Namespace(
            json=False,
            verbose=False
        )

        with patch('spec_kit.commands.verify.Validator') as MockValidator:
            mock_validator = Mock()
            MockValidator.return_value = mock_validator
            mock_validator.run_all_checks.return_value = {}
            mock_validator.get_exit_code.return_value = 0

            result = verify.execute(args)

            assert result == 0
            assert MockValidator.called
            assert mock_validator.run_all_checks.called

    def test_uses_current_directory(self, tmp_path, monkeypatch):
        """Test that verify uses current working directory."""
        monkeypatch.chdir(tmp_path)

        args = Namespace(
            json=False,
            verbose=False
        )

        with patch('spec_kit.commands.verify.Validator') as MockValidator:
            mock_validator = Mock()
            MockValidator.return_value = mock_validator
            mock_validator.run_all_checks.return_value = {}
            mock_validator.get_exit_code.return_value = 0

            verify.execute(args)

            # Verify Validator was called with current directory
            call_args = MockValidator.call_args
            target_path = call_args[1]['target_path']
            assert str(target_path) == str(tmp_path)

    def test_routes_to_json_output(self, tmp_path, monkeypatch):
        """Test --json flag routes to print_json."""
        monkeypatch.chdir(tmp_path)

        args = Namespace(
            json=True,
            verbose=False
        )

        with patch('spec_kit.commands.verify.Validator') as MockValidator:
            mock_validator = Mock()
            MockValidator.return_value = mock_validator
            mock_validator.run_all_checks.return_value = {}
            mock_validator.get_exit_code.return_value = 0

            verify.execute(args)

            # Should call print_json, not print_results
            assert mock_validator.print_json.called
            assert not mock_validator.print_results.called

    def test_routes_to_verbose_output(self, tmp_path, monkeypatch):
        """Test --verbose flag passed to print_results."""
        monkeypatch.chdir(tmp_path)

        args = Namespace(
            json=False,
            verbose=True
        )

        with patch('spec_kit.commands.verify.Validator') as MockValidator:
            mock_validator = Mock()
            MockValidator.return_value = mock_validator
            mock_validator.run_all_checks.return_value = {}
            mock_validator.get_exit_code.return_value = 0

            verify.execute(args)

            # Should call print_results with verbose=True
            assert mock_validator.print_results.called
            call_args = mock_validator.print_results.call_args
            assert call_args[1]['verbose'] is True

    def test_returns_validator_exit_code(self, tmp_path, monkeypatch):
        """Test exit code propagation from validator."""
        monkeypatch.chdir(tmp_path)

        args = Namespace(
            json=False,
            verbose=False
        )

        with patch('spec_kit.commands.verify.Validator') as MockValidator:
            mock_validator = Mock()
            MockValidator.return_value = mock_validator
            mock_validator.run_all_checks.return_value = {}
            mock_validator.get_exit_code.return_value = 1  # Failure

            result = verify.execute(args)

            assert result == 1

    def test_handles_keyboard_interrupt(self, tmp_path, monkeypatch, capsys):
        """Test KeyboardInterrupt handling."""
        monkeypatch.chdir(tmp_path)

        args = Namespace(
            json=False,
            verbose=False
        )

        with patch('spec_kit.commands.verify.Validator') as MockValidator:
            mock_validator = Mock()
            MockValidator.return_value = mock_validator
            mock_validator.run_all_checks.side_effect = KeyboardInterrupt()

            result = verify.execute(args)

            assert result == 130

        captured = capsys.readouterr()
        assert "cancelled" in captured.out

    def test_handles_general_exception(self, tmp_path, monkeypatch, capsys):
        """Test general exception handling."""
        monkeypatch.chdir(tmp_path)

        args = Namespace(
            json=False,
            verbose=False
        )

        with patch('spec_kit.commands.verify.Validator') as MockValidator:
            MockValidator.side_effect = Exception("Test error")

            result = verify.execute(args)

            assert result == 1

        captured = capsys.readouterr()
        assert "Test error" in captured.out
