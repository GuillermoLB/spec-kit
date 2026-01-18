"""Unit tests for spec_kit.core.validator module."""

import json
import pytest
from pathlib import Path

from spec_kit.core.validator import Validator, ValidationResult


class TestValidationResult:
    """Tests for ValidationResult class."""

    def test_initialization(self):
        """Test ValidationResult initialization."""
        result = ValidationResult(True, "Test message", "test.txt")

        assert result.passed is True
        assert result.message == "Test message"
        assert result.item == "test.txt"

    def test_repr_for_passed(self):
        """Test __repr__ for passed validation."""
        result = ValidationResult(True, "Success", "file.txt")

        assert "PASS" in repr(result)
        assert "file.txt" in repr(result)

    def test_repr_for_failed(self):
        """Test __repr__ for failed validation."""
        result = ValidationResult(False, "Failed", "missing.txt")

        assert "FAIL" in repr(result)
        assert "missing.txt" in repr(result)


class TestValidatorInitialization:
    """Tests for Validator class initialization."""

    def test_init_with_path(self, tmp_path):
        """Test validator initialization."""
        validator = Validator(tmp_path)

        assert validator.target_path == tmp_path.resolve()
        assert validator.results == []
        assert validator.pass_count == 0
        assert validator.fail_count == 0


class TestCheckFile:
    """Tests for _check_file method."""

    def test_returns_pass_when_file_exists(self, tmp_path):
        """Test file existence check passes."""
        validator = Validator(tmp_path)
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        result = validator._check_file(Path("test.txt"))

        assert result.passed is True
        assert validator.pass_count == 1
        assert validator.fail_count == 0

    def test_returns_fail_when_file_missing(self, tmp_path):
        """Test missing file detection."""
        validator = Validator(tmp_path)

        result = validator._check_file(Path("missing.txt"))

        assert result.passed is False
        assert "missing" in result.message
        assert validator.pass_count == 0
        assert validator.fail_count == 1

    def test_uses_custom_description(self, tmp_path):
        """Test custom description parameter."""
        validator = Validator(tmp_path)
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        result = validator._check_file(Path("test.txt"), "Custom description")

        assert "Custom description" in result.message

    def test_fails_when_path_is_directory(self, tmp_path):
        """Test that directories are not accepted as files."""
        validator = Validator(tmp_path)
        test_dir = tmp_path / "testdir"
        test_dir.mkdir()

        result = validator._check_file(Path("testdir"))

        assert result.passed is False


class TestCheckDir:
    """Tests for _check_dir method."""

    def test_returns_pass_when_dir_exists(self, tmp_path):
        """Test directory existence check passes."""
        validator = Validator(tmp_path)
        test_dir = tmp_path / "testdir"
        test_dir.mkdir()

        result = validator._check_dir(Path("testdir"))

        assert result.passed is True
        assert validator.pass_count == 1
        assert validator.fail_count == 0

    def test_returns_fail_when_dir_missing(self, tmp_path):
        """Test missing directory detection."""
        validator = Validator(tmp_path)

        result = validator._check_dir(Path("missing"))

        assert result.passed is False
        assert "missing" in result.message
        assert validator.pass_count == 0
        assert validator.fail_count == 1

    def test_fails_when_path_is_file(self, tmp_path):
        """Test that files are not accepted as directories."""
        validator = Validator(tmp_path)
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        result = validator._check_dir(Path("test.txt"))

        assert result.passed is False


class TestCheckExecutable:
    """Tests for _check_executable method."""

    def test_returns_pass_for_executable_file(self, tmp_path):
        """Test executable file check passes."""
        validator = Validator(tmp_path)
        script = tmp_path / "script.sh"
        script.write_text("#!/bin/bash\necho 'test'")
        script.chmod(0o755)

        result = validator._check_executable(Path("script.sh"))

        assert result.passed is True
        assert "executable" in result.message
        assert validator.pass_count == 1

    def test_returns_fail_for_non_executable_file(self, tmp_path):
        """Test non-executable file detection."""
        validator = Validator(tmp_path)
        script = tmp_path / "script.sh"
        script.write_text("#!/bin/bash\necho 'test'")
        script.chmod(0o644)  # Not executable

        result = validator._check_executable(Path("script.sh"))

        assert result.passed is False
        assert "not executable" in result.message
        assert validator.fail_count == 1

    def test_returns_fail_for_missing_file(self, tmp_path):
        """Test missing file detection."""
        validator = Validator(tmp_path)

        result = validator._check_executable(Path("missing.sh"))

        assert result.passed is False
        assert "missing" in result.message


