"""Implementation of 'spec-kit verify' command.

Verifies that spec-kit is properly installed in the current project,
checking for required files, directories, and proper structure.
"""

import os
from pathlib import Path

from spec_kit.core.validator import Validator
from spec_kit.utils import colors


def execute(args) -> int:
    """Execute spec-kit verify command.

    Args:
        args: Parsed command-line arguments from argparse
            - json: Output results as JSON
            - verbose: Show all checks, not just failures

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    try:
        # Get current working directory
        target_path = Path(os.getcwd())

        # Create validator
        validator = Validator(target_path=target_path)

        # Run all checks
        results = validator.run_all_checks()

        # Print results
        if args.json:
            validator.print_json(results)
        else:
            verbose = hasattr(args, 'verbose') and args.verbose
            validator.print_results(results, verbose=verbose)

        # Return exit code
        return validator.get_exit_code()

    except KeyboardInterrupt:
        print()
        colors.info("Verification cancelled")
        return 130  # Standard exit code for SIGINT

    except Exception as e:
        colors.error(f"Unexpected error: {e}")
        if hasattr(args, 'verbose') and args.verbose:
            import traceback
            traceback.print_exc()
        return 1
