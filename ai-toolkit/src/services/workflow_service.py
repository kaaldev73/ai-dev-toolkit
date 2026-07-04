from pathlib import Path

from config.config import CONTEXT_ROOT
from services.ai_task_service import AITaskService
from services.context_optimizer_service import ContextOptimizerService
from services.project_context_service import ProjectContextService
from services.prompt_builder_service import PromptBuilderService
from services.repository_analyzer_service import RepositoryAnalyzerService
from services.repository_reader_service import RepositoryReaderService


class WorkflowService:

    def __init__(self) -> None:
        self._ai = AITaskService()

    def run_implementation(
        self,
        specification: Path,
        implementation_plan: Path,
        user_prompt: str,
    ) -> str:
        context = ProjectContextService.load()

        map_path = RepositoryAnalyzerService.generate_map()

        selected = ContextOptimizerService.select_files(
            project_map=map_path,
            specification=specification,
            implementation_plan=implementation_plan,
            user_prompt=user_prompt,
        )

        code_context = RepositoryReaderService.read_files(
            [CONTEXT_ROOT / f for f in selected]
        )

        full_prompt = user_prompt
        if code_context:
            full_prompt = f"{user_prompt}\n\n## Relevant Source Code\n\n{code_context}"

        prompt = PromptBuilderService.build(
            project_context=context.get("project_context"),
            project_rules=context.get("project_rules"),
            coding_rules=context.get("coding_rules"),
            specification=specification,
            implementation_plan=implementation_plan,
            user_prompt=full_prompt,
        )
        return self._ai.generate(prompt)
