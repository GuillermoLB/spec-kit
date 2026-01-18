"""Verification logic for spec-kit installations.

Validates that spec-kit is properly installed in a project directory,
checking for required files, directories, and proper structure.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from spec_kit.utils import colors


class ValidationResult:
    """Result of a validation check."""

    def __init__(self, passed: bool, message: str, item: str):
        """Initialize validation result.

        Args:
            passed: Whether the check passed
            message: Description of the check
            item: Item being checked (file/directory path)
        """
        self.passed = passed
        self.message = message
        self.item = item

    def __repr__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return f"ValidationResult({status}, {self.item})"


class Validator:
    """Validates spec-kit installation in a project."""

    def __init__(self, target_path: Path):
        """Initialize validator.

        Args:
            target_path: Project directory to validate
        """
        self.target_path = target_path.resolve()
        self.results: List[ValidationResult] = []
        self.pass_count = 0
        self.fail_count = 0

    def _check_file(self, path: Path, description: Optional[str] = None) -> ValidationResult:
        """Check if a file exists.

        Args:
            path: File path to check (relative to target_path)
            description: Optional description for the check

        Returns:
            ValidationResult
        """
        full_path = self.target_path / path
        desc = description or str(path)

        if full_path.exists() and full_path.is_file():
            result = ValidationResult(True, desc, str(path))
            self.pass_count += 1
        else:
            result = ValidationResult(False, f"{desc} (missing)", str(path))
            self.fail_count += 1

        self.results.append(result)
        return result

    def _check_dir(self, path: Path, description: Optional[str] = None) -> ValidationResult:
        """Check if a directory exists.

        Args:
            path: Directory path to check (relative to target_path)
            description: Optional description for the check

        Returns:
            ValidationResult
        """
        full_path = self.target_path / path
        desc = description or f"{path}/"

        if full_path.exists() and full_path.is_dir():
            result = ValidationResult(True, desc, str(path))
            self.pass_count += 1
        else:
            result = ValidationResult(False, f"{desc} (missing)", str(path))
            self.fail_count += 1

        self.results.append(result)
        return result

    def _check_executable(self, path: Path, description: Optional[str] = None) -> ValidationResult:
        """Check if a file exists and is executable.

        Args:
            path: File path to check (relative to target_path)
            description: Optional description for the check

        Returns:
            ValidationResult
        """
        full_path = self.target_path / path
        desc = description or str(path)

        if full_path.exists() and full_path.is_file():
            if os.access(full_path, os.X_OK):
                result = ValidationResult(True, f"{desc} (executable)", str(path))
                self.pass_count += 1
            else:
                result = ValidationResult(False, f"{desc} (not executable)", str(path))
                self.fail_count += 1
        else:
            result = ValidationResult(False, f"{desc} (missing)", str(path))
            self.fail_count += 1

        self.results.append(result)
        return result

    def check_core_files(self) -> Dict[str, List[ValidationResult]]:
        """Check core spec-kit files.

        Returns:
            Dict with 'core' key containing list of results
        """
        results = []

        # Essential core files
        results.append(self._check_file(Path("CLAUDE.md")))
        results.append(self._check_dir(Path(".claude/skills")))
        results.append(self._check_dir(Path("specs")))

        # Optional but recommended
        claude_skills_empty = not any((self.target_path / ".claude" / "skills").iterdir()) \
            if (self.target_path / ".claude" / "skills").exists() else True

        if claude_skills_empty:
            result = ValidationResult(
                False,
                ".claude/skills/ (empty - no plugins installed)",
                ".claude/skills"
            )
            self.fail_count += 1
            results.append(result)

        return {'core': results}

    def check_plugins(self) -> Dict[str, List[ValidationResult]]:
        """Check installed plugins.

        Returns:
            Dict with plugin names as keys, list of results as values
        """
        skills_dir = self.target_path / ".claude" / "skills"

        if not skills_dir.exists():
            return {'plugins': []}

        plugin_results = {}

        # Check each plugin directory
        for plugin_dir in skills_dir.iterdir():
            if not plugin_dir.is_dir():
                continue

            plugin_name = plugin_dir.name
            results = []

            # Check for SKILL.md
            skill_file = plugin_dir / "SKILL.md"
            if skill_file.exists():
                result = ValidationResult(
                    True,
                    f"Plugin: {plugin_name}",
                    str(skill_file.relative_to(self.target_path))
                )
                self.pass_count += 1
            else:
                result = ValidationResult(
                    False,
                    f"Plugin: {plugin_name} (missing SKILL.md)",
                    str(skill_file.relative_to(self.target_path))
                )
                self.fail_count += 1

            results.append(result)

            # Check for references directory
            references_dir = plugin_dir / "references"
            if references_dir.exists() and references_dir.is_dir():
                result = ValidationResult(
                    True,
                    f"  └─ {plugin_name}/references/",
                    str(references_dir.relative_to(self.target_path))
                )
                self.pass_count += 1
                results.append(result)

            plugin_results[plugin_name] = results

        return plugin_results

    def check_templates(self) -> Dict[str, List[ValidationResult]]:
        """Check spec templates.

        Returns:
            Dict with 'templates' key containing list of results
        """
        results = []

        # Check specs directory structure
        results.append(self._check_dir(Path("specs/features")))
        results.append(self._check_dir(Path("specs/api")))

        # Check for template files (optional)
        template_files = [
            "specs/feature.template.md",
            "specs/api.template.yaml",
        ]

        for template in template_files:
            template_path = self.target_path / template
            if template_path.exists():
                result = ValidationResult(
                    True,
                    f"Template: {template}",
                    template
                )
                self.pass_count += 1
                results.append(result)

        return {'templates': results}

    def check_documentation(self) -> Dict[str, List[ValidationResult]]:
        """Check documentation files.

        Returns:
            Dict with 'documentation' key containing list of results
        """
        results = []

        # Check for README or other docs (optional in installed projects)
        readme_path = self.target_path / "README.md"
        if readme_path.exists():
            result = ValidationResult(
                True,
                "README.md",
                "README.md"
            )
            self.pass_count += 1
            results.append(result)

        return {'documentation': results}

    def check_specs_summary(self) -> Optional[ValidationResult]:
        """Check if SPECIFICATIONS_SUMMARY.md is needed.

        Returns:
            ValidationResult if warning needed, None otherwise
        """
        specs_features_dir = self.target_path / "specs" / "features"

        if not specs_features_dir.exists():
            return None

        # Count spec files
        spec_files = list(specs_features_dir.glob("*.md"))
        spec_count = len([f for f in spec_files if not f.name.startswith('.')])

        summary_file = self.target_path / "specs" / "SPECIFICATIONS_SUMMARY.md"

        if spec_count >= 3 and not summary_file.exists():
            return ValidationResult(
                False,
                f"Consider creating specs/SPECIFICATIONS_SUMMARY.md for better spec tracking ({spec_count} specs found)",
                "specs/SPECIFICATIONS_SUMMARY.md"
            )

        return None

    def run_all_checks(self) -> Dict[str, any]:
        """Run all validation checks.

        Returns:
            Dict with all check results
        """
        # Reset counters
        self.results = []
        self.pass_count = 0
        self.fail_count = 0

        all_results = {}

        # Run all checks
        all_results.update(self.check_core_files())
        all_results.update(self.check_plugins())
        all_results.update(self.check_templates())
        all_results.update(self.check_documentation())

        # Check for specs summary warning
        specs_warning = self.check_specs_summary()
        if specs_warning:
            all_results['specs_warning'] = specs_warning

        return all_results

    def print_results(self, results: Dict[str, any], verbose: bool = False) -> None:
        """Print validation results with colored output.

        Args:
            results: Results from run_all_checks()
            verbose: If True, print all results; if False, only failures
        """
        print()
        colors.print_header("Spec-Kit Verification", f"Checking: {self.target_path}")
        print()

        # Print core files
        if 'core' in results:
            print("Core Files:")
            for result in results['core']:
                if verbose or not result.passed:
                    if result.passed:
                        colors.success(result.message)
                    else:
                        colors.error(result.message)
            print()

        # Print plugins
        plugin_keys = [k for k in results.keys() if k not in ['core', 'templates', 'documentation', 'specs_warning']]
        if plugin_keys:
            print("Installed Plugins:")
            for plugin_name in plugin_keys:
                for result in results[plugin_name]:
                    if verbose or not result.passed:
                        if result.passed:
                            colors.success(result.message)
                        else:
                            colors.error(result.message)
            print()

        # Print templates
        if 'templates' in results and results['templates']:
            print("Templates:")
            for result in results['templates']:
                if verbose or not result.passed:
                    if result.passed:
                        colors.success(result.message)
                    else:
                        colors.error(result.message)
            print()

        # Print documentation
        if 'documentation' in results and results['documentation']:
            if verbose:
                print("Documentation:")
                for result in results['documentation']:
                    if result.passed:
                        colors.success(result.message)
                    else:
                        colors.error(result.message)
                print()

        # Print specs warning
        if 'specs_warning' in results:
            colors.warning(results['specs_warning'].message)
            colors.info("  Template: templates/specs/specifications-summary.template.md")
            print()

        # Print summary
        colors.print_separator()
        print(f"Results: {colors.colorize(f'{self.pass_count} passed', colors.GREEN)}, "
              f"{colors.colorize(f'{self.fail_count} failed', colors.RED)}")
        colors.print_separator()
        print()

        if self.fail_count == 0:
            colors.success("Spec-Kit installation is valid!")
            print()
        else:
            colors.error("Some checks failed")
            colors.info("Run with --verbose to see all checks")
            print()

    def print_json(self, results: Dict[str, any]) -> None:
        """Print results as JSON.

        Args:
            results: Results from run_all_checks()
        """
        output = {
            'valid': self.fail_count == 0,
            'pass_count': self.pass_count,
            'fail_count': self.fail_count,
            'checks': {}
        }

        # Convert results to JSON-serializable format
        for category, items in results.items():
            if category == 'specs_warning':
                output['warnings'] = {
                    'message': items.message,
                    'item': items.item
                }
            elif isinstance(items, list):
                output['checks'][category] = [
                    {
                        'passed': r.passed,
                        'message': r.message,
                        'item': r.item
                    }
                    for r in items
                ]
            elif isinstance(items, dict):
                # Plugin results
                for plugin_name, plugin_results in items.items():
                    output['checks'][f'plugin_{plugin_name}'] = [
                        {
                            'passed': r.passed,
                            'message': r.message,
                            'item': r.item
                        }
                        for r in plugin_results
                    ]

        print(json.dumps(output, indent=2))

    def get_exit_code(self) -> int:
        """Get exit code based on validation results.

        Returns:
            0 if all checks passed, 1 if any failed
        """
        return 0 if self.fail_count == 0 else 1
