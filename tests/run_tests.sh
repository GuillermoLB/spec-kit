#!/bin/bash
#
# Test runner script for spec-kit Python CLI
#
# Usage:
#   ./tests/run_tests.sh              # Run all tests with coverage
#   ./tests/run_tests.sh --quick      # Run without coverage (faster)
#   ./tests/run_tests.sh --verbose    # Run with verbose output
#   ./tests/run_tests.sh --file FILE  # Run specific test file

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Print header
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              Spec-Kit Python CLI Test Suite               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    print_error "pytest not found"
    echo ""
    echo "Install test dependencies with:"
    echo "  pip install -e '.[test]'"
    echo ""
    exit 1
fi

# Parse arguments
QUICK_MODE=false
VERBOSE_MODE=false
SPECIFIC_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --quick)
            QUICK_MODE=true
            shift
            ;;
        --verbose)
            VERBOSE_MODE=true
            shift
            ;;
        --file)
            SPECIFIC_FILE="$2"
            shift 2
            ;;
        *)
            print_error "Unknown option: $1"
            echo ""
            echo "Usage:"
            echo "  $0              # Run all tests with coverage"
            echo "  $0 --quick      # Run without coverage (faster)"
            echo "  $0 --verbose    # Run with verbose output"
            echo "  $0 --file FILE  # Run specific test file"
            echo ""
            exit 1
            ;;
    esac
done

# Build pytest command
PYTEST_CMD="pytest"
PYTEST_ARGS=()

# Add verbosity
if [ "$VERBOSE_MODE" = true ]; then
    PYTEST_ARGS+=("-vv")
else
    PYTEST_ARGS+=("-v")
fi

# Add coverage (unless quick mode)
if [ "$QUICK_MODE" = false ]; then
    PYTEST_ARGS+=("--cov=spec_kit")
    PYTEST_ARGS+=("--cov-report=term-missing")
    PYTEST_ARGS+=("--cov-report=html")
fi

# Set target
if [ -n "$SPECIFIC_FILE" ]; then
    if [ ! -f "$SPECIFIC_FILE" ]; then
        print_error "File not found: $SPECIFIC_FILE"
        exit 1
    fi
    PYTEST_ARGS+=("$SPECIFIC_FILE")
else
    PYTEST_ARGS+=("tests/")
fi

# Run tests
print_status "Running tests..."
echo ""

if $PYTEST_CMD "${PYTEST_ARGS[@]}"; then
    # Tests passed
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_success "All tests passed!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    if [ "$QUICK_MODE" = false ] && [ -z "$SPECIFIC_FILE" ]; then
        print_status "Coverage report saved to: htmlcov/index.html"
        echo ""
        echo "Open with:"
        echo "  open htmlcov/index.html    # macOS"
        echo "  xdg-open htmlcov/index.html  # Linux"
        echo ""
    fi

    exit 0
else
    # Tests failed
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_error "Some tests failed"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    print_warning "Run with --verbose for more details"
    echo ""
    exit 1
fi
