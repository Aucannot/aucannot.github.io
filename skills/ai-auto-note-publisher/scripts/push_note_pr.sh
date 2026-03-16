#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  bash skills/ai-auto-note-publisher/scripts/push_note_pr.sh \
    --branch <branch-name> \
    --title <pr-title> \
    --body-file <pr-body-markdown>

Description:
  Push current branch to origin and create a PR to current default branch using gh CLI.
USAGE
}

normalize_branch() {
  local name="$1"
  echo "${name#refs/heads/}"
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

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "This script must be run inside a git repository." >&2
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
EXPECTED_BRANCH="$(normalize_branch "$BRANCH")"
if [[ "$CURRENT_BRANCH" != "$EXPECTED_BRANCH" ]]; then
  echo "Current branch '$CURRENT_BRANCH' does not match --branch '$BRANCH'." >&2
  exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
BODY_FILE_ABS="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$BODY_FILE")"
REPO_ROOT_ABS="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$REPO_ROOT")"

BODY_FILE_PATHSPEC=""
if python3 -c 'import os,sys; root,f=sys.argv[1],sys.argv[2]; sys.exit(0 if os.path.commonpath([root,f])==root else 1)' "$REPO_ROOT_ABS" "$BODY_FILE_ABS"; then
  BODY_FILE_PATHSPEC="$(python3 -c 'import os,sys; print(os.path.relpath(sys.argv[2], sys.argv[1]))' "$REPO_ROOT_ABS" "$BODY_FILE_ABS")"
fi

if [[ -n "$BODY_FILE_PATHSPEC" ]]; then
  DIRTY_OUTPUT="$(git status --porcelain --untracked-files=all -- . ":(exclude)$BODY_FILE_PATHSPEC")"
else
  DIRTY_OUTPUT="$(git status --porcelain --untracked-files=all)"
fi

if [[ -n "$DIRTY_OUTPUT" ]]; then
  echo "Working tree is not clean; commit or stash changes first." >&2
  echo "$DIRTY_OUTPUT" >&2
  exit 1
fi

git push -u origin "$BRANCH"

gh pr create --fill=false --title "$PR_TITLE" --body-file "$BODY_FILE"
