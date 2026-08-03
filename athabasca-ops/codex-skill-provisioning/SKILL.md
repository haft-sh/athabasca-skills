---
name: codex-skill-provisioning
description: Adapt Hermes skills to Codex/ChatGPT worker format and deploy them to a remote .codex/skills directory. Covers frontmatter transformation, agents/openai.yaml generation, batch transfer, and verification.
version: 1.0.0
---

# Codex Skill Provisioning

Use when migrating, updating, or creating skills for a Codex/ChatGPT worker's `~/.codex/skills/` directory. This covers the format adaptation from Hermes skill format to Codex skill format, file transfer, and verification.

## Codex Skill Format

A Codex skill is a directory under `~/.codex/skills/<skill-name>/` containing:

```
<skill-name>/
  SKILL.md              # Main skill document (same structure as Hermes)
  agents/openai.yaml    # Required: ChatGPT/Codex interface metadata
  references/           # Optional: supporting docs (same as Hermes)
  scripts/              # Optional: helper scripts
  assets/               # Optional: icons, images
```

### SKILL.md Frontmatter (Codex-compatible)

Keep ONLY these fields:
- `name` — skill identifier (kebab-case)
- `description` — one-line description
- `version` — semver (optional)

STRIP these Hermes-specific fields:
- `metadata.hermes.tags`
- `metadata.hermes.related_skills`
- `triggers`
- `author`
- `license`

### agents/openai.yaml

Required for ChatGPT worker discovery. Structure:

```yaml
interface:
  display_name: "Human Readable Title"
  short_description: "25-64 char summary for UI scanning"
  default_prompt: "Use $skill-name to help with [task class]."
```

Rules:
- Quote ALL string values
- `default_prompt` MUST reference the skill as `$skill-name` (with dollar sign)
- `short_description` must be 25-64 characters
- `display_name` is Title Case derived from the skill name

Optional extended fields (rarely needed):
- `interface.icon_small`, `interface.icon_large` — paths to assets
- `interface.brand_color` — hex color
- `dependencies.tools[]` — MCP tool dependencies
- `policy.allow_implicit_invocation` — defaults true; false = explicit `$skill` only

## Migration Workflow (Hermes → Codex)

1. **Identify skills** to migrate from the Hermes skill directory
2. **rsync** skill directories (including `references/`) to the remote `.codex/skills/`
3. **Transform frontmatter** — strip Hermes fields, keep name/description/version
4. **Generate `agents/openai.yaml`** for each skill
5. **Verify** — check head of SKILL.md and openai.yaml on remote

### Batch Transfer Pattern

```bash
# Push EC2 Instance Connect key (60-second TTL!)
aws ec2-instance-connect send-ssh-public-key \
  --region <region> \
  --instance-id <id> \
  --instance-os-user ubuntu \
  --ssh-public-key file:///tmp/key.pub \
  --availability-zone <az>

# Immediately rsync (key expires in 60s — batch accordingly)
rsync -az --delete -e "ssh -i /tmp/key" "$SRC/$skill/" "ubuntu@<tailscale-ip>:/home/ubuntu/.codex/skills/$skill/"
```

### Frontmatter Transform Script

See `scripts/transform_frontmatter.py` for a reusable Python script that strips Hermes fields and generates openai.yaml.

## Pitfalls

- **EC2 Instance Connect keys expire in 60 seconds.** If rsyncing multiple large skills, re-push the key between batches. A batch of ~9 medium skills fit in one window; 11+ may need two pushes.
- **SSM agent may report offline** even when the instance is healthy. Fall back to EC2 Instance Connect + Tailscale SSH rather than waiting for SSM.
- **Unicode in SKILL.md body is fine** — Codex reads UTF-8. Only the PDF/export path needs latin-1 sanitization.
- **Don't strip `references/` content** — Codex workers can read reference files the same way Hermes does.
- **The `.system/` directory** in `.codex/skills/` is Codex-managed (skill-creator, imagegen). Don't touch it.

## Verification

After deployment, verify from the remote:
```bash
# Check all skills present
ls -1 ~/.codex/skills/ | grep <prefix>

# Spot-check frontmatter
head -8 ~/.codex/skills/<name>/SKILL.md

# Verify openai.yaml exists and is valid
cat ~/.codex/skills/<name>/agents/openai.yaml
```

The ChatGPT worker discovers skills by scanning `~/.codex/skills/*/SKILL.md` and reading `agents/openai.yaml` for UI metadata.
