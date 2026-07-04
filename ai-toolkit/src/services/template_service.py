from pathlib import Path

from config.config import TEMPLATES_DIR
from models.work_item import WorkItem


class TemplateService:

    TEMPLATES = [
        "specification.md",
        "investigation.md",
        "implementation-plan.md",
        "implementation-summary.md",
        "review.md",
        "notes.md",
    ]

    @staticmethod
    def _build_context(work_item: WorkItem) -> dict:
        return {
            "{{ID}}": work_item.id,
            "{{TITLE}}": work_item.title,
            "{{TYPE}}": work_item.work_type,
            "{{STATUS}}": work_item.status,
            "{{PRIORITY}}": work_item.priority,
            "{{CREATED}}": work_item.created,
            "{{UPDATED}}": work_item.updated,
            "{{ASSIGNEE}}": work_item.assignee,
        }

    @staticmethod
    def _render(raw: str, context: dict) -> str:
        result = raw
        for placeholder, value in context.items():
            result = result.replace(placeholder, value)
        return result

    @classmethod
    def write_all(cls, folder: Path, work_item: WorkItem) -> list[Path]:
        context = cls._build_context(work_item)
        written = []
        for template_name in cls.TEMPLATES:
            template_path = TEMPLATES_DIR / template_name
            raw = template_path.read_text(encoding="utf-8")
            rendered = cls._render(raw, context)
            output_path = folder / template_name
            output_path.write_text(rendered, encoding="utf-8")
            written.append(output_path)
        return written
