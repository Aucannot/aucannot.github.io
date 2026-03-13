#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bash skills/ai-auto-note-publisher/scripts/push_note_pr.sh \
    --branch <branch-name> \
    --title <pr-title> \
    --body-file <pr-body-markdown>

Description:
  Push current branch to origin and create a PR to current default branch using gh CLI.
EOF
}

BRANCH=""
PR_TITLE=""
BODY_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --branch)
      BRANCH="${2:-}"
      shift 2
      ;;
    --title)
      PR_TITLE="${2:-}"
      shift 2
      ;;
    --body-file)
      BODY_FILE="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$BRANCH" || -z "$PR_TITLE" || -z "$BODY_FILE" ]]; then
  echo "Missing required arguments." >&2
  usage
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Please install and run 'gh auth login' first." >&2
  exit 1
fi

if [[ ! -f "$BODY_FILE" ]]; then
  echo "PR body file not found: $BODY_FILE" >&2
  exit 1
fi

CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$CURRENT_BRANCH" != "$BRANCH" ]]; then
  echo "Current branch '$CURRENT_BRANCH' does not match --branch '$BRANCH'." >&2
  exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
BODY_FILE_ABS="$(cd "$(dirname "$BODY_FILE")" && pwd)/$(basename "$BODY_FILE")"

BODY_FILE_PATHSPEC=""
if [[ "$BODY_FILE_ABS" == "$REPO_ROOT"/* ]]; then
  BODY_FILE_PATHSPEC="${BODY_FILE_ABS#"$REPO_ROOT"/}"
fi

if [[ -n "$BODY_FILE_PATHSPEC" ]]; then
  DIRTY_OUTPUT="$(git status --porcelain --untracked-files=all -- . ":(exclude)$BODY_FILE_PATHSPEC")"
else
  DIRTY_OUTPUT="$(git status --porcelain --untracked-files=all)"
fi

if [[ -n "$DIRTY_OUTPUT" ]]; then
  echo "Working tree is not clean; commit or stash changes first." >&2
  exit 1
fi

git push -u origin "$BRANCH"

gh pr create --fill=false --title "$PR_TITLE" --body-file "$BODY_FILE"
