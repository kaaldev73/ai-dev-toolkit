from pathlib import Path

from config.config import CONTEXT_ROOT


class ProjectContextService:

    _FILES = {
        "project_context": Path("ai-ProjectSpecs") / "project-context.md",
        "project_rules":   Path("ai-ProjectSpecs") / "project-rules.md",
        "coding_rules":    Path("ai-framework") / "coding-rules.md",
        "workflow":        Path("ai-framework") / "workflow.md",
        "architecture":    Path("ai-framework") / "standards" / "architecture.md",
        "backlog":         Path("planning") / "BACKLOG.md",
    }

    @classmethod
    def load(cls) -> dict[str, Path | None]:
        result: dict[str, Path | None] = {}
        for key, relative in cls._FILES.items():
            full = CONTEXT_ROOT / relative
            result[key] = full if full.exists() else None
        return result
