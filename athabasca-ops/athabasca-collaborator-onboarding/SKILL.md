---
name: athabasca-collaborator-onboarding
description: Onboard an external human collaborator to Athabasca by handling network reachability, account invitation, invite acceptance, optional Telegram/Hermes token issuance, and post-invite verification.
triggers:
  - User asks how to add an invitee, collaborator, reviewer, or editor to Athabasca
  - Need to explain or execute Athabasca multi-user onboarding
  - Need to grant limited access to a single project for an external person
  - Need to distinguish Tailscale sharing from Athabasca app auth
version: 1.0.0
---

# Athabasca collaborator onboarding

Use this when the user wants another human to access an Athabasca instance. Treat onboarding as a layered workflow:
1. **Network reachability** (usually Tailscale)
2. **Athabasca identity + membership** (invite + accept)
3. **Optional agent/API access** (Telegram/Hermes bearer token)
4. **Verification** (they can reach only what they should)

Do not collapse these layers into one explanation. The common failure mode is mixing up Tailscale access with Athabasca auth.

## Core model

- **Tailscale controls machine reachability.** It decides whether the invitee can hit the Athabasca host at all.
- **Athabasca auth controls app access.** It decides whether the invitee can sign in and which project(s) they can access.
- **API tokens control non-browser agent access.** Use these for Telegram/Hermes or other bearer-token workflows.

## Tailscale decision rule

When the Athabasca box is only exposed on a tailnet IP:
- if the collaborator only needs access to **one machine**, prefer **Share machine** with their email
- if they need access to **multiple machines** or broader network membership, invite them to the **tailnet** instead
- **Add device** is for the owner's own new device logging into the owner's account, not for granting another person access

When answering a user who is staring at the Tailscale UI, be explicit:
- **Share machine** = right choice for a one-box external collaborator
- **Add device** = wrong choice unless they are enrolling their own laptop/phone into their own Tailscale account

## Recommended onboarding sequence

1. Confirm the Athabasca host is reachable and note the current Tailscale IP.
2. In Tailscale, give the collaborator reachability:
   - usually **Share machine** to their email
   - or tailnet invite if they need broader access
3. Verify reachability first:
   - have them open `http://<tailscale-ip>:3000/api/health`
   - if this fails, stop and fix network access before discussing app login
4. Create an Athabasca invitation.
5. Send the invite link: `http://<tailscale-ip>:3000/?invite=<raw_token>`
6. Have them accept with the **same email address** that was invited.
7. Verify they can sign in and only see the intended project(s).
8. If they need Telegram/Hermes access, mint a scoped API token separately.
9. If they need provider-backed generation, verify provider grants exist; do not assume project membership implies provider access.

## Live contract to verify before instructing

Before giving exact operator steps, inspect the current implementation rather than relying on old docs.

Useful live checks:
- `GET /api/health` — confirms the server is up and R2 status if relevant
- unauthenticated `GET /api/auth/me` — should confirm auth is live (usually returns authentication required)
- auth routes / schemas / handlers — inspect current payload shapes for invitations, accept, and API token creation

## Invite flow

Canonical endpoints to inspect/use:
- `POST /api/auth/invitations`
- `POST /api/auth/invitations/accept`
- `POST /api/auth/api-tokens`

Typical owner flow:
1. Owner logs in and obtains a session cookie.
2. Owner creates the invitation with email + project scope + role/modes.
3. The response returns a raw invite token.
4. Send the browser invite link to the collaborator.
5. Collaborator accepts the invite by entering the invited email, password, and optional name.

## Guidance for V1 collaborator scope

When the user asks for a normal human collaborator on a single project, default to the narrowest sensible scope:
- project-scoped invite
- `role: editor` unless the implementation defines a more appropriate limited role
- operation modes limited to what they actually need (for example `creator` only)

If the user wants review-only access, check the current role model first; do not invent role names.

## Email binding rule

Treat invites as email-bound unless code inspection proves otherwise.

Important operator instruction:
- the collaborator should accept using the **exact same email address** the owner invited
- mismatched email, expired token, or already-consumed token should be explained as likely failure causes

## Telegram / Hermes access

Browser access and bearer-token access are separate.

If the collaborator also needs chat/agent access:
1. create a dedicated API token after the user account is set up
2. scope it to the intended project(s)
3. keep the operation modes narrow
4. tell the user to wire it as `Authorization: Bearer <token>`

Do not assume the browser invite itself creates or reveals a reusable API token.

### Important token-identity rule

Verify who owns the token.

Current Athabasca behavior: when `POST /api/auth/api-tokens` is called **without** `userId`, the token is created for the **currently authenticated user**. So an owner minting a `kind: "telegram"` token without `userId` is creating an owner-owned token with narrowed scope, not a collaborator-owned token.

This matters for audit and attribution:
- a shared bot using that token will act as the token owner
- Athabasca will not treat Telegram sender identity as a separate app user unless the bridge maps senders to distinct Athabasca tokens/users

### Important bridge rule

`kind: "telegram"` on the Athabasca token is metadata, not automatic Hermes wiring.

