from pathlib import Path

_MAX_FILE_BYTES = 100 * 1024       # 100 KB
_MAX_TOTAL_BYTES = 1024 * 1024     # 1 MB

_LANG_MAP: dict[str, str] = {
    ".py":   "python",
    ".ts":   "ts",
    ".tsx":  "tsx",
    ".js":   "js",
    ".jsx":  "jsx",
    ".json": "json",
    ".md":   "md",
    ".yaml": "yaml",
    ".yml":  "yaml",
    ".html": "html",
    ".css":  "css",
    ".scss": "scss",
    ".sql":  "sql",
}

_SEPARATOR = "-" * 48


def _is_binary(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:512]
        return b"\x00" in chunk
    except OSError:
        return True


def _lang(path: Path) -> str:
    return _LANG_MAP.get(path.suffix.lower(), "")


def _format_file(path: Path, content: str) -> str:
    lang = _lang(path)
    return (
        f"{_SEPARATOR}\n\n"
        f"# File\n\n"
        f"{path.as_posix()}\n\n"
        f"```{lang}\n"
        f"{content}\n"
        f"```"
    )


class RepositoryReaderService:

    @staticmethod
    def read_files(files: list[Path]) -> str:
        sections: list[str] = []
        total_bytes = 0

        for path in files:
            if not path.exists() or not path.is_file():
                continue
            if path.suffix.lower() not in _LANG_MAP:
                continue
            if _is_binary(path):
                continue

            file_size = path.stat().st_size
            if file_size > _MAX_FILE_BYTES:
                continue

            if total_bytes + file_size > _MAX_TOTAL_BYTES:
                break

            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            sections.append(_format_file(path, content))
            total_bytes += file_size

        return "\n\n".join(sections)
