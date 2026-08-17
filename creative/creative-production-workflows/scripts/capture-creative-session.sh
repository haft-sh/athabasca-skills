#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $# -lt 2 || $# -gt 4 ]]; then
  echo "usage: capture-creative-session.sh <profile> <session-id> [label] [output-root]" >&2
  exit 2
fi

PROFILE="$1"
SESSION_ID="$2"
LABEL="${3:-creative-project-completion}"
ROOT="${4:-$HOME/.hermes/profiles/$PROFILE/persona-optimization/traces}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
SAFE_LABEL="$(printf '%s' "$LABEL" | tr -cs 'A-Za-z0-9._-' '-')"
OUT="$ROOT/${STAMP}-${SAFE_LABEL}-${SESSION_ID}"

mkdir -p "$OUT"

# Explicit redaction for full session content.
hermes -p "$PROFILE" sessions export "$OUT/session.jsonl" \
  --format jsonl --session-id "$SESSION_ID" --redact

# Trace exports are secret-redacted by default. Never add --no-redact here.
hermes -p "$PROFILE" sessions export "$OUT/trace.jsonl" \
  --format trace --session-id "$SESSION_ID"

hermes -p "$PROFILE" sessions export "$OUT/prompts.jsonl" \
  --format jsonl --session-id "$SESSION_ID" --only user-prompts --redact

# Flag correction/friction anchors for human review; matches are not automatic labels.
python3 "$SCRIPT_DIR/extract-creative-friction.py" \
  "$OUT/session.jsonl" "$OUT/friction-episodes.jsonl"

# Preserve pre-compaction ancestors as one human-readable logical lineage.
hermes -p "$PROFILE" sessions export "$OUT/logical-lineage" \
  --format md --session-id "$SESSION_ID" --lineage logical --redact --force

python3 - "$OUT/outcome.json" "$PROFILE" "$SESSION_ID" "$LABEL" <<'PY'
import json
import sys
from pathlib import Path

path, profile, session_id, label = sys.argv[1:]
payload = {
    "schema": "creative-session-outcome-v1",
    "profile": profile,
    "session_id": session_id,
    "label": label,
    "status": "needs-human-label",
    "creative_objective": "",
    "final_artifacts": [],
    "completion_evidence": [],
    "owner_approval": {"status": "unknown", "evidence": ""},
    "what_worked": [],
    "what_failed": [],
    "user_corrections": [],
    "workflow_bottlenecks": [],
    "tooling_or_provider_failures": [],
    "cost_or_attempt_notes": [],
    "candidate_training_episodes": [],
    "exclude_from_optimization": []
}
Path(path).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY

python3 - "$OUT" <<'PY'
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
rows = []
for path in sorted(root.rglob("*")):
    if not path.is_file() or path.name == "SHA256SUMS":
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    rows.append(f"{digest}  {path.relative_to(root)}")
(root / "SHA256SUMS").write_text("\n".join(rows) + "\n", encoding="utf-8")
PY

printf 'Captured redacted creative session trace:\n%s\n' "$OUT"
printf 'Complete outcome.json before using the trace for optimization.\n'
