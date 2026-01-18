#!/bin/bash
#
# Spec-Kit Installer (DEPRECATED)
#
# ⚠️  DEPRECATION NOTICE:
#    This bash installer will be removed in spec-kit v3.0.0
#    Please use the Python CLI instead:
#      pipx install spec-kit
#      spec-kit init
#
# Installs spec-kit into a target project with selected plugins.
#
# Usage:
#   ./install.sh [target_directory]
#   ./install.sh .              # Install in current directory
#   ./install.sh ~/my-project   # Install in specific directory
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory (where spec-kit is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Target directory (default to current directory)
TARGET_DIR="${1:-.}"
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"  # Get absolute path

# ============================================================================
# Helper Functions
# ============================================================================

print_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                    Spec-Kit Installer                    ║"
    echo "║          Spec-Driven Development for Claude Code         ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  DEPRECATION NOTICE${NC}"
    echo "   This bash installer will be removed in v3.0.0"
    echo "   Please migrate to the Python CLI:"
    echo ""
    echo "     pipx install spec-kit"
    echo "     spec-kit init"
    echo ""
    echo "   For non-interactive mode: spec-kit init --no-interactive"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# ============================================================================
# Validation
# ============================================================================

validate_environment() {
    # Check if we're in the spec-kit directory
    if [ ! -f "$SCRIPT_DIR/core/CLAUDE.md" ]; then
        print_error "Cannot find spec-kit core files. Are you running this from the spec-kit directory?"
        exit 1
    fi

    # Check if target directory exists
    if [ ! -d "$TARGET_DIR" ]; then
        print_error "Target directory does not exist: $TARGET_DIR"
        exit 1
    fi

    # Warn if CLAUDE.md already exists
    if [ -f "$TARGET_DIR/CLAUDE.md" ]; then
        print_warning "CLAUDE.md already exists in target directory"
        read -p "Overwrite? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled"
            exit 0
        fi
    fi
}

# ============================================================================
# Plugin Selection
# ============================================================================

select_plugins() {
    echo ""
    print_info "Available plugins:"
    echo ""
    echo "  1) api-development  - FastAPI + AWS SAM/Lambda patterns"
    echo "  2) ai-app           - LLM integration (Claude, OpenAI)"
    echo "  3) all              - Install all plugins"
    echo ""

    read -p "Enter plugin numbers (space-separated, e.g., '1 2') or 'all': " selection

    SELECTED_PLUGINS=()

    if [[ "$selection" == "all" ]]; then
        SELECTED_PLUGINS=("api-development" "ai-app")
    else
        for num in $selection; do
            case $num in
                1)
                    SELECTED_PLUGINS+=("api-development")
                    ;;
                2)
                    SELECTED_PLUGINS+=("ai-app")
                    ;;
                *)
                    print_warning "Unknown plugin number: $num (skipping)"
                    ;;
            esac
        done
    fi

    if [ ${#SELECTED_PLUGINS[@]} -eq 0 ]; then
        print_error "No plugins selected"
        exit 1
    fi

    echo ""
    print_info "Selected plugins: ${SELECTED_PLUGINS[*]}"
    echo ""
}

# ============================================================================
# Installation
# ============================================================================

install_core() {
    print_info "Installing core files..."

    # Copy CLAUDE.md
    cp "$SCRIPT_DIR/core/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"
    print_success "Installed CLAUDE.md"

    # Create .claude directory
    mkdir -p "$TARGET_DIR/.claude/skills"
    print_success "Created .claude/skills directory"

    # Create specs directory
    mkdir -p "$TARGET_DIR/specs/features"
    mkdir -p "$TARGET_DIR/specs/api"
    print_success "Created specs directory structure"
}

install_plugins() {
    print_info "Installing plugins..."

    for plugin in "${SELECTED_PLUGINS[@]}"; do
        plugin_src="$SCRIPT_DIR/plugins/$plugin"

        if [ ! -d "$plugin_src" ]; then
            print_warning "Plugin not found: $plugin (skipping)"
            continue
        fi

        # Create plugin directory following official Claude Code convention
        plugin_dest="$TARGET_DIR/.claude/skills/$plugin"
        mkdir -p "$plugin_dest"

        # Copy skill file as SKILL.md (official naming convention)
        cp "$plugin_src/skill.md" "$plugin_dest/SKILL.md"
        print_success "Installed plugin: $plugin"

        # Copy templates to references/ (following official pattern)
        if [ -d "$plugin_src/templates" ]; then
            references_dest="$plugin_dest/references"
            mkdir -p "$references_dest"
            cp -r "$plugin_src/templates/"* "$references_dest/"
            print_success "  └─ Added references with templates"
        fi

        # Also keep a copy in .spec-kit-templates for easy access
        if [ -d "$plugin_src/templates" ]; then
            template_dest="$TARGET_DIR/.spec-kit-templates/$plugin"
            mkdir -p "$template_dest"
            cp -r "$plugin_src/templates/"* "$template_dest/"
        fi
    done
}

install_spec_templates() {
    print_info "Installing spec templates..."

    if [ -d "$SCRIPT_DIR/templates/specs" ]; then
        cp -r "$SCRIPT_DIR/templates/specs/"* "$TARGET_DIR/specs/" 2>/dev/null || true
        print_success "Installed spec templates"
    fi
}

create_gitignore() {
    # Add .spec-kit-templates to .gitignore if it doesn't exist
    if [ -f "$TARGET_DIR/.gitignore" ]; then
        if ! grep -q ".spec-kit-templates" "$TARGET_DIR/.gitignore"; then
            echo "" >> "$TARGET_DIR/.gitignore"
            echo "# Spec-Kit templates (optional, for reference)" >> "$TARGET_DIR/.gitignore"
            echo ".spec-kit-templates/" >> "$TARGET_DIR/.gitignore"
            print_success "Updated .gitignore"
        fi
    else
        cat > "$TARGET_DIR/.gitignore" << EOF
# Spec-Kit templates (optional, for reference)
.spec-kit-templates/
EOF
        print_success "Created .gitignore"
    fi
}

print_summary() {
    echo ""
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║              Installation Complete! 🎉                   ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    print_info "Installed in: $TARGET_DIR"
    echo ""
    echo "Files created:"
    echo "  • CLAUDE.md                    - Core spec-driven workflow"
    echo "  • .claude/skills/              - Plugin skills (official structure)"
    echo "  • specs/                       - Specification directory"
    echo "  • .spec-kit-templates/         - Quick reference templates"
    echo ""
    echo "Installed plugins:"
    for plugin in "${SELECTED_PLUGINS[@]}"; do
        case $plugin in
            api-development)
                echo "  • /api-development or /api   - FastAPI + AWS SAM patterns"
                ;;
            ai-app)
                echo "  • /ai-app                    - LLM integration patterns"
                ;;
        esac
    done
    echo ""
    echo "Plugin structure (official Claude Code convention):"
    echo "  .claude/skills/"
    for plugin in "${SELECTED_PLUGINS[@]}"; do
        echo "    └── $plugin/"
        echo "        ├── SKILL.md       - Skill instructions"
        echo "        └── references/    - Templates and examples"
    done
    echo ""
    print_info "Next steps:"
    echo ""
    echo "  1. Navigate to your project:"
    echo "     cd $TARGET_DIR"
    echo ""
    echo "  2. Start Claude Code:"
    echo "     claude"
    echo ""
    echo "  3. Create your first spec in specs/ directory"
    echo ""
    echo "  4. Use skills like /api or /ai-app when developing"
    echo ""
    print_info "Documentation: https://github.com/yourusername/spec-kit"
    echo ""
}

# ============================================================================
# Main Installation Flow
# ============================================================================

main() {
    print_header

    print_info "Target directory: $TARGET_DIR"
    echo ""

    # Validate
    validate_environment

    # Select plugins
    select_plugins

    # Confirm installation
    read -p "Proceed with installation? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installation cancelled"
        exit 0
    fi
    echo ""

    # Install
    install_core
    install_plugins
    install_spec_templates
    create_gitignore

    # Done
    print_summary
}

# Run main function
main
