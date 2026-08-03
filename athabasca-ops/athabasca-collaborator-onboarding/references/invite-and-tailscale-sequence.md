# Invite + Tailscale sequence

Use this as a concrete operator checklist when onboarding one external collaborator to one Athabasca box.

## Decision rule from the Tailscale UI

If the user is choosing between **Add device** and **Share machine**:

- **Add device** = add the owner's own new laptop/phone to the owner's tailnet
- **Share machine** = give another human access to this one machine

For a one-box external collaborator, prefer **Share machine**.
For broader ongoing teammate access to several machines, prefer inviting them to the **tailnet** instead.

## Practical sequence

1. Share the Athabasca host in Tailscale or invite them to the tailnet.
2. Have them verify they can load:
   - `http://<tailscale-ip>:3000/api/health`
3. Create an Athabasca invite.
4. Send:
   - `http://<tailscale-ip>:3000/?invite=<raw_token>`
5. Tell them to accept using the **exact invited email**.
6. After acceptance, verify project visibility and intended write access.
7. Only then create a scoped API token if Telegram/Hermes access is needed.

## Implementation observations worth re-checking

These were true in one live Athabasca implementation and should be re-verified in future sessions before presenting as facts:

- unauthenticated `GET /api/auth/me` returned `{"ok":false,"error":"Authentication required"}`
- `GET /api/health` confirmed the app was up and R2 was configured
- invite creation path existed at `POST /api/auth/invitations`
- invite acceptance path existed at `POST /api/auth/invitations/accept`
- API token creation path existed at `POST /api/auth/api-tokens`
- frontend invite links were accepted via `/?invite=<token>`

## Subtle auth pitfall

If the auth model includes separate user-scoped provider grants, successful invite acceptance may still be insufficient for provider-backed generation. Confirm whether provider grants are seeded during invite onboarding or require a separate admin step.