class TestCheckCoreFiles:
    """Tests for check_core_files method."""

    def test_passes_with_complete_core_structure(self, tmp_path):
        """Test validation passes with all core files."""
        # Create complete structure
        (tmp_path / "CLAUDE.md").write_text("# Constitution")
        (tmp_path / ".claude" / "skills" / "test-plugin").mkdir(parents=True)
        (tmp_path / "specs").mkdir()

        validator = Validator(tmp_path)
        results = validator.check_core_files()

        assert 'core' in results
        # Should have checks for CLAUDE.md, .claude/skills, specs
        core_results = results['core']
        assert len(core_results) >= 3
        assert all(r.passed for r in core_results[:3])

    def test_fails_without_claude_md(self, tmp_path):
        """Test validation fails without CLAUDE.md."""
        (tmp_path / ".claude" / "skills").mkdir(parents=True)
        (tmp_path / "specs").mkdir()

        validator = Validator(tmp_path)
        results = validator.check_core_files()

        # First result should be CLAUDE.md check (failed)
        assert not results['core'][0].passed
        assert "CLAUDE.md" in results['core'][0].item

    def test_warns_when_skills_directory_empty(self, tmp_path):
        """Test warning for empty .claude/skills directory."""
        (tmp_path / "CLAUDE.md").write_text("# Constitution")
        (tmp_path / ".claude" / "skills").mkdir(parents=True)
        (tmp_path / "specs").mkdir()

        validator = Validator(tmp_path)
        results = validator.check_core_files()

        # Should have a warning about empty skills directory
        empty_warning = [r for r in results['core'] if "empty" in r.message]
        assert len(empty_warning) > 0


class TestCheckPlugins:
    """Tests for check_plugins method."""

    def test_returns_empty_when_no_skills_dir(self, tmp_path):
        """Test handling when .claude/skills doesn't exist."""
        validator = Validator(tmp_path)
        results = validator.check_plugins()

        assert results == {'plugins': []}

    def test_detects_installed_plugin(self, tmp_path):
        """Test plugin detection."""
        plugin_dir = tmp_path / ".claude" / "skills" / "test-plugin"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "SKILL.md").write_text("# Test Plugin")

        validator = Validator(tmp_path)
        results = validator.check_plugins()

        assert 'test-plugin' in results
        assert len(results['test-plugin']) >= 1
        assert results['test-plugin'][0].passed

    def test_detects_plugin_with_references(self, tmp_path):
        """Test plugin with references directory."""
        plugin_dir = tmp_path / ".claude" / "skills" / "test-plugin"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "SKILL.md").write_text("# Test Plugin")
        (plugin_dir / "references").mkdir()

        validator = Validator(tmp_path)
        results = validator.check_plugins()

        # Should have results for SKILL.md and references/
        assert len(results['test-plugin']) >= 2

    def test_detects_multiple_plugins(self, tmp_path):
        """Test detection of multiple plugins."""
        skills_dir = tmp_path / ".claude" / "skills"

        # Create two plugins
        for plugin_name in ['plugin-a', 'plugin-b']:
            plugin_dir = skills_dir / plugin_name
            plugin_dir.mkdir(parents=True)
            (plugin_dir / "SKILL.md").write_text(f"# {plugin_name}")

        validator = Validator(tmp_path)
        results = validator.check_plugins()

        assert 'plugin-a' in results
        assert 'plugin-b' in results

    def test_fails_for_plugin_without_skill_md(self, tmp_path):
        """Test failure when SKILL.md is missing."""
        plugin_dir = tmp_path / ".claude" / "skills" / "bad-plugin"
        plugin_dir.mkdir(parents=True)

        validator = Validator(tmp_path)
        results = validator.check_plugins()

        assert 'bad-plugin' in results
        assert not results['bad-plugin'][0].passed
        assert "missing SKILL.md" in results['bad-plugin'][0].message


