#!/usr/bin/env python3
"""Minimal Athabasca bearer-token client for bot/server-side integrations.

Use this when a Hermes/Telegram profile needs to call Athabasca but there is no
existing single bridge module that already owns outbound Athabasca requests.
Keep the raw token on the bot/server side only.

Raw usage:
  python-athabasca-bearer-client.py GET /api/health
  python-athabasca-bearer-client.py GET /api/projects
  python-athabasca-bearer-client.py POST /api/projects/my-slug/research-report '{"phase":"research","content":"..."}'

Convenience commands:
  python-athabasca-bearer-client.py list-projects
  python-athabasca-bearer-client.py get-project good-boy
  python-athabasca-bearer-client.py project-path good-boy storyboard
  python-athabasca-bearer-client.py project-get good-boy storyboard
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

BASE_URL = os.environ.get("ATHABASCA_BASE_URL", "").rstrip("/")
API_TOKEN = os.environ.get("ATHABASCA_API_TOKEN", "")
DEFAULT_PROJECT_SLUG = os.environ.get("ATHABASCA_PROJECT_SLUG", "")
TIMEOUT_SECONDS = int(os.environ.get("ATHABASCA_HTTP_TIMEOUT", "120"))

if not BASE_URL:
    raise SystemExit("Missing ATHABASCA_BASE_URL")
if not API_TOKEN:
    raise SystemExit("Missing ATHABASCA_API_TOKEN")


def request(method: str, path: str, body: Any = None) -> tuple[int, Any]:
    if not path.startswith("/"):
        path = "/" + path
    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {"ok": False, "error": raw}
        return e.code, payload


def project_path(project_slug: str | None = None, suffix: str = "") -> str:
    slug = project_slug or DEFAULT_PROJECT_SLUG
    if not slug:
        raise ValueError("project_slug required when ATHABASCA_PROJECT_SLUG is unset")
    suffix = suffix or ""
    if suffix and not suffix.startswith("/"):
        suffix = "/" + suffix
    return f"/api/projects/{slug}{suffix}"


def _parse_body(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON body: {exc}") from exc


def _print_result(status: int, payload: Any) -> None:
    print(json.dumps({"status": status, "payload": payload}, indent=2))


def _usage() -> str:
    return (
        "usage:\n"
        "  python-athabasca-bearer-client.py METHOD PATH [JSON_BODY]\n"
        "  python-athabasca-bearer-client.py list-projects\n"
        "  python-athabasca-bearer-client.py get-project <slug>\n"
        "  python-athabasca-bearer-client.py project-path <slug|-> [suffix]\n"
        "  python-athabasca-bearer-client.py project-get <slug|-> [suffix]\n"
        "  python-athabasca-bearer-client.py project-post <slug|-> [suffix] <JSON_BODY>\n"
        "\n"
        "Use '-' for <slug> to fall back to ATHABASCA_PROJECT_SLUG."
    )


def _resolve_slug(raw: str | None) -> str | None:
    if raw in (None, "", "-"):
        return None
    return raw


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(_usage(), file=sys.stderr)
        raise SystemExit(2)

    command = args[0]

    if command == "list-projects":
        status, payload = request("GET", "/api/projects")
        _print_result(status, payload)
        return

    if command == "get-project":
        if len(args) != 2:
            print("usage: python-athabasca-bearer-client.py get-project <slug>", file=sys.stderr)
            raise SystemExit(2)
        status, payload = request("GET", project_path(args[1]))
        _print_result(status, payload)
        return

    if command == "project-path":
        if len(args) not in (2, 3):
            print("usage: python-athabasca-bearer-client.py project-path <slug|-> [suffix]", file=sys.stderr)
            raise SystemExit(2)
        slug = _resolve_slug(args[1])
        suffix = args[2] if len(args) == 3 else ""
        print(project_path(slug, suffix))
        return

    if command == "project-get":
        if len(args) not in (2, 3):
            print("usage: python-athabasca-bearer-client.py project-get <slug|-> [suffix]", file=sys.stderr)
            raise SystemExit(2)
        slug = _resolve_slug(args[1])
        suffix = args[2] if len(args) == 3 else ""
        status, payload = request("GET", project_path(slug, suffix))
        _print_result(status, payload)
        return

    if command == "project-post":
        if len(args) != 4:
            print("usage: python-athabasca-bearer-client.py project-post <slug|-> [suffix] <JSON_BODY>", file=sys.stderr)
            raise SystemExit(2)
        slug = _resolve_slug(args[1])
        suffix = args[2]
        body = _parse_body(args[3])
        status, payload = request("POST", project_path(slug, suffix), body)
        _print_result(status, payload)
        return

    if len(args) < 2:
        print(_usage(), file=sys.stderr)
        raise SystemExit(2)

    method = args[0]
    path = args[1]
    body = _parse_body(args[2]) if len(args) > 2 else None
    status, payload = request(method, path, body)
    _print_result(status, payload)


if __name__ == "__main__":
    main()
