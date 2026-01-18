#!/bin/bash
#
# Spec-Kit Verification Script
#
# Verifies that spec-kit is properly structured and ready for distribution.
#

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Verifying Spec-Kit Structure..."
echo ""

# Track results
PASS=0
FAIL=0

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} $1 (missing)"
        ((FAIL++))
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} $1/ (missing)"
        ((FAIL++))
    fi
}

check_executable() {
    if [ -x "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 (executable)"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠${NC} $1 (not executable)"
        ((FAIL++))
    fi
}

echo "Core Files:"
check_file "README.md"
check_file "QUICKSTART.md"
check_file "CLAUDE.md"
check_file ".gitignore"
check_file "core/CLAUDE.md"
check_executable "install.sh"
echo ""

echo "Plugin: api-development"
check_file "plugins/api-development/skill.md"
check_file "plugins/api-development/templates/fastapi-endpoint.py"
check_file "plugins/api-development/templates/sam-template.yaml"
echo ""

echo "Plugin: ai-app"
check_file "plugins/ai-app/skill.md"
check_file "plugins/ai-app/templates/anthropic-client.py"
check_file "plugins/ai-app/templates/prompt-patterns.md"
echo ""

echo "Templates:"
check_file "templates/specs/feature.template.md"
check_file "templates/specs/api.template.yaml"
check_file "templates/specs/specifications-summary.template.md"
echo ""

echo "Documentation:"
check_file "CONTRIBUTING.md"
check_dir "docs"
check_file "docs/TROUBLESHOOTING.md"
check_file "docs/PLUGIN_DEVELOPMENT.md"
echo ""

echo "Directories:"
check_dir "core"
check_dir "plugins"
check_dir "templates"
echo ""

# Check for SPECIFICATIONS_SUMMARY.md if multiple specs exist
SPEC_COUNT=$(find specs/features -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
if [ "$SPEC_COUNT" -ge 3 ] && [ ! -f "specs/SPECIFICATIONS_SUMMARY.md" ]; then
    echo -e "${YELLOW}⚠${NC} Consider creating specs/SPECIFICATIONS_SUMMARY.md for better spec tracking ($SPEC_COUNT specs found)"
    echo "  Template: templates/specs/specifications-summary.template.md"
    echo ""
fi

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results: ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ Spec-Kit is ready for distribution!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Test installation: mkdir test-project && ./install.sh test-project"
    echo "  2. Initialize git: git init && git add . && git commit -m 'Initial spec-kit'"
    echo "  3. Push to GitHub (optional)"
    exit 0
else
    echo -e "${RED}✗ Some files are missing or incorrect${NC}"
    echo "Please fix the issues above before distributing."
    exit 1
fi
