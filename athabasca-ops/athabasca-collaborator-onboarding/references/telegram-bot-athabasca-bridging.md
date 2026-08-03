# Telegram bot ↔ Athabasca bearer-token bridging

Use this note when the user already has a Hermes/Telegram bot and wants another human to talk to that bot while the bot performs project-scoped Athabasca actions.

## Separate the layers

1. **Telegram gateway authorization** — can this Telegram user talk to the bot at all?
2. **Athabasca bearer-token authorization** — what user/project/modes do bot-originated Athabasca requests run as?

Do not conflate these.

## Hermes gateway allowlist

For a DM-based Hermes Telegram bot, first add the collaborator's Telegram numeric user ID to the relevant profile `.env`:

```env
TELEGRAM_ALLOWED_USERS=<existing_ids>,<new_user_id>
```

Then restart that profile's gateway:

```bash
hermes -p <profile> gateway restart
```

If the traffic is in a shared group/forum/channel rather than DM, also inspect:
- `TELEGRAM_GROUP_ALLOWED_USERS`
- `TELEGRAM_GROUP_ALLOWED_CHATS`

## Athabasca token ownership gotcha

Current Athabasca behavior:
- `POST /api/auth/api-tokens` defaults `userId` to the currently authenticated user when `userId` is omitted
- bearer auth resolves back to `apiToken.userId`

So if the owner mints a token like:

```json
{
  "name": "cliphouse",
  "kind": "telegram",
  "projectScopes": [{ "projectSlug": "gly", "role": "editor" }],
  "operationModes": ["creator"]
}
```

without `userId`, the token is an **owner-owned token with narrowed scope**, not a collaborator-owned token.

## `kind: "telegram"` is not automatic Hermes wiring

The token kind is useful metadata on the Athabasca side, but it does not automatically configure Hermes to use that token.

The actual bot/integration code still needs to attach:

```http
Authorization: Bearer <athabasca_token>
```

on outbound requests to Athabasca.

## Two valid operating modes

### 1) Fast shared-bot mode
- one bot-held project-scoped Athabasca token
- all approved Telegram users talk to the same bot
- the bot uses the same bearer token for everyone

Pros:
- fastest to ship
- minimal bridge logic

Cons:
- all Athabasca actions attribute to the token owner
- collaborator-level revocation and audit are weaker

### 2) Per-user mapped mode
- collaborator first accepts their Athabasca invite
- mint a token for that collaborator's actual `userId`
- bot bridge maps Telegram sender ID to that user's Athabasca token

Pros:
- proper attribution
- cleaner revocation
- future multi-user semantics are correct

Cons:
- extra bridge/state work

## Security rule

Do **not** send the raw Athabasca bearer token to the collaborator if the goal is "use the bot on Telegram."

The token should normally stay on the bot/server side. The collaborator talks to the bot; the bot talks to Athabasca.
