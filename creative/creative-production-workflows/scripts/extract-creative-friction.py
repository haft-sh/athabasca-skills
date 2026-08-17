#!/usr/bin/env python3
"""Extract human-reviewable friction episodes from redacted Hermes JSONL exports."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TAXONOMY = SKILL_ROOT / "references" / "creative-friction-taxonomy.json"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_no}: expected JSON object")
        rows.append(value)
    return rows


def compile_signals(taxonomy: dict[str, Any]) -> list[dict[str, Any]]:
    compiled = []
    for signal in taxonomy["signals"]:
        patterns = [
            re.compile(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", re.IGNORECASE)
            for phrase in signal["patterns"]
        ]
        compiled.append({**signal, "compiled_patterns": patterns})
    return compiled


def clean_message(message: dict[str, Any]) -> dict[str, Any]:
    content = message.get("content")
    if not isinstance(content, str):
        content = json.dumps(content, ensure_ascii=False) if content is not None else ""
    return {
        "id": message.get("id"),
        "role": message.get("role"),
        "timestamp": message.get("timestamp"),
        "tool_name": message.get("tool_name"),
        "content": content,
    }


def detect(text: str, signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    matches = []
    for signal in signals:
        phrases = [
            phrase
            for phrase, pattern in zip(signal["patterns"], signal["compiled_patterns"])
            if pattern.search(text)
        ]
        if phrases:
            matches.append(
                {
                    "type": signal["type"],
                    "confidence": signal["confidence"],
                    "matched_phrases": phrases,
                }
            )
    return matches


def prior_user(messages: list[dict[str, Any]], anchor: int) -> int:
    for index in range(anchor - 1, -1, -1):
        if messages[index].get("role") == "user":
            return index
    return max(0, anchor - 6)


def next_user(messages: list[dict[str, Any]], anchor: int) -> int:
    for index in range(anchor + 1, len(messages)):
        if messages[index].get("role") == "user":
            return index
    return min(len(messages) - 1, anchor + 6)


def extract(rows: list[dict[str, Any]], signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    episodes: list[dict[str, Any]] = []
    for session in rows:
        messages = session.get("messages") or []
        if not isinstance(messages, list):
            continue
        for index, message in enumerate(messages):
            if message.get("role") != "user":
                continue
            content = message.get("content")
            text = content if isinstance(content, str) else ""
            matches = detect(text, signals)
            if not matches:
                continue
            start = prior_user(messages, index)
            end = next_user(messages, index)
            episodes.append(
                {
                    "schema": "creative-friction-episode-v1",
                    "episode_id": f"{session.get('id')}:{message.get('id', index)}",
                    "session_id": session.get("id"),
                    "session_title": session.get("title"),
                    "workspace": session.get("cwd"),
                    "anchor_message_id": message.get("id"),
                    "anchor_timestamp": message.get("timestamp"),
                    "signals": matches,
                    "correction": clean_message(message),
                    "preceding_context": [clean_message(item) for item in messages[start:index]],
                    "recovery_window": [clean_message(item) for item in messages[index + 1 : end + 1]],
                    "human_label": "needs-review",
                    "root_causes": [],
                    "resolution_status": "unknown",
                    "resolution_metrics": {},
                    "what_should_change": "",
                    "include_in_optimizer": False,
                }
            )
    return episodes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="secret-redacted Hermes session JSONL")
    parser.add_argument("output", type=Path, help="candidate friction episode JSONL")
    parser.add_argument("--taxonomy", type=Path, default=DEFAULT_TAXONOMY)
    args = parser.parse_args()

    taxonomy = json.loads(args.taxonomy.read_text(encoding="utf-8"))
    episodes = extract(load_jsonl(args.input), compile_signals(taxonomy))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for episode in episodes:
            handle.write(json.dumps(episode, ensure_ascii=False) + "\n")

    counts: dict[str, int] = {}
    for episode in episodes:
        for signal in episode["signals"]:
            kind = signal["type"]
            counts[kind] = counts.get(kind, 0) + 1
    print(f"friction_candidates={len(episodes)}")
    print("signal_counts=" + json.dumps(counts, sort_keys=True))
    print(f"output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
