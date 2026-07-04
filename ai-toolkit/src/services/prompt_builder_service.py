from pathlib import Path


class PromptBuilderService:

    _SEPARATOR = "\n\n---\n\n"

    @classmethod
    def build(
        cls,
        *,
        project_context: Path | None = None,
        project_rules: Path | None = None,
        coding_rules: Path | None = None,
        specification: Path | None = None,
        implementation_plan: Path | None = None,
        user_prompt: str,
    ) -> str:
        sections = []

        ordered_files = [
            ("Project Context", project_context),
            ("Project Rules", project_rules),
            ("Coding Rules", coding_rules),
            ("Specification", specification),
            ("Implementation Plan", implementation_plan),
        ]

        for label, path in ordered_files:
            if path is None:
                continue
            if not path.exists():
                continue
            content = path.read_text(encoding="utf-8").strip()
            if not content:
                continue
            sections.append(f"## {label}\n\n{content}")

        sections.append(f"## Task\n\n{user_prompt.strip()}")

        return cls._SEPARATOR.join(sections)
