# Phone Screen Generation

Patterns for generating smartphone screen UI shots where the phone content itself carries narrative meaning.

## Aspect Ratio

Always use `portrait` for phone screen shots.

## UI Platform Language

- Specify the platform explicitly, e.g. `dark mode Twitter/X interface`
- For feeds: say `Twitter/X feed being doom-scrolled`
- For composers: say `Twitter/X post composer` and specify the exact text if legibility matters

## Narrative Text Rule

When generating phone screens with visible posts, messages, or notifications, the text should be narratively relevant rather than placeholder filler.

Always specify exact text when the content matters. If left vague, image models often invent unreadable or off-story UI text.

## Context and Framing

Phone screens are usually held by a character in a specific place. Include:
- where the character is
- what is visible around the phone
- lighting that matches the surrounding scene

Example framing:
> The phone is held by someone lying on a couch. Sofa fabric and living-room ceiling are visible in the softly blurred background. Bright daytime natural light from windows.

## Provider Routing

Use `fal-ai` + `openai/gpt-image-2` with `referenceAssetIds` pointing to the canonical environment when room continuity matters.

```json
{
  "provider": "fal-ai",
  "model": "openai/gpt-image-2",
  "aspectRatio": "portrait",
  "referenceAssetIds": ["canonical environment asset ID"]
}
```

## Pitfalls

- UI text may render garbled; be explicit about exact text content
- The phone screen should be the focus, not the background set
- Avoid dramatic spotlight language unless the surrounding scene actually wants it
- If a thumbnail or selfie appears on the phone, describe only the visible story function unless a strict likeness lock is required

## Generic Prompt Patterns

### Doom-scrolling feed

```text
Smartphone screen showing a dark mode Twitter/X feed being doom-scrolled. The visible posts are narratively relevant to the surrounding scene and use the following exact text: "...". The phone screen is the focus, shot from above as if POV of the person scrolling. The surrounding room remains softly blurred in the background. Bright natural ambient light. Photorealistic. Portrait orientation.
```

### Post composer

```text
Smartphone screen showing a dark mode Twitter/X post composer. The post text reads exactly: "...". The primary action button is visible and prominent. The phone is held in the current scene environment, which remains softly blurred behind the screen. Photorealistic. Portrait orientation.
```

## Anti-Bloat Rule

Keep reusable UI-shot patterns here. Do not preserve one production's exact tweets, usernames, or character-specific gag copy unless they are serving as a temporary worked example somewhere else.