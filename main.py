#!/usr/bin/env python3
"""main.py — one office-life one-liner, for make.fun's
"Make the AI Judge Laugh: Office Jokes".

Writes one line (<=199 chars) to /output/entry.txt. The judge is a comedy club
booker picking the joke that makes a room of tired office workers laugh
hardest: funny first, then recognition (the meeting, the printer, the
reply-all, the calendar) so the laugh comes with a wince.
"""

from __future__ import annotations

import os
import sys

MAX_LEN = 199
OUTPUT_PATH = "/output/entry.txt"
FALLBACK_PATH = "output/entry.txt"

CANDIDATES: list[str] = [
    "My calendar is just back-to-back meetings titled 'quick sync' that could've been a message, from a man who could've been a message.",

    "I reply-all by accident once and now the whole company knows I also don't know what 'per my last email' means.",

    "The printer jams every Monday because it, too, does not want to be here.",

    "We have a meeting to decide why we have so many meetings. It's standing-room only and nobody is standing.",

    "HR said to bring my whole self to work. I did, and now they want me to leave the part that needs a nap.",

    "Corporate called it a 'flat structure.' There are still eleven managers between me and a stapler.",

    "I put 'team player' on my resume, which is how I ended up on a 9 AM call that an email already answered.",

    "Out of office is the only meeting that ever gets declined on my behalf.",

    "The printer asked for my password, then judged it. Just like performance review season.",

    "I work best under pressure, which is why management keeps applying more.",
]

COMEDY: dict[str, int] = {
    "could've been a message": 5,   # universal wince, clean build
    "reply-all by accident": 4,
    "printer jams every Monday": 4,
    "meeting to decide why we have so many meetings": 5,
    "bring my whole self to work": 4,
    "eleven managers between me and a stapler": 4,
    "an email already answered": 4,
    "Out of office is the only meeting": 4,
    "printer asked for my password": 3,
    "work best under pressure": 3,
}

OFFICE_WORDS = ("meeting", "printer", "reply-all", "calendar", "email",
                "HR", "manager", "corporate", "sync", "review", "team")


def label(text: str) -> str:
    body = text.lower()
    for key in COMEDY:
        if key.lower() in body:
            return key
    return ""


def is_valid(text: str) -> bool:
    body = text.strip()
    return 1 <= len(body) <= MAX_LEN and "\n" not in body


def score(text: str) -> tuple[int, ...]:
    body = text.strip()
    low = body.lower()
    rec = sum(1 for w in OFFICE_WORDS if w in low)
    return (COMEDY.get(label(text), 0), is_valid(text), rec, MAX_LEN - len(body))


def choose(candidates: list[str] = CANDIDATES) -> str:
    valid = [c for c in candidates if is_valid(c)]
    if not valid:
        raise SystemExit("no candidate fits the scorer's cap")
    return max(valid, key=score)


def write_entry(text: str) -> str:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    try:
        target = OUTPUT_PATH
        with open(target, "w", encoding="utf-8") as h:
            h.write(text + "\n")
    except PermissionError:
        target = FALLBACK_PATH
        os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
        with open(target, "w", encoding="utf-8") as h:
            h.write(text + "\n")
    return target


def main() -> int:
    text = choose()
    assert is_valid(text), f"entry is {len(text)} chars, cap {MAX_LEN}"
    where = write_entry(text)
    print(text)
    print(f"[{len(text)} chars] written to {where}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())