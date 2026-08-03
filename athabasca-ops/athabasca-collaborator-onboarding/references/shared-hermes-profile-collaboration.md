# Shared Hermes profile collaboration notes

Use this reference when onboarding a human collaborator to a **shared Hermes Telegram bot/profile** that fronts Athabasca.

## Separate the layers

1. **Telegram/Hermes access**
   - Add the collaborator's Telegram numeric user ID to the relevant profile allowlist.
   - Restart the gateway.
   - This only grants access to talk to the bot.

2. **Athabasca app access**
   - Create an Athabasca invitation.
   - Send the invite link.
   - The collaborator accepts with the invited email.
   - This creates/updates the Athabasca user and browser session.

3. **Optional Athabasca bearer-token access**
   - Create an API token only if the collaborator or bridge needs non-browser access.
   - Do not conflate invite acceptance with token issuance.

## Shared-bot group pattern

When the owner wants visibility into the collaborator's interaction history, prefer a shared Telegram group/topic:

- owner + collaborator + bot in one group/topic
- `TELEGRAM_ALLOWED_CHATS=<group_id>`
- `TELEGRAM_GROUP_ALLOWED_CHATS=<group_id>`
- `telegram.require_mention: true`
- optional: `TELEGRAM_OBSERVE_UNMENTIONED_GROUP_MESSAGES=true`

Operational notes:
- if the bot does not see normal group messages, Telegram privacy mode is the first thing to check
- disabling privacy mode requires removing and re-adding the bot to the group
- making the bot a group admin is an alternative

## Per-user Codex ownership caveat

A shared Hermes profile does **not** natively provide sender-specific OpenAI Codex usage attribution just because multiple people authenticate into the same profile.

Assume:
- one shared profile = one shared credential pool
- adding a second `openai-codex` login adds another credential entry to the same pool
- routing is profile-scoped, not Telegram-sender-scoped

So:
- **fast path:** shared profile, shared bot, shared provider pool
- **clean ownership path:** separate Hermes profiles/bots or a custom sender→credential bridge

## Skills isolation caveat

`skills.external_dirs` is not a write redirection mechanism.

Behavior to remember:
- external skill dirs are loaded/indexed
- new agent-created skills still write to the profile-local skills directory under that profile's `HERMES_HOME`

If the operator wants reviewable self-improvement only in a worktree path, they need a stronger workflow/guardrail than `skills.external_dirs` alone.

## Security posture reminder

A collaborator talking to a shared Hermes bot does not automatically get Unix-level access to the underlying host. The real risk is **what the bot is allowed to do on the host**.

Review these before handing a shared bot to a collaborator:
- enabled toolsets (`terminal`, `file`, `code_execution`, `delegation`, `cronjob`)
- live/default working directory
- whether the bot is creator-mode vs operator/dev-mode
- whether secrets remain only server-side
