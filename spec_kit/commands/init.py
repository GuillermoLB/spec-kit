"""Implementation of 'spec-kit init' command.

Handles the initialization of spec-kit in a target project directory,
including plugin selection and installation.
"""

from pathlib import Path
from typing import List, Optional

from spec_kit.core.installer import Installer
from spec_kit.utils import colors


def execute(args) -> int:
    """Execute spec-kit init command.

    Args:
        args: Parsed command-line arguments from argparse
            - path: Target directory path
            - plugins: Comma-separated plugin names
            - no_interactive: Skip interactive prompts
            - force: Overwrite existing installation

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    try:
        # Resolve target path
        target_path = Path(args.path).resolve()

        # Create installer
        installer = Installer(target_path=target_path)

        # Parse plugins list if provided
        plugins: Optional[List[str]] = None
        if args.plugins:
            plugins = [p.strip() for p in args.plugins.split(',')]

        # Run installation
        installer.run_installation(
            plugins=plugins,
            force=args.force,
            interactive=not args.no_interactive,
        )

        return 0

    except FileNotFoundError as e:
        colors.error(str(e))
        return 1

    except FileExistsError as e:
        colors.error(str(e))
        return 1

    except ValueError as e:
        colors.error(str(e))
        return 1

    except RuntimeError as e:
        colors.error(str(e))
        return 1

    except KeyboardInterrupt:
        print()
        colors.info("Installation cancelled")
        return 130  # Standard exit code for SIGINT

    except Exception as e:
        colors.error(f"Unexpected error: {e}")
        if hasattr(args, 'verbose') and args.verbose:
            import traceback
            traceback.print_exc()
        return 1
