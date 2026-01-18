"""Unit tests for spec_kit.core.installer module."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from spec_kit.core.installer import Installer, AVAILABLE_PLUGINS


class TestInstallerInitialization:
    """Tests for Installer class initialization."""

    def test_init_with_valid_spec_kit_root(self, mock_spec_kit_root, mock_target_dir):
        """Test that installer initializes with valid spec-kit root."""
        installer = Installer(mock_target_dir, mock_spec_kit_root)

        assert installer.target_path == mock_target_dir
        assert installer.spec_kit_root == mock_spec_kit_root
        assert installer.selected_plugins == []

    def test_init_raises_without_core_claude_md(self, tmp_path, mock_target_dir):
        """Test that validation fails if core/CLAUDE.md is missing."""
        # Create root without core/CLAUDE.md
        bad_root = tmp_path / "bad-root"
        bad_root.mkdir()

        installer = Installer(mock_target_dir, bad_root)
        with pytest.raises(FileNotFoundError, match="Cannot find spec-kit core files"):
            installer.validate_environment()

    def test_init_auto_detects_spec_kit_root(self, mock_target_dir):
        """Test that spec-kit root can be auto-detected."""
        # When spec_kit_root is None, it should call find_spec_kit_root
        with patch('spec_kit.core.installer.find_spec_kit_root') as mock_find:
            mock_find.return_value = None  # Return None to trigger RuntimeError

            # Should raise because find_spec_kit_root returned None
            with pytest.raises(RuntimeError, match="Cannot find spec-kit installation"):
                Installer(mock_target_dir, None)


class TestValidateEnvironment:
    """Tests for validate_environment method."""

    def test_passes_with_valid_environment(self, installer):
        """Test validation passes with proper spec-kit structure."""
        # Should not raise
        installer.validate_environment()

    def test_fails_without_core_claude_md(self, installer, mock_spec_kit_root):
        """Test validation fails if CLAUDE.md is removed."""
        # Remove CLAUDE.md
        (mock_spec_kit_root / "core" / "CLAUDE.md").unlink()

        with pytest.raises(FileNotFoundError, match="Cannot find spec-kit core files"):
            installer.validate_environment()


class TestValidateTarget:
    """Tests for validate_target method."""

    def test_validates_existing_empty_directory(self, installer):
        """Test that validation passes for existing empty directory."""
        # Should not raise
        installer.validate_target()

    def test_raises_for_nonexistent_directory(self, installer, tmp_path):
        """Test that validation fails for non-existent directory."""
        installer.target_path = tmp_path / "nonexistent"

        with pytest.raises(FileNotFoundError, match="Target directory does not exist"):
            installer.validate_target()

    def test_raises_for_file_instead_of_directory(self, installer, tmp_path):
        """Test that validation fails if target is a file."""
        file_path = tmp_path / "somefile.txt"
        file_path.write_text("content")
        installer.target_path = file_path

        with pytest.raises(NotADirectoryError, match="Target path is not a directory"):
            installer.validate_target()

    def test_raises_for_existing_claude_md_without_force(self, installer, mock_target_dir):
        """Test that validation fails if CLAUDE.md exists and force=False."""
        (mock_target_dir / "CLAUDE.md").write_text("existing")

        with pytest.raises(FileExistsError, match="CLAUDE.md already exists"):
            installer.validate_target(force=False)

    def test_passes_with_existing_claude_md_and_force(self, installer, mock_target_dir):
        """Test that validation passes if CLAUDE.md exists but force=True."""
        (mock_target_dir / "CLAUDE.md").write_text("existing")

        # Should not raise
        installer.validate_target(force=True)


class TestPluginSelection:
    """Tests for plugin selection methods."""

    def test_select_plugins_from_args_resolves_full_names(self, installer):
        """Test that plugin full names are recognized."""
        result = installer.select_plugins_from_args(['api-development', 'ai-app'])

        assert result == ['api-development', 'ai-app']
        assert installer.selected_plugins == ['api-development', 'ai-app']

    def test_select_plugins_from_args_resolves_aliases(self, installer):
        """Test that plugin aliases are resolved to full names."""
        result = installer.select_plugins_from_args(['api', 'ai'])

        assert result == ['api-development', 'ai-app']

    def test_select_plugins_from_args_handles_mixed(self, installer):
        """Test that mix of full names and aliases works."""
        result = installer.select_plugins_from_args(['api', 'ai-app'])

        assert result == ['api-development', 'ai-app']

    def test_select_plugins_from_args_raises_on_invalid(self, installer):
        """Test that invalid plugin names raise ValueError."""
        with pytest.raises(ValueError, match="Unknown plugin: invalid-plugin"):
            installer.select_plugins_from_args(['invalid-plugin'])

    def test_select_plugins_interactive_prompts_user(self, installer, monkeypatch):
        """Test interactive plugin selection."""
        # Mock user input: select plugins 1 and 2
        monkeypatch.setattr('builtins.input', lambda _: '1 2')

        result = installer.select_plugins_interactive()

        assert 'api-development' in result
        assert 'ai-app' in result

    def test_select_plugins_interactive_handles_all(self, installer, monkeypatch):
        """Test that 'all' selection works."""
        monkeypatch.setattr('builtins.input', lambda _: 'all')

        result = installer.select_plugins_interactive()

        assert 'api-development' in result
        assert 'ai-app' in result

    def test_select_plugins_interactive_retries_on_invalid(self, installer, monkeypatch):
        """Test that invalid input prompts retry."""
        inputs = iter(['invalid', '1'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        result = installer.select_plugins_interactive()

        assert 'api-development' in result


class TestInstallCore:
    """Tests for install_core method."""

    def test_copies_claude_md(self, installer, mock_target_dir, mock_spec_kit_root):
        """Test that CLAUDE.md is copied."""
        installer.install_core()

        claude_md = mock_target_dir / "CLAUDE.md"
        assert claude_md.exists()
        assert claude_md.read_text() == (mock_spec_kit_root / "core" / "CLAUDE.md").read_text()

    def test_creates_claude_skills_directory(self, installer, mock_target_dir):
        """Test that .claude/skills directory is created."""
        installer.install_core()

        skills_dir = mock_target_dir / ".claude" / "skills"
        assert skills_dir.exists()
        assert skills_dir.is_dir()

    def test_creates_specs_directory_structure(self, installer, mock_target_dir):
        """Test that specs directory structure is created."""
        installer.install_core()

        assert (mock_target_dir / "specs" / "features").exists()
        assert (mock_target_dir / "specs" / "api").exists()


class TestInstallPlugins:
    """Tests for install_plugins method."""

    def test_installs_plugin_skill_file(self, installer, mock_target_dir):
        """Test that plugin SKILL.md is installed."""
        installer.selected_plugins = ['api-development']
        installer.install_plugins()

        skill_file = mock_target_dir / ".claude" / "skills" / "api-development" / "SKILL.md"
        assert skill_file.exists()

    def test_installs_plugin_templates_to_references(self, installer, mock_target_dir):
        """Test that plugin templates are copied to references directory."""
        installer.selected_plugins = ['api-development']
        installer.install_plugins()

        references_dir = mock_target_dir / ".claude" / "skills" / "api-development" / "references"
        assert references_dir.exists()
        assert (references_dir / "fastapi-endpoint.py").exists()
        assert (references_dir / "sam-template.yaml").exists()

    def test_installs_templates_to_spec_kit_templates(self, installer, mock_target_dir):
        """Test that templates are also copied to .spec-kit-templates."""
        installer.selected_plugins = ['api-development']
        installer.install_plugins()

        templates_dir = mock_target_dir / ".spec-kit-templates" / "api-development"
        assert templates_dir.exists()
        assert (templates_dir / "fastapi-endpoint.py").exists()

    def test_installs_multiple_plugins(self, installer, mock_target_dir):
        """Test installing multiple plugins."""
        installer.selected_plugins = ['api-development', 'ai-app']
        installer.install_plugins()

        assert (mock_target_dir / ".claude" / "skills" / "api-development" / "SKILL.md").exists()
        assert (mock_target_dir / ".claude" / "skills" / "ai-app" / "SKILL.md").exists()

    def test_handles_missing_plugin_gracefully(self, installer, mock_target_dir, capsys):
        """Test that missing plugin is skipped with warning."""
        installer.selected_plugins = ['nonexistent-plugin']
        installer.install_plugins()

        captured = capsys.readouterr()
        # Should warn but not crash


class TestInstallTemplates:
    """Tests for install_templates method."""

    def test_installs_spec_templates(self, installer, mock_target_dir):
        """Test that spec templates are installed."""
        installer.install_templates()

        assert (mock_target_dir / "specs" / "feature.template.md").exists()
        assert (mock_target_dir / "specs" / "api.template.yaml").exists()
        assert (mock_target_dir / "specs" / "specifications-summary.template.md").exists()


class TestUpdateProjectGitignore:
    """Tests for update_project_gitignore method."""

    def test_creates_gitignore_if_missing(self, installer, mock_target_dir):
        """Test that .gitignore is created if it doesn't exist."""
        installer.update_project_gitignore()

        gitignore = mock_target_dir / ".gitignore"
        assert gitignore.exists()
        assert ".spec-kit-templates/" in gitignore.read_text()

    def test_appends_to_existing_gitignore(self, installer, mock_target_dir):
        """Test that entries are appended to existing .gitignore."""
        gitignore = mock_target_dir / ".gitignore"
        gitignore.write_text("*.pyc\n")

        installer.update_project_gitignore()

        content = gitignore.read_text()
        assert "*.pyc" in content
        assert ".spec-kit-templates/" in content

    def test_is_idempotent(self, installer, mock_target_dir):
        """Test that running twice doesn't duplicate entries."""
        installer.update_project_gitignore()
        installer.update_project_gitignore()

        gitignore = mock_target_dir / ".gitignore"
        content = gitignore.read_text()
        assert content.count(".spec-kit-templates/") == 1


