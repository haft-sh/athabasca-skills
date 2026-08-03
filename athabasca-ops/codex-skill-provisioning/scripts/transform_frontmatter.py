#!/usr/bin/env python3
"""Transform Hermes SKILL.md frontmatter to Codex format and generate agents/openai.yaml.

Usage: python3 transform_frontmatter.py <skills_dir> <skill1> [skill2 ...]

Strips Hermes-specific frontmatter (metadata, triggers, author, license),
keeps name/description/version, and creates agents/openai.yaml for each skill.
"""
import os, re, sys

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml")
    sys.exit(1)


def title_case(name):
    """Convert skill name to display title, stripping common prefixes."""
    for prefix in ("athabasca-", "haft-"):
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    return name.replace("-", " ").title()


def fix_frontmatter(content):
    """Strip Hermes-specific fields from YAML frontmatter."""
    if not content.startswith("---"):
        return content
    end = content.find("---", 3)
    if end == -1:
        return content
    fm_text = content[3:end].strip()
    body = content[end + 3:]
    try:
        fm = yaml.safe_load(fm_text)
    except Exception:
        return content
    if not isinstance(fm, dict):
        return content

    # Remove Hermes-specific fields
    for key in ("metadata", "triggers", "author", "license"):
        fm.pop(key, None)

    # Keep only Codex-compatible fields
    clean_fm = {}
    for key in ("name", "description", "version"):
        if key in fm:
            clean_fm[key] = fm[key]

    new_fm = yaml.dump(clean_fm, default_flow_style=False,
                       allow_unicode=True, sort_keys=False).strip()
    return "---\n" + new_fm + "\n---" + body


def make_openai_yaml(name, description):
    """Generate agents/openai.yaml content."""
    display = title_case(name)
    short = description[:61] + "..." if len(description) > 64 else description
    prompt = "Use $" + name + " to help with creative writing and production tasks."
    return (
        'interface:\n'
        '  display_name: "' + display + '"\n'
        '  short_description: "' + short + '"\n'
        '  default_prompt: "' + prompt + '"\n'
    )


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 transform_frontmatter.py <skills_dir> <skill1> [skill2 ...]")
        sys.exit(1)

    skills_dir = sys.argv[1]
    skill_names = sys.argv[2:]

    for name in skill_names:
        skill_dir = os.path.join(skills_dir, name)
        skill_file = os.path.join(skill_dir, "SKILL.md")
        if not os.path.exists(skill_file):
            print("SKIP (no SKILL.md): " + name)
            continue

        with open(skill_file, "r") as f:
            content = f.read()

        # Extract description before modifying
        desc_match = re.search(
            r'^description:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE
        )
        description = desc_match.group(1) if desc_match else "Creative skill: " + name

        # Fix frontmatter
        new_content = fix_frontmatter(content)
        with open(skill_file, "w") as f:
            f.write(new_content)

        # Create agents/openai.yaml
        agents_dir = os.path.join(skill_dir, "agents")
        os.makedirs(agents_dir, exist_ok=True)
        yaml_path = os.path.join(agents_dir, "openai.yaml")
        with open(yaml_path, "w") as f:
            f.write(make_openai_yaml(name, description))

        print("OK: " + name)

    print("\nDone. Transformed %d skills." % len(skill_names))


if __name__ == "__main__":
    main()
