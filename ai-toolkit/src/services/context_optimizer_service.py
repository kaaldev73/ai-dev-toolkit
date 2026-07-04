import re
from pathlib import Path

_MAX_FILES = 20

_STOP_WORDS = {
    "the", "and", "for", "with", "this", "that", "from", "have",
    "will", "should", "must", "not", "are", "was", "been", "all",
    "any", "can", "use", "used", "new", "add", "file", "code",
    "into", "data", "each", "its", "our", "per",
}


def _parse_map(project_map: Path) -> list[Path]:
    """Extract file paths from project-map.md lines starting with '- '."""
    if not project_map.exists():
        return []
    paths: list[Path] = []
    for line in project_map.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            paths.append(Path(stripped[2:]))
    return paths


def _tokenize(text: str) -> set[str]:
    """Split text into lowercase keywords, stripping punctuation."""
    raw = re.sub(r"[^a-zA-Z0-9\s]", " ", text).lower().split()
    return {w for w in raw if len(w) >= 3 and w not in _STOP_WORDS}


def _path_tokens(path: Path) -> set[str]:
    """
    Break a file path into searchable tokens including camelCase splits
    and hyphen/underscore splits.
    """
    stem = path.stem.lower()
    # split on non-alpha chars
    by_separator = re.split(r"[^a-z0-9]", stem)
    # split camelCase segments
    camel = re.sub(r"([a-z])([A-Z])", r"\1 \2", path.stem).lower().split()
    parts = [p.lower() for p in path.parts]
    tokens: set[str] = set()
    for t in by_separator + camel + parts:
        if len(t) >= 3:
            tokens.add(t)
    return tokens


def _score(file_path: Path, keywords: set[str]) -> int:
    tokens = _path_tokens(file_path)
    return sum(1 for kw in keywords if any(kw in tok for tok in tokens))


class ContextOptimizerService:

    @staticmethod
    def select_files(
        project_map: Path,
        specification: Path,
        implementation_plan: Path,
        user_prompt: str,
    ) -> list[Path]:
        candidates = _parse_map(project_map)
        if not candidates:
            return []

        keywords: set[str] = set()
        for source in (specification, implementation_plan):
            if source and source.exists():
                keywords |= _tokenize(source.read_text(encoding="utf-8"))
        keywords |= _tokenize(user_prompt)

        scored: list[tuple[int, str, Path]] = []
        seen: set[str] = set()
        for path in candidates:
            key = path.as_posix()
            if key in seen:
                continue
            seen.add(key)
            score = _score(path, keywords)
            if score > 0:
                scored.append((-score, key, path))

        scored.sort(key=lambda t: (t[0], t[1]))
        return [t[2] for t in scored[:_MAX_FILES]]