class TestCheckTemplates:
    """Tests for check_templates method."""

    def test_checks_specs_directory_structure(self, tmp_path):
        """Test specs directory structure validation."""
        (tmp_path / "specs" / "features").mkdir(parents=True)
        (tmp_path / "specs" / "api").mkdir(parents=True)

        validator = Validator(tmp_path)
        results = validator.check_templates()

        assert 'templates' in results
        # Should check for specs/features and specs/api
        passed = [r for r in results['templates'] if r.passed]
        assert len(passed) >= 2

    def test_detects_template_files(self, tmp_path):
        """Test template file detection."""
        (tmp_path / "specs" / "features").mkdir(parents=True)
        (tmp_path / "specs" / "api").mkdir(parents=True)
        (tmp_path / "specs" / "feature.template.md").write_text("# Template")
        (tmp_path / "specs" / "api.template.yaml").write_text("# API Template")

        validator = Validator(tmp_path)
        results = validator.check_templates()

        # Should detect both template files
        template_results = [r for r in results['templates'] if "Template:" in r.message]
        assert len(template_results) == 2


class TestCheckDocumentation:
    """Tests for check_documentation method."""

    def test_detects_readme(self, tmp_path):
        """Test README.md detection."""
        (tmp_path / "README.md").write_text("# Project")

        validator = Validator(tmp_path)
        results = validator.check_documentation()

        assert 'documentation' in results
        assert len(results['documentation']) > 0
        assert results['documentation'][0].passed

    def test_handles_missing_readme(self, tmp_path):
        """Test handling when README is missing."""
        validator = Validator(tmp_path)
        results = validator.check_documentation()

        # Should return empty list, not fail
        assert 'documentation' in results
        assert results['documentation'] == []


class TestCheckSpecsSummary:
    """Tests for check_specs_summary method."""

    def test_returns_none_when_no_specs_dir(self, tmp_path):
        """Test handling when specs/features doesn't exist."""
        validator = Validator(tmp_path)
        warning = validator.check_specs_summary()

        assert warning is None

    def test_returns_none_when_few_specs(self, tmp_path):
        """Test no warning for <3 specs."""
        specs_dir = tmp_path / "specs" / "features"
        specs_dir.mkdir(parents=True)

        # Create 2 spec files
        for i in range(2):
            (specs_dir / f"spec{i}.md").write_text("# Spec")

        validator = Validator(tmp_path)
        warning = validator.check_specs_summary()

        assert warning is None

    def test_warns_for_3_plus_specs_without_summary(self, tmp_path):
        """Test warning for 3+ specs without summary."""
        specs_dir = tmp_path / "specs" / "features"
        specs_dir.mkdir(parents=True)

        # Create 3 spec files
        for i in range(3):
            (specs_dir / f"spec{i}.md").write_text("# Spec")

        validator = Validator(tmp_path)
        warning = validator.check_specs_summary()

        assert warning is not None
        assert not warning.passed
        assert "SPECIFICATIONS_SUMMARY.md" in warning.message

    def test_no_warning_when_summary_exists(self, tmp_path):
        """Test no warning when summary exists."""
        specs_dir = tmp_path / "specs" / "features"
        specs_dir.mkdir(parents=True)

        # Create 3 spec files + summary
        for i in range(3):
            (specs_dir / f"spec{i}.md").write_text("# Spec")
        (tmp_path / "specs" / "SPECIFICATIONS_SUMMARY.md").write_text("# Summary")

        validator = Validator(tmp_path)
        warning = validator.check_specs_summary()

        assert warning is None


class TestRunAllChecks:
    """Tests for run_all_checks method."""

    def test_runs_all_check_methods(self, tmp_path):
        """Test that all check methods are called."""
        # Create minimal valid structure
        (tmp_path / "CLAUDE.md").write_text("# Constitution")
        (tmp_path / ".claude" / "skills" / "test-plugin").mkdir(parents=True)
        (tmp_path / ".claude" / "skills" / "test-plugin" / "SKILL.md").write_text("# Plugin")
        (tmp_path / "specs" / "features").mkdir(parents=True)
        (tmp_path / "specs" / "api").mkdir(parents=True)

        validator = Validator(tmp_path)
        results = validator.run_all_checks()

        # Should have results from all check methods
        assert 'core' in results
        assert 'test-plugin' in results
        assert 'templates' in results
        assert 'documentation' in results

    def test_resets_counters_on_each_run(self, tmp_path):
        """Test counters reset between runs."""
        (tmp_path / "CLAUDE.md").write_text("# Constitution")

        validator = Validator(tmp_path)

        # First run
        validator.run_all_checks()
        first_pass = validator.pass_count

        # Second run
        validator.run_all_checks()
        second_pass = validator.pass_count

        # Counts should be the same (not cumulative)
        assert first_pass == second_pass

    def test_counts_pass_fail_correctly(self, tmp_path):
        """Test pass/fail counting."""
        # Create structure with some passes and some fails
        (tmp_path / "CLAUDE.md").write_text("# Constitution")
        # Missing .claude/skills
        (tmp_path / "specs").mkdir()

        validator = Validator(tmp_path)
        validator.run_all_checks()

        assert validator.pass_count > 0
        assert validator.fail_count > 0


