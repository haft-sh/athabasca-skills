# Reference-to-video dispatch integrity

## Packet text is execution source

When a reviewed prompt packet contains the intended group prompt, dispatch its exact extracted `<pre>` payload. Do not summarize, rewrite, condense, or reconstruct it. Permit only explicitly approved deltas, ideally appended as a narrowly scoped correction; retain the original wording, shot order, camera, composition, focus, and emotion clauses.

Before submission, normalize line endings only and record a hash/equality check between the extracted packet block and submitted prompt.

## Reference manifest is separate from prompt text

Build a per-group manifest before dispatch:

| Slot | Authority | Scope |
|---|---|---|
| identity | canonical full-body / neutral pose | silhouette, costume, scale |
| expression | emote sheet | face/visor performance only |
| environment | one designated location master | geography and production design |
| prop | prop design reference | exact object silhouette/material |
| posture | emotional performance frame | body state only |

Do not replace an identity reference with an emote sheet. When both are needed, attach both and explicitly distinguish their scopes in the packet.

## Avoid competing authorities

Multiple images are valid when each governs a distinct dimension. Remove only genuinely overlapping environment/location images; do not discard an emotional-posture or expression reference merely because it is an additional image. If a provider returns an ambiguous failure, do not infer a reference-count limit from a single run; retry with a fresh idempotency key and compare verified request manifests.

## Required verification

After generation, verify the persisted request references by URL and order, then review representative frames against each authority. Diagnose separately:

- **packet-to-dispatch drift:** prompt compression, altered text, wrong URL/order, omitted reference;
- **reference-to-render drift:** provider failed to preserve an accurately attached authority.
