"""Pytest configuration and fixtures for spec-kit tests."""

import pytest
from pathlib import Path


@pytest.fixture
def mock_spec_kit_root(tmp_path):
    """Create a mock spec-kit installation structure.

    This fixture creates a complete mock spec-kit directory with:
    - core/CLAUDE.md
    - plugins (api-development, ai-app) with SKILL.md and templates
    - templates/specs with template files

    Returns:
        Path: Root directory of the mock spec-kit installation
    """
    root = tmp_path / "spec-kit"

    # Create core/CLAUDE.md
    core_dir = root / "core"
    core_dir.mkdir(parents=True)
    claude_md = core_dir / "CLAUDE.md"
    claude_md.write_text("# Spec-Driven Development Constitution\n\nMock constitution for testing.")

    # Create plugins
    plugins_dir = root / "plugins"

    # api-development plugin
    api_plugin = plugins_dir / "api-development"
    api_plugin.mkdir(parents=True)
    (api_plugin / "skill.md").write_text("# API Development Skill\n\nMock skill content.")

    api_templates = api_plugin / "templates"
    api_templates.mkdir()
    (api_templates / "fastapi-endpoint.py").write_text("# Mock FastAPI template\n")
    (api_templates / "sam-template.yaml").write_text("# Mock SAM template\n")

    # ai-app plugin
    ai_plugin = plugins_dir / "ai-app"
    ai_plugin.mkdir(parents=True)
    (ai_plugin / "skill.md").write_text("# AI App Skill\n\nMock skill content.")

    ai_templates = ai_plugin / "templates"
    ai_templates.mkdir()
    (ai_templates / "anthropic-client.py").write_text("# Mock Anthropic client\n")
    (ai_templates / "prompt-patterns.md").write_text("# Mock prompt patterns\n")

    # Create templates/specs
    specs_templates = root / "templates" / "specs"
    specs_templates.mkdir(parents=True)
    (specs_templates / "feature.template.md").write_text("# Feature Template\n\nMock feature template.")
    (specs_templates / "api.template.yaml").write_text("# Mock API template\n")
    (specs_templates / "specifications-summary.template.md").write_text("# Specifications Summary\n\nMock summary.")

    return root


@pytest.fixture
def mock_target_dir(tmp_path):
    """Create an empty target directory for installation.

    Returns:
        Path: Empty directory to use as installation target
    """
    target = tmp_path / "target-project"
    target.mkdir()
    return target


@pytest.fixture
def installer(mock_spec_kit_root, mock_target_dir):
    """Create an Installer instance with mocked paths.

    Args:
        mock_spec_kit_root: Fixture providing mock spec-kit root
        mock_target_dir: Fixture providing empty target directory

    Returns:
        Installer: Configured installer instance ready for testing
    """
    from spec_kit.core.installer import Installer
    return Installer(target_path=mock_target_dir, spec_kit_root=mock_spec_kit_root)


@pytest.fixture
def validator(mock_target_dir):
    """Create a Validator instance with a target directory.

    Args:
        mock_target_dir: Fixture providing target directory

    Returns:
        Validator: Configured validator instance ready for testing
    """
    from spec_kit.core.validator import Validator
    return Validator(target_path=mock_target_dir)


@pytest.fixture
def installed_project(mock_spec_kit_root, mock_target_dir):
    """Create a fully installed spec-kit project for testing.

    This fixture runs a complete installation workflow to create
    a valid spec-kit project structure for integration testing.

    Args:
        mock_spec_kit_root: Fixture providing mock spec-kit root
        mock_target_dir: Fixture providing empty target directory

    Returns:
        Path: Path to the installed project directory
    """
    from spec_kit.core.installer import Installer

    installer = Installer(target_path=mock_target_dir, spec_kit_root=mock_spec_kit_root)
    installer.run_installation(
        plugins=['api-development'],
        force=False,
        interactive=False
    )

    return mock_target_dir
