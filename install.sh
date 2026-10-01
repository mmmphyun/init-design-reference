#!/usr/bin/env bash
#
# One-liner installer for init-design-reference agent skill.
# Supports Google Antigravity, Claude Code, Cursor, and custom targets on Linux and macOS.
#
# Usage:
#   # Remote one-liner (Google Antigravity default):
#   curl -fsSL https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.sh | bash
#
#   # With options:
#   curl -fsSL https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.sh | bash -s -- --agent claude
#
#   # Local execution:
#   ./install.sh --agent antigravity
#

set -euo pipefail

AGENT="antigravity"
TARGET_DIR=""
REPO="${INIT_DESIGN_REF_REPO:-mmmphyun/init-design-reference}"
BRANCH="main"
FORCE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent)
      AGENT="$2"
      shift 2
      ;;
    --target)
      TARGET_DIR="$2"
      shift 2
      ;;
    --repo)
      REPO="$2"
      shift 2
      ;;
    --branch)
      BRANCH="$2"
      shift 2
      ;;
    --force|-f)
      FORCE=true
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

# Resolve install directory
if [[ -n "$TARGET_DIR" ]]; then
  INSTALL_PATH="$TARGET_DIR"
else
  case "$AGENT" in
    antigravity)
      INSTALL_PATH="$HOME/.gemini/config/skills/init-design-reference"
      ;;
    claude)
      INSTALL_PATH="$HOME/.claude/skills/init-design-reference"
      ;;
    cursor)
      INSTALL_PATH="$HOME/.cursor/skills/init-design-reference"
      ;;
    custom)
      echo "Error: --target must be specified when --agent is set to 'custom'." >&2
      exit 1
      ;;
    *)
      echo "Error: Unsupported agent '$AGENT'. Supported values: antigravity, claude, cursor, custom." >&2
      exit 1
      ;;
  esac
fi

echo "Target installation path: $INSTALL_PATH"

if [[ -d "$INSTALL_PATH" ]]; then
  if [[ "$FORCE" != "true" ]]; then
    echo "Warning: Directory already exists: $INSTALL_PATH"
    echo "Pass --force to overwrite."
    exit 0
  fi
  echo "Overwriting existing directory (--force specified)..."
fi

# Detect local execution vs remote stream
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo "")"
IS_LOCAL=false

if [[ -n "$SCRIPT_DIR" && -f "$SCRIPT_DIR/SKILL.md" ]]; then
  IS_LOCAL=true
fi

if [[ "$IS_LOCAL" == "true" ]]; then
  echo "Installing from local repository: $SCRIPT_DIR"
  rm -rf "$INSTALL_PATH"
  mkdir -p "$INSTALL_PATH"

  for item in SKILL.md README.md scripts templates; do
    if [[ -e "$SCRIPT_DIR/$item" ]]; then
      cp -R "$SCRIPT_DIR/$item" "$INSTALL_PATH/"
    fi
  done
else
  echo "Installing from remote repository: $REPO ($BRANCH branch)..."
  TMP_DIR="$(mktemp -d)"
  trap 'rm -rf "$TMP_DIR"' EXIT

  ARCHIVE_URL="https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz"
  echo "Downloading $ARCHIVE_URL..."

  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$ARCHIVE_URL" | tar -xz -C "$TMP_DIR"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO- "$ARCHIVE_URL" | tar -xz -C "$TMP_DIR"
  else
    echo "Error: Neither curl nor wget is available." >&2
    exit 1
  fi

  EXTRACTED_DIR="$(find "$TMP_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
  if [[ -z "$EXTRACTED_DIR" ]]; then
    echo "Error: Failed to find extracted archive directory." >&2
    exit 1
  fi

  rm -rf "$INSTALL_PATH"
  mkdir -p "$INSTALL_PATH"

  for item in SKILL.md README.md scripts templates; do
    if [[ -e "$EXTRACTED_DIR/$item" ]]; then
      cp -R "$EXTRACTED_DIR/$item" "$INSTALL_PATH/"
    fi
  done
fi

echo ""
echo "Installation successful!"
echo "Skill installed at: $INSTALL_PATH"
echo "Verify adapter execution:"
echo "  python \"$INSTALL_PATH/scripts/adapter.py\" \"reference\""