class TestRunInstallation:
    """Tests for run_installation method (integration-like)."""

    def test_completes_full_installation(self, installer):
        """Test that full installation workflow completes."""
        installer.run_installation(
            plugins=['api-development'],
            force=False,
            interactive=False
        )

        target = installer.target_path

        # Verify all components installed
        assert (target / "CLAUDE.md").exists()
        assert (target / ".claude" / "skills").exists()
        assert (target / "specs" / "features").exists()
        assert (target / ".gitignore").exists()
        assert (target / ".claude" / "skills" / "api-development" / "SKILL.md").exists()

    def test_uses_default_plugin_when_none_specified(self, installer):
        """Test that default plugin is used in non-interactive mode."""
        installer.run_installation(
            plugins=None,
            force=False,
            interactive=False
        )

        # Should install api-development by default
        assert (installer.target_path / ".claude" / "skills" / "api-development" / "SKILL.md").exists()


class TestPluginMetadata:
    """Tests for AVAILABLE_PLUGINS constant."""

    def test_has_required_plugins(self):
        """Test that required plugins are defined."""
        assert 'api-development' in AVAILABLE_PLUGINS
        assert 'ai-app' in AVAILABLE_PLUGINS

    def test_plugins_have_required_fields(self):
        """Test that each plugin has required metadata fields."""
        for plugin_name, plugin_info in AVAILABLE_PLUGINS.items():
            assert 'name' in plugin_info
            assert 'aliases' in plugin_info
            assert 'description' in plugin_info
            assert 'skill_command' in plugin_info

    def test_aliases_are_lists(self):
        """Test that plugin aliases are lists."""
        for plugin_info in AVAILABLE_PLUGINS.values():
            assert isinstance(plugin_info['aliases'], list)
