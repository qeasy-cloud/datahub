from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_SOURCES = [ROOT / "README.md", ROOT / "docs"]
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CODE_FENCE_PATTERN = re.compile(r"```.*?```", re.DOTALL)


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for source in MARKDOWN_SOURCES:
        if source.is_file():
            files.append(source)
        elif source.is_dir():
            files.extend(sorted(source.rglob("*.md")))
    return files


def is_valid_target(base: Path, link: str) -> bool:
    if not link or link.startswith(("http://", "https://", "mailto:", "#")):
        return True

    path = link.split("#", 1)[0].strip()
    if not path:
        return True

    target = (base / path).resolve()
    candidates = [target]
    if target.suffix == "":
        candidates.extend(
            [
                Path(f"{target}.md"),
                target / "README.md",
            ]
        )

    return any(candidate.exists() for candidate in candidates)


def main() -> int:
    broken: list[tuple[Path, str]] = []

    for markdown_file in iter_markdown_files():
        text = markdown_file.read_text(encoding="utf-8")
        text = CODE_FENCE_PATTERN.sub("", text)
        for link in LINK_PATTERN.findall(text):
            if not is_valid_target(markdown_file.parent, link.strip()):
                broken.append((markdown_file.relative_to(ROOT), link.strip()))

    if broken:
        print(f"发现 {len(broken)} 个失效链接：")
        for file_path, link in broken:
            print(f"- {file_path}: {link}")
        return 1

    print("Markdown 链接检查通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
