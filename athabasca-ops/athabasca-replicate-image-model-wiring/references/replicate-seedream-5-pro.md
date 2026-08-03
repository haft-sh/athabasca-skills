# Replicate Seedream 5 Pro

## Verified model identity

- Provider: `replicate`
- Model slug: `bytedance/seedream-5-pro`
- Replicate page: `replicate.com/bytedance/seedream-5-pro/api`
- Status observed during wiring: public official model

## Why this matters

A guessed slug like `bytedance/seedream-5` failed upstream even after local runtime patching. The durable lesson is to verify the exact model slug first, then wire Athabasca.

## Verified schema notes

Observed through Replicate model metadata during runtime wiring:

- `prompt`: required
- `image_input`: optional, list of 1-10 reference images
- `size`: `1K` or `2K`
- `aspect_ratio`: `match_input_image`, `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `3:2`, `2:3`, `21:9`
- `output_format`: `png` or `jpeg`

## Adapter shape that worked

For Athabasca's Replicate image worker, the successful model-specific payload shape was:

- `prompt`
- `aspect_ratio`
- `size: "2K"`
- `output_format: "png"`
- `image_input` when references are present, capped to 10 URLs

## Runtime-specific lesson that generalizes

The first cheap probe succeeded, but the real reference-heavy room generation timed out because the worker's polling window was too short. Extending the Replicate image polling timeout from 120 seconds to 300 seconds allowed the real generation to complete.

## Operational pattern

1. verify page + model API
2. wire validation/config/worker support
3. run cheap probe through Athabasca project API
4. if probe works but real generation times out, inspect poll timeout before blaming model compatibility
5. only then present the model as supported
