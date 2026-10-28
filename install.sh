#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$ROOT/.opencode"

usage() {
  echo "OpenCode Multi-Agent Starter"
  echo
  echo "Usage:"
  echo "  ./install.sh --global [--dry-run]"
  echo "  ./install.sh --project PATH [--dry-run]"
  echo
  echo "Existing files are never overwritten."
}

if [[ $# -eq 0 ]]; then
  usage
  exit 2
fi

case "$1" in
  --global)
    DEST="$HOME/.config/opencode"
    shift
    ;;
  --project)
    if [[ $# -lt 2 || ! -d "$2" ]]; then
      echo "Error: specify an existing project directory."
      exit 2
    fi
    DEST="$(cd "$2" && pwd -P)/.opencode"
    shift 2
    ;;
  --help|-h)
    usage
    exit 0
    ;;
  *)
    usage
    exit 2
    ;;
esac

DRY_RUN=false

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  shift
fi

if [[ $# -ne 0 ]]; then
  echo "Error: unexpected arguments."
  usage
  exit 2
fi

if [[ ! -f "$SOURCE/opencode.json" ||
      ! -d "$SOURCE/agents" ||
      ! -d "$SOURCE/skills" ]]; then
  echo "Error: incomplete starter configuration."
  exit 1
fi

echo "Source: $SOURCE"
echo "Destination: $DEST"
echo "Dry run: $DRY_RUN"
echo

copied=0
skipped=0

shopt -s nullglob

files=(
  "$SOURCE/opencode.json"
  "$SOURCE/agents/"*.md
  "$SOURCE/skills/"*/SKILL.md
)

for src in "${files[@]}"; do
  relative="${src#"$SOURCE/"}"
  target="$DEST/$relative"

  if [[ -e "$target" || -L "$target" ]]; then
    echo "SKIP: $relative (already exists)"
    ((skipped+=1))
    continue
  fi

  if [[ "$DRY_RUN" == true ]]; then
    echo "WOULD INSTALL: $relative"
  else
    mkdir -p "$(dirname "$target")"
    cp -n "$src" "$target"
    echo "INSTALLED: $relative"
  fi

  ((copied+=1))
done

echo
if [[ "$DRY_RUN" == true ]]; then
  echo "Dry run complete: $copied installable, $skipped existing."
  echo "No files were changed."
else
  echo "Installation complete: $copied installed, $skipped skipped."
  echo "Restart OpenCode or reload its configuration."
fi

if [[ -e "$DEST/opencode.json" && $skipped -gt 0 ]]; then
  echo
  echo "Note: existing configuration files were not merged."
  echo "Verify default_agent=planner and subagent_depth=2."
fi
