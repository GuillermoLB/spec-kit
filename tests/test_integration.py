"""Integration tests for spec-kit workflows.

These tests validate complete end-to-end workflows using real filesystem
operations (via tmp_path fixture) rather than mocking.
"""

import pytest
from pathlib import Path

from spec_kit.core.installer import Installer
from spec_kit.core.validator import Validator


class TestFullInstallationWorkflow:
    """Tests for complete installation workflow."""

    def test_installs_core_files_successfully(self, mock_spec_kit_root, mock_target_dir):
        """Test full installation creates all core files."""
        installer = Installer(mock_target_dir, mock_spec_kit_root)

        # Run complete installation
        installer.run_installation(
            plugins=['api-development'],
            force=False,
            interactive=False
        )

        # Verify core files installed
        assert (mock_target_dir / "CLAUDE.md").exists()
        assert (mock_target_dir / "CLAUDE.md").is_file()

        # Verify directory structure
        assert (mock_target_dir / ".claude" / "skills").exists()
        assert (mock_target_dir / ".claude" / "skills").is_dir()

        assert (mock_target_dir / "specs" / "features").exists()
        assert (mock_target_dir / "specs" / "api").exists()

        # Verify .gitignore created and updated
        assert (mock_target_dir / ".gitignore").exists()
        gitignore_content = (mock_target_dir / ".gitignore").read_text()
        assert ".spec-kit-templates/" in gitignore_content

    def test_installs_plugin_files(self, mock_spec_kit_root, mock_target_dir):
        """Test plugin installation creates plugin files."""
        installer = Installer(mock_target_dir, mock_spec_kit_root)

        installer.run_installation(
            plugins=['api-development'],
            force=False,
            interactive=False
        )

        # Verify plugin skill file
        skill_file = mock_target_dir / ".claude" / "skills" / "api-development" / "SKILL.md"
        assert skill_file.exists()
        assert skill_file.is_file()
        assert len(skill_file.read_text()) > 0

        # Verify plugin references
        references_dir = mock_target_dir / ".claude" / "skills" / "api-development" / "references"
        assert references_dir.exists()
        assert (references_dir / "fastapi-endpoint.py").exists()

        # Verify templates directory
        templates_dir = mock_target_dir / ".spec-kit-templates" / "api-development"
        assert templates_dir.exists()

    def test_installs_multiple_plugins(self, mock_spec_kit_root, mock_target_dir):
        """Test installing multiple plugins."""
        installer = Installer(mock_target_dir, mock_spec_kit_root)

        installer.run_installation(
            plugins=['api-development', 'ai-app'],
            force=False,
            interactive=False
        )

        # Verify both plugins installed
        assert (mock_target_dir / ".claude" / "skills" / "api-development" / "SKILL.md").exists()
        assert (mock_target_dir / ".claude" / "skills" / "ai-app" / "SKILL.md").exists()

    def test_installs_spec_templates(self, mock_spec_kit_root, mock_target_dir):
        """Test spec templates are installed."""
        installer = Installer(mock_target_dir, mock_spec_kit_root)

        installer.run_installation(
            plugins=['api-development'],
            force=False,
            interactive=False
        )

        # Verify template files
        assert (mock_target_dir / "specs" / "feature.template.md").exists()
        assert (mock_target_dir / "specs" / "api.template.yaml").exists()
        assert (mock_target_dir / "specs" / "specifications-summary.template.md").exists()

    def test_force_flag_overwrites_existing(self, mock_spec_kit_root, mock_target_dir):
        """Test --force flag allows overwriting."""
        # First installation
        installer1 = Installer(mock_target_dir, mock_spec_kit_root)
        installer1.run_installation(
            plugins=['api-development'],
            force=False,
            interactive=False
        )

        # Modify CLAUDE.md
        claude_md = mock_target_dir / "CLAUDE.md"
        claude_md.write_text("Modified content")

        # Second installation with force
        installer2 = Installer(mock_target_dir, mock_spec_kit_root)
        installer2.run_installation(
            plugins=['api-development'],
            force=True,
            interactive=False
        )

        # CLAUDE.md should be restored
        content = claude_md.read_text()
        assert "Modified content" not in content
        assert "Spec-Driven Development" in content or "Constitution" in content


class TestFullVerificationWorkflow:
    """Tests for complete verification workflow."""

    def test_validates_complete_installation(self, installed_project):
        """Test verification passes for complete installation."""
        validator = Validator(installed_project)

        results = validator.run_all_checks()

        # Should have core results
        assert 'core' in results
        assert len(results['core']) > 0

        # Should have plugin results
        assert 'api-development' in results

        # All core checks should pass
        core_failures = [r for r in results['core'] if not r.passed]
        # Note: Empty skills warning might fail, but core files should pass
        assert len(core_failures) <= 1  # At most the empty warning

    def test_reports_exit_code_0_for_valid_install(self, installed_project):
        """Test validator returns 0 for valid installation."""
        validator = Validator(installed_project)

        validator.run_all_checks()
        exit_code = validator.get_exit_code()

        assert exit_code == 0

    def test_detects_missing_core_file(self, installed_project):
        """Test validation detects missing core files."""
        # Remove CLAUDE.md
        (installed_project / "CLAUDE.md").unlink()

        validator = Validator(installed_project)
        results = validator.run_all_checks()

        # Should detect missing CLAUDE.md
        assert validator.fail_count > 0
        assert validator.get_exit_code() == 1

    def test_detects_missing_plugin_file(self, installed_project):
        """Test validation detects missing plugin files."""
        # Remove plugin SKILL.md
        skill_file = installed_project / ".claude" / "skills" / "api-development" / "SKILL.md"
        skill_file.unlink()

        validator = Validator(installed_project)
        results = validator.run_all_checks()

        # Should detect missing SKILL.md
        assert 'api-development' in results
        plugin_failures = [r for r in results['api-development'] if not r.passed]
        assert len(plugin_failures) > 0

    def test_warns_for_missing_specs_summary(self, installed_project):
        """Test warning for missing SPECIFICATIONS_SUMMARY.md."""
        specs_dir = installed_project / "specs" / "features"

        # Create 3+ spec files
        for i in range(3):
            (specs_dir / f"spec{i}.md").write_text(f"# Spec {i}")

        validator = Validator(installed_project)
        results = validator.run_all_checks()

        # Should have specs warning
        assert 'specs_warning' in results
        assert "SPECIFICATIONS_SUMMARY" in results['specs_warning'].message


