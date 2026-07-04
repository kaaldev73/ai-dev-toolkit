from pathlib import Path

from config.config import CONTEXT_ROOT


class ProjectContextService:

    _FILES = {
        "project_context": Path(".ai") / "project-context.md",
        "project_rules":   Path(".ai") / "project-rules.md",
        "coding_rules":    Path(".ai") / "coding-rules.md",
        "workflow":        Path(".ai") / "workflow.md",
        "architecture":    Path("docs") / "ARCHITECTURE.md",
        "backlog":         Path("planning") / "BACKLOG.md",
    }

    @classmethod
    def load(cls) -> dict[str, Path | None]:
        result: dict[str, Path | None] = {}
        for key, relative in cls._FILES.items():
            full = CONTEXT_ROOT / relative
            result[key] = full if full.exists() else None
        return result
