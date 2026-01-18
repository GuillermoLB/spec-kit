"""Main CLI entry point for spec-kit.

Provides the command-line interface with argparse, routing commands
to their respective handlers.
"""

import argparse
import sys

from spec_kit.commands import init, verify


def main() -> int:
    """Main CLI entry point.

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = argparse.ArgumentParser(
        prog='spec-kit',
        description='Professional spec-driven development toolkit for Claude Code',
        epilog='Visit https://github.com/spec-kit/spec-kit for documentation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '--version',
        action='version',
        version='spec-kit 2.0.0'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output with detailed error messages'
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(
        dest='command',
        required=True,
        help='Available commands'
    )

    # ========================================================================
    # spec-kit init
    # ========================================================================
    init_parser = subparsers.add_parser(
        'init',
        help='Initialize spec-kit in a project directory',
        description='Install spec-kit files, plugins, and templates into a project directory.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  spec-kit init                        # Install in current directory (interactive)
  spec-kit init ~/my-project           # Install in specific directory
  spec-kit init --plugins api,ai       # Install with specific plugins
  spec-kit init --no-interactive       # Non-interactive mode (CI/CD)
  spec-kit init --force                # Overwrite existing installation

Available plugins:
  api-development (alias: api)  - FastAPI + AWS SAM/Lambda patterns
  ai-app (alias: ai)            - LLM integration (Claude, OpenAI)
        """
    )

    init_parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Target directory for installation (default: current directory)'
    )

    init_parser.add_argument(
        '--plugins',
        help='Comma-separated plugin names (e.g., "api,ai" or "api-development,ai-app")'
    )

    init_parser.add_argument(
        '--no-interactive',
        action='store_true',
        help='Skip interactive prompts (useful for CI/CD)'
    )

    init_parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing spec-kit installation'
    )

    # ========================================================================
    # spec-kit verify
    # ========================================================================
    verify_parser = subparsers.add_parser(
        'verify',
        help='Verify spec-kit installation',
        description='Check that spec-kit is properly installed in the current project.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  spec-kit verify                      # Verify current directory
  spec-kit verify --verbose            # Show all checks (passed and failed)
  spec-kit verify --json               # Output results as JSON (for CI/CD)

Exit codes:
  0 - All checks passed
  1 - Some checks failed
        """
    )

    verify_parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON (useful for CI/CD)'
    )

    verify_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show all checks (passed and failed), not just failures'
    )

    # Parse arguments
    args = parser.parse_args()

    # Route to command handlers
    try:
        if args.command == 'init':
            return init.execute(args)
        elif args.command == 'verify':
            return verify.execute(args)
        else:
            parser.print_help()
            return 1

    except KeyboardInterrupt:
        print()
        return 130  # Standard exit code for SIGINT

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
