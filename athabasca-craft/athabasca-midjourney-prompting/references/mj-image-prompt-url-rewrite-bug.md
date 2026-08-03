# Midjourney image-prompt URL rewrite bug

## Symptom

Athabasca logs a Midjourney generation as timed out even though the image grid is visible in Discord.

## Confirmed reproduction

- Submitted prompt begins with an Athabasca project-media URL, e.g. `https://media.wheretoaccess.com/...png`
- Midjourney/Discord returns a successful grid message
- Discord message rewrites the leading image URL to a shortened `https://s.mj.run/...` link
- Athabasca poller fails to match the returned message against the original prompt and times out

Observed successful Discord messages for this class of bug had:
- MJ bot author id `936929561302675456`
- attachment image URL present
- completed U/V buttons present
- content beginning with `**<https://s.mj.run/...>` instead of the original project-media URL

## Root cause

`src/server/workers/midjourney-provider.ts` matched Discord results by normalized prompt-string containment. When the original prompt started with a full Athabasca media URL, the returned Discord message no longer contained that same literal URL because Midjourney rewrote it to `s.mj.run`.

So generation succeeded upstream, but local result matching rejected the message and reported a false timeout.

## Durable fix

Before prompt matching:
1. Strip leading image-prompt URLs from both the submitted prompt and Discord message content
2. Then normalize markdown/params/whitespace and compare the descriptive body text

This preserves image-prompt workflows while surviving Discord URL rewriting.

## Regression test shape

Add a test where:
- submitted prompt starts with `https://media.wheretoaccess.com/...`
- returned message starts with `**<https://s.mj.run/...>`
- `messageMatchesPrompt(...)` still returns true

## Investigation pattern

If the user says "it timed out but I can see the image in Discord":
1. fetch recent channel messages
2. confirm the MJ grid exists and has attachments/buttons
3. compare the submitted prompt with returned message content
4. check whether the leading reference URL was rewritten to `s.mj.run`
5. classify as a prompt-matching bug, not an upstream timeout
