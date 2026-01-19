"""Installation logic for spec-kit.

Provides the core installation functionality, wrapping the bash install.sh
logic in a Python implementation with better error handling and UX.
"""

import os
from pathlib import Path
from typing import List, Optional, Dict

from spec_kit.utils import colors
from spec_kit.utils.file_ops import (
    ensure_directory,
    safe_copy_file,
    safe_copy_tree,
    validate_path,
    find_spec_kit_root,
    update_gitignore,
    get_gitignore_entries,
)


# Plugin metadata
AVAILABLE_PLUGINS = {
    'api-development': {
        'name': 'api-development',
        'aliases': ['api'],
        'description': 'FastAPI + AWS SAM/Lambda patterns',
        'skill_command': '/api-development or /api',
    },
    'ai-app': {
        'name': 'ai-app',
        'aliases': ['ai'],
        'description': 'LLM integration (Claude, OpenAI)',
        'skill_command': '/ai-app',
    },
}


class Installer:
    """Handles spec-kit installation into target projects."""

    def __init__(self, target_path: Path, spec_kit_root: Optional[Path] = None):
        """Initialize installer.

        Args:
            target_path: Target directory for installation
            spec_kit_root: Spec-kit source directory (auto-detected if None)
        """
        self.target_path = target_path.resolve()
        self.spec_kit_root = spec_kit_root or find_spec_kit_root()
        self.selected_plugins: List[str] = []

        if self.spec_kit_root is None:
            raise RuntimeError(
                "Cannot find spec-kit installation directory. "
                "Please ensure spec-kit is properly installed."
            )

    def validate_environment(self) -> None:
        """Validate spec-kit source files exist.

        Raises:
            FileNotFoundError: If core spec-kit files are missing
        """
        core_file = self.spec_kit_root / "core" / "CLAUDE.md"
        if not core_file.exists():
            raise FileNotFoundError(
                f"Cannot find spec-kit core files at {self.spec_kit_root}\n"
                f"Expected {core_file} to exist.\n"
                f"Please ensure spec-kit is properly installed."
            )

        colors.success("Validated spec-kit source files")

    def validate_target(self, force: bool = False) -> None:
        """Validate target directory.

        Args:
            force: If True, allow overwriting existing installation

        Raises:
            FileNotFoundError: If target directory doesn't exist
            FileExistsError: If installation already exists and force=False
        """
        if not self.target_path.exists():
            raise FileNotFoundError(
                f"Target directory does not exist: {self.target_path}\n"
                f"Please create the directory first or specify a valid path."
            )

        if not self.target_path.is_dir():
            raise NotADirectoryError(
                f"Target path is not a directory: {self.target_path}"
            )

        # Check if CLAUDE.md already exists
        claude_md = self.target_path / "CLAUDE.md"
        if claude_md.exists() and not force:
            raise FileExistsError(
                f"CLAUDE.md already exists in {self.target_path}\n"
                f"Use --force to overwrite the existing installation."
            )

        colors.success(f"Target directory validated: {self.target_path}")

    def select_plugins_interactive(self) -> List[str]:
        """Interactively select plugins to install.

        Returns:
            List of selected plugin names
        """
        colors.info("Available plugins:")
        print()

        # Display options
        plugin_list = list(AVAILABLE_PLUGINS.values())
        for idx, plugin_info in enumerate(plugin_list, 1):
            print(f"  {idx}) {plugin_info['name']:<20} - {plugin_info['description']}")
        print(f"  {len(plugin_list) + 1}) all                  - Install all plugins")
        print()

        # Get user input
        while True:
            try:
                selection = input(
                    "Enter plugin numbers (space-separated, e.g., '1 2') or 'all': "
                ).strip()

                if selection.lower() == 'all':
                    selected = [p['name'] for p in plugin_list]
                    break

                # Parse numbers
                numbers = [int(x.strip()) for x in selection.split()]
                selected = []
                for num in numbers:
                    if 1 <= num <= len(plugin_list):
                        selected.append(plugin_list[num - 1]['name'])
                    else:
                        colors.warning(f"Invalid plugin number: {num} (skipping)")

                if selected:
                    break
                else:
                    colors.error("No valid plugins selected. Please try again.")

            except ValueError:
                colors.error("Invalid input. Please enter numbers separated by spaces.")
            except KeyboardInterrupt:
                print()
                colors.info("Installation cancelled")
                raise SystemExit(0)

        self.selected_plugins = selected
        print()
        colors.info(f"Selected plugins: {', '.join(selected)}")
        print()
        return selected

    def select_plugins_from_args(self, plugins: List[str]) -> List[str]:
        """Select plugins from command-line arguments.

        Args:
            plugins: List of plugin names or aliases

        Returns:
            List of resolved plugin names

        Raises:
            ValueError: If unknown plugin specified
        """
        resolved = []
        for plugin in plugins:
            plugin = plugin.strip().lower()

            # Check if it's a direct name
            if plugin in AVAILABLE_PLUGINS:
                resolved.append(plugin)
                continue

            # Check if it's an alias
            found = False
            for plugin_info in AVAILABLE_PLUGINS.values():
                if plugin in plugin_info.get('aliases', []):
                    resolved.append(plugin_info['name'])
                    found = True
                    break

            if not found:
                available = ', '.join(AVAILABLE_PLUGINS.keys())
                raise ValueError(
                    f"Unknown plugin: {plugin}\n"
                    f"Available plugins: {available}"
                )

        self.selected_plugins = resolved
        return resolved

    def install_core(self) -> None:
        """Install core spec-kit files."""
        colors.info("Installing core files...")

        # Copy CLAUDE.md
        src_claude = self.spec_kit_root / "core" / "CLAUDE.md"
        dest_claude = self.target_path / "CLAUDE.md"
        safe_copy_file(src_claude, dest_claude, force=True)
        colors.success("Installed CLAUDE.md")

        # Create .claude/skills directory
        claude_dir = self.target_path / ".claude" / "skills"
        ensure_directory(claude_dir)
        colors.success("Created .claude/skills directory")

        # Create specs directory structure
        ensure_directory(self.target_path / "specs" / "features")
        ensure_directory(self.target_path / "specs" / "api")
        colors.success("Created specs directory structure")

    def install_plugins(self, plugins: Optional[List[str]] = None) -> None:
        """Install selected plugins.

        Args:
            plugins: List of plugin names (uses self.selected_plugins if None)
        """
        if plugins is None:
            plugins = self.selected_plugins

        if not plugins:
            colors.warning("No plugins selected for installation")
            return

        colors.info("Installing plugins...")

        for plugin in plugins:
            plugin_src = self.spec_kit_root / "plugins" / plugin

            if not plugin_src.exists():
                colors.warning(f"Plugin not found: {plugin} (skipping)")
                continue

            # Create plugin directory following official Claude Code convention
            plugin_dest = self.target_path / ".claude" / "skills" / plugin
            ensure_directory(plugin_dest)

            # Copy skill file as SKILL.md (official naming convention)
            skill_src = plugin_src / "skill.md"
            skill_dest = plugin_dest / "SKILL.md"

            if not skill_src.exists():
                colors.warning(f"Skill file not found for {plugin}: {skill_src} (skipping)")
                continue

            safe_copy_file(skill_src, skill_dest, force=True)
            colors.success(f"Installed plugin: {plugin}")

            # Copy templates to references/ (following official pattern)
            templates_src = plugin_src / "templates"
            if templates_src.exists() and templates_src.is_dir():
                references_dest = plugin_dest / "references"
                ensure_directory(references_dest)
                safe_copy_tree(templates_src, references_dest, force=True)
                colors.success("  └─ Added references with templates")

                # Also keep a copy in .spec-kit-templates for easy access
                template_dest = self.target_path / ".spec-kit-templates" / plugin
                ensure_directory(template_dest)
                safe_copy_tree(templates_src, template_dest, force=True)

    def install_templates(self) -> None:
        """Install spec templates."""
        colors.info("Installing spec templates...")

        templates_src = self.spec_kit_root / "templates" / "specs"
        specs_dest = self.target_path / "specs"

        if not templates_src.exists():
            colors.warning("No spec templates found (skipping)")
            return

        # Copy template files to specs directory
        try:
            safe_copy_tree(templates_src, specs_dest, force=True)
            colors.success("Installed spec templates")
        except Exception as e:
            colors.warning(f"Could not install spec templates: {e}")

    def offer_architecture_doc(self, interactive: bool = True) -> None:
        """Optionally create architecture.md from template.

        Args:
            interactive: If True, prompt user; if False, skip
        """
        if not interactive:
            return

        print()
        colors.info("Would you like to create a system architecture document?")
        print()
        print("  This creates specs/architecture.md to document:")
        print("  - Core architectural principles")
        print("  - System design and component structure")
        print("  - Key architectural decisions")
        print()

        try:
            response = input("Create architecture.md? (y/n): ").strip().lower()
            print()

            if response in ('y', 'yes'):
                arch_template = self.spec_kit_root / "templates" / "specs" / "architecture.template.md"
                arch_dest = self.target_path / "specs" / "architecture.md"

                if arch_template.exists():
                    safe_copy_file(arch_template, arch_dest, force=True)
                    colors.success("Created specs/architecture.md")
                    print()
                    colors.info("Next: Edit specs/architecture.md with your project's architecture")
                else:
                    colors.warning("architecture.template.md not found, skipping")
            else:
                colors.info("Skipped architecture.md (create later from templates/specs/architecture.template.md)")
            print()

        except KeyboardInterrupt:
            print()
            colors.info("Skipped architecture.md")
            print()

    def update_project_gitignore(self) -> None:
        """Update .gitignore with spec-kit entries."""
        entries = get_gitignore_entries()
        modified = update_gitignore(self.target_path, entries)

        if modified:
            colors.success("Updated .gitignore")
        else:
            colors.info(".gitignore already up to date")

    def print_summary(self) -> None:
        """Print installation summary."""
        print()
        colors.print_header("Installation Complete!", "🎉")
        print()
        colors.info(f"Installed in: {self.target_path}")
        print()

        print("Files created:")
        print("  • CLAUDE.md                    - Core spec-driven workflow")
        print("  • .claude/skills/              - Plugin skills (official structure)")
        print("  • specs/                       - Specification directory")
        print("  • .spec-kit-templates/         - Quick reference templates")
        print()

        if self.selected_plugins:
            print("Installed plugins:")
            for plugin in self.selected_plugins:
                plugin_info = AVAILABLE_PLUGINS.get(plugin, {})
                skill_cmd = plugin_info.get('skill_command', f'/{plugin}')
                desc = plugin_info.get('description', 'Plugin')
                print(f"  • {skill_cmd:<28} - {desc}")
            print()

            print("Plugin structure (official Claude Code convention):")
            print("  .claude/skills/")
            for plugin in self.selected_plugins:
                print(f"    └── {plugin}/")
                print("        ├── SKILL.md       - Skill instructions")
                print("        └── references/    - Templates and examples")
            print()

        colors.info("Next steps:")
        print()
        print(f"  1. Navigate to your project:")
        print(f"     cd {self.target_path}")
        print()
        print("  2. Start Claude Code:")
        print("     claude")
        print()
        print("  3. Create your first spec in specs/ directory")
        print()
        if self.selected_plugins:
            print("  4. Use skills like /api or /ai-app when developing")
            print()

        colors.info("Documentation: https://github.com/spec-kit/spec-kit")
        print()

    def confirm_installation(self) -> bool:
        """Prompt user to confirm installation.

        Returns:
            True if user confirms, False otherwise
        """
        try:
            response = input("Proceed with installation? (y/n): ").strip().lower()
            return response in ('y', 'yes')
        except KeyboardInterrupt:
            print()
            colors.info("Installation cancelled")
            return False

    def run_installation(
        self,
        plugins: Optional[List[str]] = None,
        force: bool = False,
        interactive: bool = True,
    ) -> None:
        """Run complete installation workflow.

        Args:
            plugins: List of plugin names (None for interactive selection)
            force: If True, overwrite existing installation
            interactive: If True, prompt for confirmation
        """
        # Print header
        colors.print_header("Spec-Kit Installer", "Spec-Driven Development for Claude Code")
        colors.info(f"Target directory: {self.target_path}")
        print()

        # Validate environment
        self.validate_environment()
        self.validate_target(force=force)

        # Select plugins
        if plugins:
            self.select_plugins_from_args(plugins)
        elif interactive:
            self.select_plugins_interactive()
        else:
            # Non-interactive mode with no plugins specified - use default
            colors.info("No plugins specified, using default: api-development")
            self.selected_plugins = ['api-development']

        # Confirm installation
        if interactive:
            if not self.confirm_installation():
                colors.info("Installation cancelled")
                return
            print()

        # Install
        self.install_core()
        self.install_plugins()
        self.install_templates()
        self.offer_architecture_doc(interactive=interactive)
        self.update_project_gitignore()

        # Done
        self.print_summary()