Do **not** imply that creating a `kind: "telegram"` API token automatically makes Hermes use it. The actual Telegram/Hermes bridge still needs an explicit place where outbound Athabasca requests attach:

```http
Authorization: Bearer <token>
```

If the bot/server is the integration point, keep the token on the bot/server side and have the bridge inject the header. Do **not** send the raw Athabasca bearer token to the collaborator unless the explicit goal is direct API access outside the bot.

#### When no existing bridge file is obvious

A common real-world case is that the Hermes profile exists, the Telegram allowlist is configured, but there is **no single checked-in app file** that already owns Athabasca API traffic. In that case, do not hand-wave "put the token somewhere in the bot". Route bot-side Athabasca requests through one explicit Athabasca client surface.

Default concrete location for Hermes-side integrations:
- `.hermes/plugins/athabasca-api`

Recommended contract for that plugin/client surface:
- load `ATHABASCA_BASE_URL`
- load `ATHABASCA_API_TOKEN`
- optionally load `ATHABASCA_PROJECT_SLUG`
- attach `Authorization: Bearer <token>` on every outbound Athabasca request
- centralize HTTP error handling there instead of duplicating curl/fetch snippets across prompts/scripts
- block raw terminal HTTP calls to Athabasca when the plugin is available

Compatibility location for the legacy live helper:
- `~/.hermes/scripts/athabasca_client.py`

Also keep a repo-tracked recovery/reference duplicate at:
- `docs/reference/agent-tools/athabasca_client.py`

This gives the operator one verifiable insertion point for bearer auth and makes later migration from a shared token to per-user token mapping much simpler.

See also:
- `references/global-owner-token-and-bearer-helper.md`

- preferred Hermes plugin: `.hermes/plugins/athabasca-api`
- legacy live helper: `~/.hermes/scripts/athabasca_client.py`
- repo-tracked recovery/reference copy: `docs/reference/agent-tools/athabasca_client.py`

This gives the operator one verifiable insertion point for bearer auth and makes later migration from a shared token to per-user token mapping much simpler.

This gives the operator one verifiable insertion point for bearer auth and makes later migration from a shared token to per-user token mapping much simpler.

### Hermes gateway allowlist step

If the collaborator needs to DM an existing Hermes Telegram bot, check the profile's Telegram allowlist before discussing bearer-token wiring.

Common operational path:
- add the collaborator's Telegram numeric user ID to `TELEGRAM_ALLOWED_USERS` in the relevant Hermes profile `.env`
- restart that Hermes gateway/profile
- only then test the DM path

For existing shared/group Telegram chats, also inspect chat allowlists if applicable (`TELEGRAM_GROUP_ALLOWED_USERS`, `TELEGRAM_GROUP_ALLOWED_CHATS`).

Important operator distinction:
- this Telegram allowlist step only grants **Hermes chat access** to that bot/profile
- it does **not** create an Athabasca app account, browser session cookie, or Athabasca bearer token
- Athabasca onboarding still requires the separate invite → accept → optional API-token flow

### Shared-bot collaboration best practice

When the real goal is a human collaborator plus the bot working in the same lane — and the owner wants visibility into the collaborator's interaction history — prefer a **shared Telegram group/topic** over private DMs.

Recommended shared-group pattern:
- put owner + collaborator + Hermes bot in the same Telegram group or forum topic
- allowlist the group chat via `TELEGRAM_ALLOWED_CHATS` and `TELEGRAM_GROUP_ALLOWED_CHATS`
- keep `telegram.require_mention: true` so the bot only responds when explicitly triggered
- optionally enable `TELEGRAM_OBSERVE_UNMENTIONED_GROUP_MESSAGES=true` if you want the bot to observe group chatter for context without auto-replying
- if Telegram privacy mode prevents normal group visibility, either disable privacy mode in BotFather and re-add the bot, or promote the bot to group admin

This gives better auditability and collaboration than DM-only workflows.

### Group-only access while blocking collaborator DMs

If the owner wants a collaborator to use a shared Hermes bot **only inside a shared Telegram group**, do not add that collaborator to `TELEGRAM_ALLOWED_USERS`.

Use this pattern instead:
- keep `TELEGRAM_ALLOWED_USERS` limited to the owner/operator accounts that may DM the bot directly
- allowlist the shared Telegram group chat ID in both `TELEGRAM_ALLOWED_CHATS` and `TELEGRAM_GROUP_ALLOWED_CHATS`
- keep `telegram.require_mention: true` so the bot only replies when explicitly invoked in the group

Important nuance:
- once a group chat is allowlisted by chat ID, any member of that allowed group can trigger the bot there
- so the group should be a deliberately scoped private collaboration chat, not a broad team room

This is the clean way to get:
- **no collaborator DM access**
- **yes collaborator group access**

without needing per-user Telegram sender rules for the group path.

### Finding the Telegram group ID

After the bot has seen at least one message in the target group, prefer Hermes' own observed data to discover the chat ID:
- inspect the profile's `channel_directory.json`, or
- use Hermes channel/target listing to read the observed Telegram chat identifier

