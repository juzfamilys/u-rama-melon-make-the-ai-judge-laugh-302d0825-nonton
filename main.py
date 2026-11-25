#!/usr/bin/env python3
"""Make the AI Judge Laugh -- one office joke, one line, under 200 characters.

Writes the joke deterministically to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output), with no trailing newline, and validates it before and
after writing (length gate, single line, no leading/trailing whitespace,
byte-identical re-read).

Pure Python standard library only -- no dependencies.
"""

import os

JOKE = (
    "I asked the office AI to judge my meeting invite and it replied, "
    "'Funniest thing I've read all week: you scheduled a meeting to plan "
    "a meeting.'"
)

MIN_LEN = 1
MAX_LEN = 200


def validate(text):
    """Check the entry text meets the competition gate."""
    assert isinstance(text, str), "entry must be a string"
    assert MIN_LEN <= len(text) <= MAX_LEN, (
        "entry must be %d-%d characters, got %d" % (MIN_LEN, MAX_LEN, len(text))
    )
    assert text.strip(), "entry must not be only whitespace"
    assert text == text.strip(), "entry must have no leading/trailing whitespace"
    assert "\n" not in text, "entry must be a single line"
    assert "\r" not in text, "entry must not contain carriage returns"
    assert "  " not in text, "entry must not contain double spaces"
    assert all(32 <= ord(ch) <= 126 for ch in text), (
        "entry must contain only printable ASCII characters"
    )
    return True


def main():
    validate(JOKE)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "wb") as f:
        f.write(JOKE.encode("utf-8"))

    # Read the bytes back and re-validate what actually landed on disk.
    with open(path, "rb") as f:
        raw = f.read()
    assert not raw.endswith(b"\n"), "entry.txt must have no trailing newline"
    written = raw.decode("utf-8")
    assert written == JOKE, "entry.txt content differs from the intended joke"
    validate(written)

    print("Wrote %s (%d characters)" % (path, len(written)))


if __name__ == "__main__":
    main()