class TestCliIntegration:
    """Tests for CLI commands working together."""

    def test_init_then_verify_succeeds(self, mock_spec_kit_root, tmp_path):
        """Test init followed by verify."""
        target = tmp_path / "project"
        target.mkdir()

        # Run init
        installer = Installer(target, mock_spec_kit_root)
        installer.run_installation(
            plugins=['api-development'],
            force=False,
            interactive=False
        )

        # Run verify
        validator = Validator(target)
        results = validator.run_all_checks()

        # Verification should pass
        assert validator.get_exit_code() == 0
        assert validator.pass_count > 0

    def test_verify_detects_incomplete_manual_setup(self, tmp_path):
        """Test verify detects incomplete manual installation."""
        # Create partial structure manually
        (tmp_path / "CLAUDE.md").write_text("# Constitution")
        # Missing .claude/skills and specs

        validator = Validator(tmp_path)
        results = validator.run_all_checks()

        # Should fail validation
        assert validator.fail_count > 0
        assert validator.get_exit_code() == 1

    def test_verify_handles_empty_directory(self, tmp_path):
        """Test verify handles completely empty directory."""
        validator = Validator(tmp_path)
        results = validator.run_all_checks()

        # Should have failures
        assert validator.fail_count > 0
        assert validator.get_exit_code() == 1


class TestErrorRecovery:
    """Tests for error handling and recovery."""

    def test_installer_validates_before_installation(self, mock_spec_kit_root, tmp_path):
        """Test installer validates environment before proceeding."""
        target = tmp_path / "project"
        target.mkdir()

        installer = Installer(target, mock_spec_kit_root)

        # Should validate without error
        installer.validate_environment()
        installer.validate_target()

    def test_installer_rejects_nonexistent_target(self, mock_spec_kit_root, tmp_path):
        """Test installer rejects non-existent target directory."""
        bad_target = tmp_path / "nonexistent"

        installer = Installer(bad_target, mock_spec_kit_root)

        with pytest.raises(FileNotFoundError):
            installer.validate_target()

    def test_installer_rejects_existing_without_force(self, mock_spec_kit_root, tmp_path):
        """Test installer rejects existing CLAUDE.md without --force."""
        target = tmp_path / "project"
        target.mkdir()
        (target / "CLAUDE.md").write_text("Existing")

        installer = Installer(target, mock_spec_kit_root)

        with pytest.raises(FileExistsError):
            installer.validate_target(force=False)

    def test_gitignore_update_is_idempotent(self, mock_spec_kit_root, mock_target_dir):
        """Test gitignore updates don't duplicate entries."""
        installer = Installer(mock_target_dir, mock_spec_kit_root)

        # Run twice
        installer.update_project_gitignore()
        installer.update_project_gitignore()

        gitignore = (mock_target_dir / ".gitignore").read_text()

        # Should only appear once
        assert gitignore.count(".spec-kit-templates/") == 1


class TestPluginResolution:
    """Tests for plugin name and alias resolution."""

    def test_resolves_plugin_aliases(self, mock_spec_kit_root, mock_target_dir):
        """Test plugin aliases resolve to full names."""
        installer = Installer(mock_target_dir, mock_spec_kit_root)

        resolved = installer.select_plugins_from_args(['api', 'ai'])

        assert resolved == ['api-development', 'ai-app']

    def test_accepts_full_plugin_names(self, mock_spec_kit_root, mock_target_dir):
        """Test full plugin names are accepted."""
        installer = Installer(mock_target_dir, mock_spec_kit_root)

        resolved = installer.select_plugins_from_args(['api-development', 'ai-app'])

        assert resolved == ['api-development', 'ai-app']

    def test_handles_mixed_names_and_aliases(self, mock_spec_kit_root, mock_target_dir):
        """Test mix of names and aliases."""
        installer = Installer(mock_target_dir, mock_spec_kit_root)

        resolved = installer.select_plugins_from_args(['api', 'ai-app'])

        assert resolved == ['api-development', 'ai-app']

    def test_rejects_invalid_plugin_names(self, mock_spec_kit_root, mock_target_dir):
        """Test invalid plugin names raise ValueError."""
        installer = Installer(mock_target_dir, mock_spec_kit_root)

        with pytest.raises(ValueError, match="Unknown plugin"):
            installer.select_plugins_from_args(['invalid-plugin'])
