# Direct GPT Image 2 Reference Edits via Codex Responses API

Use this when the user explicitly wants **GPT Image 2** and needs a **reference-based edit** anchored to one or more existing Athabasca media assets.

Why this exists:
- the exposed `image_generate` tool surface in this environment does not take reference images
- the reliable working path is the ChatGPT/Codex Responses API with `input_image` parts and the `image_generation` tool
- the wrapped Athabasca `/generate/image` path with `provider=openai-codex` has been unreliable for this workflow and should not be the first choice

## Working Pattern

1. Resolve Athabasca asset IDs to `publicUrl` values via `GET /api/media/:assetId`
2. Build a Codex Responses request with:
   - `model: "gpt-5.4"`
   - `tools: [{"type":"image_generation","model":"gpt-image-2",...}]`
   - `tool_choice` forced to `image_generation`
   - `stream: true`
3. Put reference images in the user message as alternating text/image parts
4. Assign each reference a role explicitly:
   - reference 1 = composition or scene anchor
   - reference 2 = prop, costume, or face detail only
5. Parse SSE events and keep the latest image payload
6. Save the decoded PNG locally
7. Verify locally, then persist through `POST /api/projects/:slug/media`
8. If this is part of a shot workflow, also attach via `POST /api/projects/:slug/shots/:shotId/media`

## Working Python Implementation

```python
import json, base64, urllib.request
from pathlib import Path

def load_codex_headers():
    payload = json.loads(Path('/home/nrsimha/.hermes/auth.json').read_text())
    tokens = payload['providers']['openai-codex']['tokens']
    access = tokens['access_token']
    parts = access.split('.')
    claims = {}
    if len(parts) > 1:
        p = parts[1] + '=' * ((4 - len(parts[1]) % 4) % 4)
        claims = json.loads(base64.urlsafe_b64decode(p.encode()).decode())
    account = claims.get('https://api.openai.com/auth', {}).get('chatgpt_account_id') or tokens.get('account_id')
    headers = {
        'Authorization': f'Bearer {access}',
        'Content-Type': 'application/json',
        'User-Agent': 'codex_cli_rs/0.0.0 (Athabasca direct ref edit)',
        'originator': 'codex_cli_rs',
    }
    if account:
        headers['ChatGPT-Account-ID'] = account
    return headers

HEADERS = load_codex_headers()

def codex_reference_edit(parts, outpath):
    body = {
        'model': 'gpt-5.4',
        'stream': True,
        'store': False,
        'instructions': 'You are an assistant that must fulfill image generation requests by using the image_generation tool when provided.',
        'input': [{'type': 'message', 'role': 'user', 'content': parts}],
        'tools': [{
            'type': 'image_generation',
            'model': 'gpt-image-2',
            'size': '1536x1024',
            'quality': 'medium',
            'output_format': 'png',
            'background': 'opaque',
            'partial_images': 1
        }],
        'tool_choice': {
            'type': 'allowed_tools',
            'mode': 'required',
            'tools': [{'type': 'image_generation'}]
        }
    }
    url = 'https://chatgpt.com/backend-api/codex/responses'
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HEADERS, method='POST')
    text = urllib.request.urlopen(req, timeout=300).read().decode('utf-8', 'replace')

    img_b64 = None
    for line in text.splitlines():
        if not line.startswith('data: '):
            continue
        data = line[6:]
        if data == '[DONE]':
            continue
        try:
            obj = json.loads(data)
        except Exception:
            continue
        if obj.get('type') == 'response.image_generation_call.partial_image':
            img_b64 = obj.get('partial_image_b64') or img_b64
        elif obj.get('type') == 'response.output_item.done':
            item = obj.get('item') or {}
            if item.get('type') == 'image_generation_call' and item.get('result'):
                img_b64 = item.get('result')

    if not img_b64:
        raise RuntimeError('no image payload found in SSE stream')

    p = Path(outpath)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(base64.b64decode(img_b64))
    return p
```

## Usage Shape

```python
parts = [
    {'type': 'input_text', 'text': 'Reference image 1: composition anchor only.'},
    {'type': 'input_image', 'image_url': 'https://media.wheretoaccess.com/project/generated/anchor.png'},
    {'type': 'input_text', 'text': 'Reference image 2: secondary design detail only.'},
    {'type': 'input_image', 'image_url': 'https://media.wheretoaccess.com/project/generated/detail.png'},
    {'type': 'input_text', 'text': 'Create a medium shot preserving the first reference composition while transferring only the design detail from the second reference.'},
]
local_path = codex_reference_edit(parts, '/tmp/project-ref-edits/shot-v1.png')
```

Then verify locally and persist via `POST /api/projects/:slug/media`.

## Important Prompt Pattern

For minimal edits, say all of these explicitly:
- preserve the exact framing, staging, background, wardrobe, and lighting
- change only the requested object or attribute
- explain which reference controls the secondary design detail
- include guardrails like `do not widen the shot`, `do not add extra props`, and `keep realistic hand anatomy`

## Practical Caveats

**Vision rate limits** — if repeated vision checks fail during batch review, download images locally first and verify in a smaller number of combined calls.

**On HTTP 429 from Codex** — stop hammering the endpoint and switch to a fallback provider immediately.

**Do not treat the wrapped endpoint as authoritative** — if `POST /api/projects/:slug/generate/image` with `provider=openai-codex` fails for this workflow, use the direct Codex pattern above or fall back.

## Fallback Chain

```text
User asks for GPT Image 2 + multi-reference
  → try direct Codex Responses API
    → if HTTP 429: switch to Gemini or another supported fallback via Athabasca
```

Do not claim success until verification confirms:
- the requested change is visible
- the composition still matches the original shot
- the secondary reference details actually transferred