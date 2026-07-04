from pathlib import Path

from config.config import CONTEXT_ROOT

_SCAN_FOLDERS = ["src", "server", "pages", "components", "app", "lib", "api"]

_IGNORE_DIRS = {
    ".git", ".github", ".ai-toolkit", "node_modules",
    "dist", "build", "coverage", "__pycache__", "output",
}

_OUTPUT_PATH = Path(".ai") / "project-map.md"


def _collect_files(folder: Path, root: Path) -> list[Path]:
    """Return all files under folder, skipping ignored directories, sorted."""
    results: list[Path] = []
    for item in sorted(folder.rglob("*")):
        if not item.is_file():
            continue
        if any(part in _IGNORE_DIRS for part in item.parts):
            continue
        results.append(item.relative_to(root))
    return results


class RepositoryAnalyzerService:

    @staticmethod
    def generate_map(root: Path = CONTEXT_ROOT) -> Path:
        sections: list[str] = ["# Project Map\n"]

        for folder_name in _SCAN_FOLDERS:
            folder = root / folder_name
            if not folder.exists() or not folder.is_dir():
                continue

            files = _collect_files(folder, root)
            if not files:
                continue

            lines = [f"## {folder_name}\n"]
            for f in files:
                lines.append(f"- {f.as_posix()}")
            sections.append("\n".join(lines))

        content = "\n\n".join(sections)

        output = root / _OUTPUT_PATH
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")

        return output