class TestGetExitCode:
    """Tests for get_exit_code method."""

    def test_returns_0_when_all_pass(self, tmp_path):
        """Test exit code 0 for success."""
        validator = Validator(tmp_path)
        validator.fail_count = 0

        assert validator.get_exit_code() == 0

    def test_returns_1_when_failures_exist(self, tmp_path):
        """Test exit code 1 for failures."""
        validator = Validator(tmp_path)
        validator.fail_count = 1

        assert validator.get_exit_code() == 1


class TestPrintResults:
    """Tests for print_results method."""

    def test_prints_without_error(self, tmp_path, capsys):
        """Test that print_results doesn't crash."""
        (tmp_path / "CLAUDE.md").write_text("# Constitution")
        (tmp_path / ".claude" / "skills" / "test").mkdir(parents=True)
        (tmp_path / "specs").mkdir()

        validator = Validator(tmp_path)
        results = validator.run_all_checks()
        validator.print_results(results)

        captured = capsys.readouterr()
        assert "Spec-Kit Verification" in captured.out

    def test_prints_core_files_section(self, tmp_path, capsys):
        """Test core files section is printed."""
        (tmp_path / "CLAUDE.md").write_text("# Constitution")
        (tmp_path / ".claude" / "skills" / "test").mkdir(parents=True)
        (tmp_path / "specs").mkdir()

        validator = Validator(tmp_path)
        results = validator.run_all_checks()
        validator.print_results(results)

        captured = capsys.readouterr()
        assert "Core Files:" in captured.out

    def test_verbose_mode_shows_all_results(self, tmp_path, capsys):
        """Test verbose mode prints all checks."""
        (tmp_path / "CLAUDE.md").write_text("# Constitution")
        (tmp_path / ".claude" / "skills" / "test").mkdir(parents=True)
        (tmp_path / "specs").mkdir()

        validator = Validator(tmp_path)
        results = validator.run_all_checks()
        validator.print_results(results, verbose=True)

        captured = capsys.readouterr()
        # Verbose should show passed checks
        assert len(captured.out) > 100  # Substantial output


class TestPrintJson:
    """Tests for print_json method."""

    def test_produces_valid_json(self, tmp_path, capsys):
        """Test JSON output is valid."""
        (tmp_path / "CLAUDE.md").write_text("# Constitution")
        (tmp_path / ".claude" / "skills" / "test").mkdir(parents=True)
        (tmp_path / "specs").mkdir()

        validator = Validator(tmp_path)
        results = validator.run_all_checks()
        validator.print_json(results)

        captured = capsys.readouterr()
        output = json.loads(captured.out)

        assert 'valid' in output
        assert 'pass_count' in output
        assert 'fail_count' in output
        assert 'checks' in output

    def test_json_includes_all_results(self, tmp_path, capsys):
        """Test JSON includes all check categories."""
        (tmp_path / "CLAUDE.md").write_text("# Constitution")
        (tmp_path / ".claude" / "skills" / "test-plugin").mkdir(parents=True)
        (tmp_path / ".claude" / "skills" / "test-plugin" / "SKILL.md").write_text("# Plugin")
        (tmp_path / "specs" / "features").mkdir(parents=True)
        (tmp_path / "specs" / "api").mkdir(parents=True)

        validator = Validator(tmp_path)
        results = validator.run_all_checks()
        validator.print_json(results)

        captured = capsys.readouterr()
        output = json.loads(captured.out)

        assert 'core' in output['checks']
        assert 'templates' in output['checks']

    def test_json_valid_key_reflects_fail_count(self, tmp_path, capsys):
        """Test valid key is false when failures exist."""
        # Create incomplete structure
        (tmp_path / "CLAUDE.md").write_text("# Constitution")

        validator = Validator(tmp_path)
        results = validator.run_all_checks()
        validator.print_json(results)

        captured = capsys.readouterr()
        output = json.loads(captured.out)

        # Should have failures, so valid should be False
        assert output['valid'] is False
        assert output['fail_count'] > 0