Use that numeric Telegram group ID (usually `-100...`) for `TELEGRAM_ALLOWED_CHATS` and `TELEGRAM_GROUP_ALLOWED_CHATS`.

### Shared Hermes profile credential caveat

Do not imply that adding a collaborator's `openai-codex` login to an **existing shared Hermes profile** creates sender-specific billing or provider isolation.

Current practical behavior to assume:
- a Hermes profile has one shared credential pool (`auth.json`) for that profile
- adding another provider login to the same profile adds another shared credential entry to that pool
- it does **not** mean "JT uses JT's Codex account when JT speaks, while the user uses the user's account when the user speaks" unless custom sender→credential routing has been implemented separately

Operational guidance:
- **shared profile + shared bot** is the fast path, but provider spend is effectively shared at the profile level
- if true per-user provider ownership matters, prefer **separate Hermes profiles/bots** or a custom sender-to-token bridge, not multiple device logins into one shared profile

### Skills isolation caveat for shared profiles

Do not assume `skills.external_dirs` redirects where new skills are written.

Current Hermes behavior:
- `skills.external_dirs` are scanned/indexed alongside the local profile skills directory
- external dirs are effectively **read-only discovery locations**
- new skills created by the agent still go to the profile-local skills directory under that profile's `HERMES_HOME`

So if an operator wants a shared collaborator-facing profile to accumulate self-improvement changes only in a reviewed worktree path, that requires an explicit workflow or code/config guardrail beyond merely setting `skills.external_dirs`.

See also:
- `references/shared-hermes-profile-collaboration.md`

### Recommended token strategy

Prefer these modes explicitly:
- **Fast/shared-bot path:** one bot-held project-scoped token used for all Telegram users talking to that bot
- **Better per-user path:** invite the collaborator into Athabasca first, then mint a token for **that collaborator's `userId`**, and have the bot bridge map Telegram sender ID to that user's Athabasca token

When advising the user, name the tradeoff:
- shared token = fastest, but actions attribute to the token owner
- per-user token mapping = more setup, but correct attribution and cleaner revocation

### Important current model: global owner token now exists

Do not claim that Athabasca only supports project-scoped non-expiring tokens. Verify the live code first.

Current supported superadmin pattern:
- `projectScopes: []`
- requested `operationModes` include `"owner"`
- token is created by an authenticated owner for their own user
- `expiresInDays: null` is allowed for a non-expiring token

Semantics:
- zero project scopes on an owner-mode token means **global owner access**, not "no access"
- the token should reach all current and future projects automatically
- `GET /api/projects` with that token should return all projects

Guardrails:
- do not treat all zero-scope tokens as global; this behavior is specific to owner-mode superadmin tokens
- do not mint these for collaborators by default
- keep collaborator/bot tokens project-scoped unless the explicit goal is owner-level cross-project automation

Recommended usage split:
- collaborator/bot with narrow access → project-scoped token
- owner/operator automation across the whole system → zero-scope owner token

Reference: `references/global-owner-token-and-client-helper.md`

## Provider-grant pitfall

A recurring subtlety in multi-user Athabasca auth:
- project membership and login may work
- provider-backed generation may still fail if provider access is enforced separately (for example via user-scoped provider grants)

So after onboarding, if the collaborator is expected to generate media:
- verify whether provider grants are seeded at invite time
- if not, route through the current provider-grant admin path or implementation-specific setup
- do not promise generation capability just because login and project visibility work

## Verification checklist

Minimum successful handoff means all of the following are true:
- collaborator can reach `http://<tailscale-ip>:3000/api/health`
- collaborator can open the invite link
- collaborator can create/activate their account
- collaborator can sign in after acceptance
- collaborator sees only the intended project(s)
- collaborator can perform the intended project action (not just load the dashboard)
- if agent access was requested, the scoped bearer token works
- if generation was requested, provider-backed actions work too

## Pitfalls

- Do not tell the owner to use **Add device** when the goal is sharing access with another human.
- Do not start with Athabasca invite instructions before network reachability is proven.
- Do not assume an owner-facing invite UI exists; if the implementation is API-first, say so and use the API path.
- Do not assume API token creation is part of invite acceptance.
- Do not assume provider access is inherited from project membership.
- Do not skip the exact-email warning for invite acceptance.

## Communication pattern

When the user asks "what do I do in Tailscale, Telegram, send invite, etc.", answer in this order:
1. Tailscale reachability
2. Athabasca invite creation
3. Invite link delivery
4. Invitee acceptance
5. Optional Telegram/Hermes token
6. Verification

Keep the explanation operational and concrete. The point is to get a real collaborator in, not to explain auth architecture abstractly.

References:
- `references/invite-and-tailscale-sequence.md`
- `references/telegram-bot-athabasca-bridging.md`
- `references/master-token-limitations.md` — historical auth-model notes from before zero-scope owner tokens existed
- `references/global-owner-token-and-client-helper.md` — current owner-token semantics, Hermes env placement, and the `.hermes/plugins/athabasca-api` plugin pattern
- `templates/python-athabasca-bearer-client.py` — minimal bot-side helper that centralizes Athabasca bearer-token injection
