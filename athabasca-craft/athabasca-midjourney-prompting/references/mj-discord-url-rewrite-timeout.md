# Midjourney false timeout from Discord image-URL rewrite

## Symptom

Athabasca logs a Midjourney generation as timed out, but the user can already see the successful image in Discord.

## Confirmed cause pattern

This can happen when the submitted prompt begins with a project-media URL, for example an Athabasca `publicUrl` used as a Midjourney image prompt.

Athabasca submits something like:

```text
https://media.wheretoaccess.com/gly/misc/img_1b431c921d4e_1778712118067.jpg wide desert canyon location plate, two roughly hewn stone columns framing a natural vertical gap ... --iw 1.3 --ar 16:9 --v 8.1 --style raw
```

But the returned Discord message may begin with a rewritten short URL:

```text
**<https://s.mj.run/GKnPCjOKA5k> wide desert canyon location plate, two roughly hewn stone columns framing a natural vertical gap ... --iw 1.3 --ar 16:9 --v 8.1 --raw** - <@user> (fast)
```

If the poller compares the normalized full prompt string against the normalized Discord message content, the strings do not match because the leading URL changed.

## Evidence shape

The failure is not an upstream generation failure when all of these are true:
- Discord has a recent Midjourney message from bot id `936929561302675456`
- the message timestamp is after submission time
- the message contains the expected descriptive prompt body
- the message includes an attachment URL and completed grid buttons (`U1-U4`, `V1-V4`)
- Athabasca still recorded `Timed out waiting for Midjourney image after 180s`

## Fix

In `src/server/workers/midjourney-provider.ts`:
- strip leading image-prompt URLs before prompt normalization/matching
- keep submit-time gating so older jobs are still ignored
- add a regression test covering:
  - prompt starts with original Athabasca media URL
  - Discord content starts with `s.mj.run/...`
  - matcher still returns true

## Recovery playbook

When the user says the image is visible in Discord even though Athabasca logged a timeout:
1. inspect recent Discord channel messages
2. verify whether the prompt used a leading image URL
3. if Discord rewrote that URL, classify it as a matcher bug / false timeout
4. salvage the already-generated Discord image if needed instead of re-running blindly
5. patch the matcher and add the regression test before closing the issue
