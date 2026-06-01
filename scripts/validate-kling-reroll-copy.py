#!/usr/bin/env python3
"""Validate Kling rerender guidance in curated skill docs."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_MARKERS = {
    "skills/app-sizzle/SKILL.md": (
        "Kling variation rule",
        "Do not submit an identical Kling payload",
        "change the payload",
    ),
    "skills/baseball-trend/SKILL.md": (
        "Kling variation rule",
        "Do not submit an identical Kling payload",
        "change the payload",
    ),
    "skills/kiss-cam/SKILL.md": (
        "Kling variation rule",
        "Do not submit an identical Kling payload",
        "change the payload",
    ),
    "skills/podcast/SKILL.md": (
        "Kling variation rule",
        "Do not submit an identical Kling payload",
        "change the payload",
    ),
    "skills/ugc-ads/SKILL.md": (
        "Kling variation rule",
        "Do not submit an identical Kling payload",
        "change the payload",
    ),
}

BANNED_PHRASES = (
    "to re-roll just call again",
    "re-rolls are non-reproducible",
)


def main() -> int:
    failures: list[str] = []

    for rel_path, markers in REQUIRED_MARKERS.items():
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        lower = text.lower()
        for phrase in BANNED_PHRASES:
            if phrase in lower:
                failures.append(f"{rel_path}: banned unsafe Kling reroll phrase: {phrase!r}")
        for marker in markers:
            if marker not in text:
                failures.append(f"{rel_path}: missing required marker: {marker!r}")

    if failures:
        print("Kling reroll copy validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Kling reroll copy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
