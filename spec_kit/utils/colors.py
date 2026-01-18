"""Terminal color utilities using ANSI escape codes.

Provides colored output functionality matching the bash script aesthetics.
Zero dependencies - uses only ANSI escape codes.
"""

# ANSI Color Codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color / Reset


def colorize(text: str, color: str) -> str:
    """Wrap text in ANSI color codes.

    Args:
        text: Text to colorize
        color: Color code (RED, GREEN, YELLOW, BLUE)

    Returns:
        Colored text string
    """
    return f"{color}{text}{NC}"


def success(message: str) -> None:
    """Print success message with green checkmark.

    Args:
        message: Success message to print
    """
    print(f"{GREEN}✓{NC} {message}")


def error(message: str) -> None:
    """Print error message with red X.

    Args:
        message: Error message to print
    """
    print(f"{RED}✗{NC} {message}")


def warning(message: str) -> None:
    """Print warning message with yellow warning symbol.

    Args:
        message: Warning message to print
    """
    print(f"{YELLOW}⚠{NC} {message}")


def info(message: str) -> None:
    """Print info message with blue info symbol.

    Args:
        message: Info message to print
    """
    print(f"{BLUE}ℹ{NC} {message}")


def print_header(title: str, subtitle: str = "") -> None:
    """Print formatted header box.

    Args:
        title: Main title text
        subtitle: Optional subtitle text
    """
    print(colorize("╔══════════════════════════════════════════════════════════╗", BLUE))
    print(colorize(f"║{title.center(58)}║", BLUE))
    if subtitle:
        print(colorize(f"║{subtitle.center(58)}║", BLUE))
    print(colorize("╚══════════════════════════════════════════════════════════╝", BLUE))
    print()


def print_separator() -> None:
    """Print horizontal separator line."""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
