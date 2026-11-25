"""Unsent: The Micro-Confession Sprint — make.fun entry.

Writes one two-part micro-confession (a "To:" line plus the unsent
message itself, one line, exactly as typed) to entry.txt.

Standard library only. The output path resolves as: ENTRY_OUTPUT, else
OUTPUT_DIR / MAKEFUN_OUTPUT_DIR, else /output/entry.txt when that
directory exists, else beside this script.
"""

import os

ENTRY = (
    "To: my sister\n"
    "I kept the voicemail where you cried about Dad because it's the "
    "only time you've ever sounded like a kid again."
)


def resolve_output_path():
    path = os.environ.get("ENTRY_OUTPUT")
    if path:
        return path
    for key in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        directory = os.environ.get(key)
        if directory:
            return os.path.join(directory, "entry.txt")
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.txt")


def validate_entry(text):
    """Enforce the competition gate before anything is written."""
    if not text or not text.strip():
        raise SystemExit("entry is empty or only whitespace")
    if len(text) > 260:
        raise SystemExit("entry exceeds the 260 character gate")
    lines = text.split("\n")
    if len(lines) != 2 or not lines[0].startswith("To: "):
        raise SystemExit("entry must be a To: line plus one message line")
    if len(lines[1]) > 200:
        raise SystemExit("message line exceeds 200 characters")


def main():
    validate_entry(ENTRY)
    path = resolve_output_path()
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
