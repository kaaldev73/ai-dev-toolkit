import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from services.workflow_service import WorkflowService

SPEC = Path("spec.md")
PLAN = Path("plan.md")
PROMPT = "implement this"


_EMPTY_CONTEXT: dict = {
    k: None for k in
    ["project_context", "project_rules", "coding_rules", "workflow", "architecture", "backlog"]
}


def _make_service(ai_response: str = "AI result") -> tuple[WorkflowService, MagicMock]:
    """Return a WorkflowService with mocked AITaskService and ProjectContextService."""
    mock_ai = MagicMock()
    mock_ai.generate.return_value = ai_response
    with patch("services.workflow_service.AITaskService", return_value=mock_ai), \
         patch("services.workflow_service.ProjectContextService.load", return_value=_EMPTY_CONTEXT):
        svc = WorkflowService()
    svc._ai = mock_ai
    return svc, mock_ai


# ── PromptBuilderService called ───────────────────────────────────────────────

def test_prompt_builder_called_with_correct_args():
    svc, _ = _make_service()
    with patch("services.workflow_service.ProjectContextService.load", return_value=_EMPTY_CONTEXT), \
         patch("services.workflow_service.PromptBuilderService.build", return_value="built prompt") as mock_build:
        svc.run_implementation(SPEC, PLAN, PROMPT)
    kwargs = mock_build.call_args[1]
    assert kwargs["specification"] == SPEC
    assert kwargs["implementation_plan"] == PLAN
    assert kwargs["user_prompt"] == PROMPT


def _ctx_patch():
    return patch("services.workflow_service.ProjectContextService.load", return_value=_EMPTY_CONTEXT)


def test_prompt_builder_output_passed_to_ai():
    svc, mock_ai = _make_service()
    with _ctx_patch(), patch("services.workflow_service.PromptBuilderService.build", return_value="assembled prompt"):
        svc.run_implementation(SPEC, PLAN, PROMPT)
    mock_ai.generate.assert_called_once_with("assembled prompt")


# ── AITaskService called ──────────────────────────────────────────────────────

def test_ai_task_service_called():
    svc, mock_ai = _make_service()
    with _ctx_patch(), patch("services.workflow_service.PromptBuilderService.build", return_value="p"):
        svc.run_implementation(SPEC, PLAN, PROMPT)
    mock_ai.generate.assert_called_once()


def test_ai_task_service_called_exactly_once():
    svc, mock_ai = _make_service()
    with _ctx_patch(), patch("services.workflow_service.PromptBuilderService.build", return_value="p"):
        svc.run_implementation(SPEC, PLAN, PROMPT)
    assert mock_ai.generate.call_count == 1


# ── Return value ──────────────────────────────────────────────────────────────

def test_returns_ai_response():
    svc, _ = _make_service(ai_response="Generated code here")
    with _ctx_patch(), patch("services.workflow_service.PromptBuilderService.build", return_value="p"):
        result = svc.run_implementation(SPEC, PLAN, PROMPT)
    assert result == "Generated code here"


def test_returns_ai_response_unmodified():
    raw = "line1\nline2\n```python\nprint('hi')\n```"
    svc, _ = _make_service(ai_response=raw)
    with _ctx_patch(), patch("services.workflow_service.PromptBuilderService.build", return_value="p"):
        result = svc.run_implementation(SPEC, PLAN, PROMPT)
    assert result == raw


# ── Exception propagation ─────────────────────────────────────────────────────

def test_ai_exception_propagates():
    svc, mock_ai = _make_service()
    mock_ai.generate.side_effect = RuntimeError("provider error")
    with _ctx_patch(), patch("services.workflow_service.PromptBuilderService.build", return_value="p"):
        try:
            svc.run_implementation(SPEC, PLAN, PROMPT)
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "provider error" in str(e)


def test_prompt_builder_exception_propagates():
    svc, _ = _make_service()
    with _ctx_patch(), patch(
        "services.workflow_service.PromptBuilderService.build",
        side_effect=IOError("cannot read file"),
    ):
        try:
            svc.run_implementation(SPEC, PLAN, PROMPT)
            assert False, "Should have raised IOError"
        except IOError as e:
            assert "cannot read file" in str(e)


def test_no_provider_imports_in_workflow():
    """WorkflowService must not import Claude or OpenRouter directly."""
    import services.workflow_service as wf_module
    source = Path(wf_module.__file__).read_text()
    assert "claude" not in source.lower().replace("# claude", "")
    assert "openrouter" not in source.lower()
    assert "anthropic" not in source.lower()


if __name__ == "__main__":
    tests = [
        test_prompt_builder_called_with_correct_args,
        test_prompt_builder_output_passed_to_ai,
        test_ai_task_service_called,
        test_ai_task_service_called_exactly_once,
        test_returns_ai_response,
        test_returns_ai_response_unmodified,
        test_ai_exception_propagates,
        test_prompt_builder_exception_propagates,
        test_no_provider_imports_in_workflow,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
