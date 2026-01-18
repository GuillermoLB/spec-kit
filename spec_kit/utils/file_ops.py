"""File operation utilities with safety checks.

Provides safe file and directory operations with proper error handling.
Uses pathlib for cross-platform compatibility.
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional


def ensure_directory(path: Path) -> None:
    """Create directory if it doesn't exist.

    Args:
        path: Directory path to create

    Raises:
        OSError: If directory creation fails
    """
    path.mkdir(parents=True, exist_ok=True)


def safe_copy_file(src: Path, dest: Path, force: bool = False) -> bool:
    """Safely copy file with optional overwrite protection.

    Args:
        src: Source file path
        dest: Destination file path
        force: If True, overwrite existing files

    Returns:
        True if file was copied, False if skipped

    Raises:
        FileNotFoundError: If source file doesn't exist
        OSError: If copy operation fails
    """
    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {src}")

    if dest.exists() and not force:
        return False

    # Ensure destination directory exists
    dest.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(src, dest)
    return True


def safe_copy_tree(src: Path, dest: Path, force: bool = False) -> None:
    """Safely copy directory tree.

    Args:
        src: Source directory path
        dest: Destination directory path
        force: If True, overwrite existing files

    Raises:
        FileNotFoundError: If source directory doesn't exist
        OSError: If copy operation fails
    """
    if not src.exists():
        raise FileNotFoundError(f"Source directory not found: {src}")

    if not src.is_dir():
        raise NotADirectoryError(f"Source is not a directory: {src}")

    # Ensure destination directory exists
    dest.mkdir(parents=True, exist_ok=True)

    # Copy all files and subdirectories
    for item in src.rglob('*'):
        if item.is_file():
            relative_path = item.relative_to(src)
            dest_file = dest / relative_path
            safe_copy_file(item, dest_file, force=force)


def validate_path(path: Path, must_exist: bool = False, must_be_dir: bool = False) -> bool:
    """Validate a file system path.

    Args:
        path: Path to validate
        must_exist: If True, path must exist
        must_be_dir: If True, path must be a directory

    Returns:
        True if path is valid

    Raises:
        FileNotFoundError: If path must exist but doesn't
        NotADirectoryError: If path must be directory but isn't
    """
    if must_exist and not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    if must_be_dir and path.exists() and not path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")

    return True


def find_spec_kit_root() -> Optional[Path]:
    """Find the spec-kit installation directory.

    Searches upward from current file location to find the spec-kit root
    (identified by presence of core/CLAUDE.md).

    Returns:
        Path to spec-kit root, or None if not found
    """
    current = Path(__file__).resolve()

    # Search upward for spec-kit root (max 10 levels)
    for _ in range(10):
        current = current.parent
        if (current / "core" / "CLAUDE.md").exists():
            return current

    return None


def get_gitignore_entries() -> List[str]:
    """Get gitignore entries for spec-kit templates.

    Returns:
        List of gitignore entry strings
    """
    return [
        "",
        "# Spec-Kit templates (optional, for reference)",
        ".spec-kit-templates/",
    ]


def update_gitignore(target_dir: Path, entries: List[str]) -> bool:
    """Update .gitignore file with spec-kit entries.

    Args:
        target_dir: Target directory containing .gitignore
        entries: List of entries to add

    Returns:
        True if gitignore was modified, False if entries already present
    """
    gitignore_path = target_dir / ".gitignore"

    # Read existing content
    existing_content = ""
    if gitignore_path.exists():
        existing_content = gitignore_path.read_text()

    # Check if entries already present
    if ".spec-kit-templates/" in existing_content:
        return False

    # Append entries
    with gitignore_path.open('a') as f:
        for entry in entries:
            f.write(entry + '\n')

    return True
