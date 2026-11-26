"""Rebuild claude-directory/skills/ from skills/ for the Claude plugin directory submission.

The submission includes documentation-only skills. Non-text resources are rejected.
Text files are written with LF line endings, because the
directory rejects SKILL.md front matter with Windows line endings.

Run from the repository root:  python tools/sync_claude_directory.py
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "skills"
DST = ROOT / "claude-directory" / "skills"

TEXT = {".md", ".json", ".yaml", ".yml", ".txt"}


def main() -> None:
    if DST.exists():
        shutil.rmtree(DST)
    DST.mkdir(parents=True)
    copied = []
    for skill in sorted(p for p in SRC.iterdir() if p.is_dir()):
        for f in skill.rglob("*"):
            if not f.is_file():
                continue
            if f.suffix.lower() not in TEXT:
                raise SystemExit(f"Not allowed in the directory submission: {f.relative_to(ROOT)}")
            out = DST / f.relative_to(SRC)
            out.parent.mkdir(parents=True, exist_ok=True)
            data = f.read_bytes().replace(b"\r\n", b"\n")
            if data.startswith(b"\xef\xbb\xbf"):
                data = data[3:]
            out.write_bytes(data)
        copied.append(skill.name)
    print(f"{len(copied)} skills -> {DST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
