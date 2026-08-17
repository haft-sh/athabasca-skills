---
name: athabasca-nightshift-logging
description: Log Athabasca Night Shift session metadata to GitHub Issue #55 instead of markdown files to prevent merge conflicts during parallel branch work.
trigger: When starting, during, or completing a Night Shift session in the Athabasca repo, or when asked to log session state, heartbeat, or TODO updates.
---

## Overview

Night Shift operational logs (heartbeat, TODO state, session metadata) are stored in **GitHub Issue #55** as append-only comments, not in repo markdown files. This eliminates merge conflicts when multiple branches run parallel Night Shift sessions.

## When to Use

- Starting a Night Shift session
- Completing a Night Shift session  
- Updating TODO state during a session
- Recording heartbeat/timestamp entries
- Migrating from old `docs/ops/HEARTBEAT.md` or `docs/ops/TODO_FOR_HUMAN.md` patterns

## Procedure

### 1. Log Session Start

At the beginning of each Night Shift session, post a comment to Issue #55:

```bash
./scripts/log-nightshift-session.sh "Session start: $(date -I) - Night Shift beginning. Selected issue: #XX - [title]"
```

Or manually:
```bash
gh issue comment 55 --repo jplew/athabasca --body "## Session: $(date -I)
- **Phase:** Night Shift
- **Start Time:** $(date -I)
- **Selected Issue:** #XX - [title]
- **Agent:** Hermes (Night Shift)
- **Status:** In Progress"
```

### 2. Log Session Progress (Optional)

For long sessions or major milestones:
```bash
gh issue comment 55 --repo jplew/athabasca --body "### Progress Update - $(date -I)
- Completed: [summary]
- Next: [next step]
- Tests: [status]"
```

### 3. Log Session Completion

At session end, post final summary:
```bash
gh issue comment 55 --repo jplew/athabasca --body "## Session Complete: $(date -I)
- **Duration:** [start] - [end]
- **Issue Completed:** #XX
- **Commits:** [hashes]
- **Tests:** [count] passing
- **Board State:** Issue #XX → Done
- **Ambiguities:** [none / list any]
- **Next Ready Items:** [list or 'none']"
```

## Helper Script

Location: `scripts/log-nightshift-session.sh`

Usage:
```bash
./scripts/log-nightshift-session.sh "Your session summary here"
```

The script:
- Validates repo context (must be athabasca)
- Formats message with timestamp
- Posts to Issue #55 via gh CLI
- Returns success/failure status

## Migration Notes

**Old Pattern (DEPRECATED):**
```markdown
# docs/ops/HEARTBEAT.md
## 2026-03-17
Session: Night Shift
Issue: #42
```

**New Pattern (CURRENT):**
```bash
gh issue comment 55 --body "## Session: 2026-03-17..."
```

The files `docs/ops/HEARTBEAT.md` and `docs/ops/TODO_FOR_HUMAN.md` are:
- ✅ Removed from repo
- ✅ Added to `.gitignore`
- ✅ Replaced by Issue #55 comments

## Benefits

1. **No merge conflicts** - Append-only via API, not edited in branches
2. **Queryable history** - `gh issue view 55` or GitHub API
3. **Built-in provenance** - Author, timestamp, edit history tracked by GitHub
4. **Centralized** - Single source of truth across all branches/machines
5. **Separation of concerns** - Product code in repo, operational metadata in GitHub

## Pitfalls

- ❌ Don't create new markdown log files in `docs/ops/`
- ❌ Don't edit Issue #55 comments (append only for traceability)
- ❌ Don't log to local files (`~/.athabasca/logs/`) - use GitHub as canonical
- ✅ Do verify repo context before logging (script does this automatically)
- ✅ Do include timestamps in ISO format for consistency
- ✅ Do post both start and completion summaries for full traceability

## Verification

After logging, verify the comment was posted:
```bash
gh issue view 55 --repo jplew/athabasca --comments | tail -20
```

Should show your most recent session log at the bottom.

## Related

- Issue #55: Night Shift Session Logs (centralized log destination)
- `docs/ops/NIGHT_SHIFT.md`: Night Shift operating procedures
- `docs/ops/NIGHT_SHIFT_CONTINUATION_PROMPT.md`: Agent prompt with logging instructions
- Skill: `github-issues` - General GitHub issue management
