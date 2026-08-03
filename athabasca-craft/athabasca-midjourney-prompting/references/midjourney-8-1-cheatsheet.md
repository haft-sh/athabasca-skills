# Midjourney 8.1 Cheat Sheet for Athabasca

Last researched: 2026-05-13

## Officially observed source facts

From Midjourney docs and updates during authoring:

- Prompts work best when short, clear, descriptive, and focused.
- Put parameters at the end of the prompt.
- Describe what you want, not what you want to avoid. (`--no` is not supported in V8.1.)
- Prompt elements to consider: subject, medium, environment, lighting, color, mood, composition.
- Image prompts influence content, composition, and colors.
- Discord image prompt syntax places valid image URLs at the beginning of the prompt.
- Style references use `--sref` and influence vibe: colors, medium, textures, lighting, and mood.
- `--sw` controls style-reference strength from 0 to 1000; default is 100.
- Multiple `--sref` URLs can be weighted like `URL1::2 URL2::1`.
- Parameters include `--ar`, `--v`, `--s`, `--c`, `--q`, `--seed`, `--tile`, `--iw`, `--sref`, `--sw`, `--style raw`, speed modes, and visibility modes. (Note: `--no` is NOT supported in V8.1 — confirmed May 2026.)
- V8.1 alpha update says V8.1 restored image prompts and image weights, improved style reference/moodboard stability, made HD faster/cheaper, and updated Describe/prompt-shortening behavior.

## Practical V8.1 defaults

Use as starting points:

```text
--v 8.1 --ar 16:9 --s 180
```

For controlled production stills:

```text
--v 8.1 --ar 16:9 --s 100-250 --c 5-15
```

For more exploratory visual development:

```text
--v 8.1 --ar 16:9 --s 250-450 --c 15-35
```

For realism / less Midjourney gloss:

```text
--v 8.1 --style raw --ar 16:9 --s 100-200
```

For style references:

```text
--sref [STYLE_URL] --sw 100-150
```

For image prompts:

```text
[IMAGE_URL] prompt text --iw 0.75-1.5 --v 8.1
```

## Reference-type decision guide

- Need content/layout/color influence from a source image: use image prompt URL(s) at the beginning.
- Need aesthetic/vibe transfer: use `--sref`.
- Need exact person/object/character carryover: check current Midjourney support. Official Omni Reference documentation observed during authoring describes `--oref` as V7-only; use V7 fallback if needed.

## Discord syntax patterns

Text only:

```text
/imagine prompt: cinematic animation still of [subject], [action], [setting], [composition], [lighting], [style] --ar 16:9 --v 8.1
```

Image prompt:

```text
/imagine prompt: [IMAGE_URL] cinematic animation still of [subject], [action], [setting] --iw 1.2 --ar 16:9 --v 8.1
```

Style reference:

```text
/imagine prompt: cinematic animation still of [subject], [action], [setting] --sref [STYLE_URL] --sw 125 --ar 16:9 --v 8.1
```

Combined:

```text
/imagine prompt: [IMAGE_URL] cinematic animation still of [subject], [action], [setting], [composition], [lighting] --iw 1.15 --sref [STYLE_URL] --sw 125 --ar 16:9 --v 8.1
```

## Web UI notes

- Use the image icon in the Imagine bar.
- Drag images into the intended section: Image Prompt, Style Reference, Omni Reference, or Starting Frame, depending on the UI's current options.
- Pin references with the lock icon when generating multiple related frames.
- When using web reference slots, the text prompt can omit URL syntax, but still include the same final-image description and parameters.

## Useful negative prompts

Keep short:

```text
--no text, watermark, logo
```

For animation stills:

```text
--no text, watermark, logo, subtitles, extra limbs
```

For clean concept art:

```text
--no text, watermark, logo, border, frame
```

Avoid giant negative lists; they often dilute the prompt.
