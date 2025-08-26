#!/usr/bin/env bash
set -euo pipefail
: "${REPO:?Set REPO=owner/repo}"
gh label create "epic"            -R "$REPO" -c "#5319e7" -d "Tracking issue (epic)"
gh label create "type:feature"    -R "$REPO" -c "#0e8a16"
gh label create "type:bug"        -R "$REPO" -c "#d73a4a"
gh label create "type:chore"      -R "$REPO" -c "#c5def5"
gh label create "priority:P1"     -R "$REPO" -c "#b60205"
gh label create "priority:P2"     -R "$REPO" -c "#d93f0b"
gh label create "priority:P3"     -R "$REPO" -c "#fbca04"
gh label create "ready"           -R "$REPO" -c "#00c0ff" -d "Auto-create a branch when applied"
