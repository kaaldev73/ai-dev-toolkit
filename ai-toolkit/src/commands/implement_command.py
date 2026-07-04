from pathlib import Path

from config.config import OUTPUT_DIR
from services.workflow_service import WorkflowService

_DEFAULT_PROMPT = (
    "Implement the work item as described in the specification "
    "and implementation plan above. Provide complete, working code."
)
_RESPONSE_FILE = "implementation-response.md"


def _locate_folder(work_item_id: str) -> Path:
    prefix = work_item_id.upper() + "-"
    if OUTPUT_DIR.exists():
        for folder in OUTPUT_DIR.iterdir():
            if folder.is_dir() and folder.name.startswith(prefix):
                return folder
    raise FileNotFoundError(
        f"No work item folder found for '{work_item_id}' in {OUTPUT_DIR}"
    )


def run(work_item_id: str, user_prompt: str | None = None) -> Path:
    folder = _locate_folder(work_item_id)

    specification = folder / "specification.md"
    implementation_plan = folder / "implementation-plan.md"

    if not specification.exists():
        raise FileNotFoundError(f"specification.md not found in {folder}")
    if not implementation_plan.exists():
        raise FileNotFoundError(f"implementation-plan.md not found in {folder}")

    prompt = user_prompt or _DEFAULT_PROMPT

    workflow = WorkflowService()
    response = workflow.run_implementation(
        specification=specification,
        implementation_plan=implementation_plan,
        user_prompt=prompt,
    )

    output_path = folder / _RESPONSE_FILE
    output_path.write_text(response, encoding="utf-8")

    return output_path
