import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import services.project_context_service as pcs_module
from services.project_context_service import ProjectContextService


def _patch_root(tmp: Path):
    return patch.object(pcs_module, "CONTEXT_ROOT", tmp)


def _create_files(root: Path, *relative_paths: str) -> dict[str, Path]:
    created = {}
    for rel in relative_paths:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"content of {rel}", encoding="utf-8")
        created[rel] = p
    return created


# ── All files exist ───────────────────────────────────────────────────────────

def test_all_files_present_returns_all_paths():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        _create_files(
            d,
            ".ai/project-context.md",
            ".ai/project-rules.md",
            ".ai/coding-rules.md",
            ".ai/workflow.md",
            "docs/ARCHITECTURE.md",
            "planning/BACKLOG.md",
        )
        with _patch_root(d):
            result = ProjectContextService.load()

    assert result["project_context"] is not None
    assert result["project_rules"] is not None
    assert result["coding_rules"] is not None
    assert result["workflow"] is not None
    assert result["architecture"] is not None
    assert result["backlog"] is not None


def test_all_files_present_returns_correct_paths():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        _create_files(d, ".ai/project-context.md", ".ai/project-rules.md")
        with _patch_root(d):
            result = ProjectContextService.load()

    assert result["project_context"] == d / ".ai" / "project-context.md"
    assert result["project_rules"] == d / ".ai" / "project-rules.md"


def test_result_has_all_keys():
    with tempfile.TemporaryDirectory() as tmp:
        with _patch_root(Path(tmp)):
            result = ProjectContextService.load()

    expected_keys = {"project_context", "project_rules", "coding_rules",
                     "workflow", "architecture", "backlog"}
    assert set(result.keys()) == expected_keys


# ── Some files missing ────────────────────────────────────────────────────────

def test_missing_files_return_none():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        _create_files(d, ".ai/project-context.md")
        with _patch_root(d):
            result = ProjectContextService.load()

    assert result["project_context"] is not None
    assert result["project_rules"] is None
    assert result["coding_rules"] is None
    assert result["workflow"] is None
    assert result["architecture"] is None
    assert result["backlog"] is None


def test_partial_files_correct_nones():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        _create_files(d, "docs/ARCHITECTURE.md", "planning/BACKLOG.md")
        with _patch_root(d):
            result = ProjectContextService.load()

    assert result["architecture"] is not None
    assert result["backlog"] is not None
    assert result["project_context"] is None
    assert result["project_rules"] is None


# ── No files exist ────────────────────────────────────────────────────────────

def test_no_files_all_none():
    with tempfile.TemporaryDirectory() as tmp:
        with _patch_root(Path(tmp)):
            result = ProjectContextService.load()

    assert all(v is None for v in result.values())


def test_no_files_never_raises():
    with tempfile.TemporaryDirectory() as tmp:
        with _patch_root(Path(tmp)):
            try:
                ProjectContextService.load()
            except Exception as e:
                assert False, f"Should not raise: {e}"


def test_nonexistent_root_never_raises():
    with _patch_root(Path("/nonexistent/path/that/does/not/exist")):
        try:
            result = ProjectContextService.load()
            assert all(v is None for v in result.values())
        except Exception as e:
            assert False, f"Should not raise: {e}"


# ── WorkflowService uses ProjectContextService ────────────────────────────────

def test_workflow_calls_project_context_service():
    with patch("services.workflow_service.ProjectContextService.load") as mock_load, \
         patch("services.workflow_service.PromptBuilderService.build", return_value="p"), \
         patch("services.workflow_service.AITaskService") as mock_ai_cls:
        mock_load.return_value = {k: None for k in
            ["project_context","project_rules","coding_rules","workflow","architecture","backlog"]}
        mock_ai_cls.return_value.generate.return_value = "result"

        from services.workflow_service import WorkflowService
        svc = WorkflowService()
        svc.run_implementation(Path("spec.md"), Path("plan.md"), "task")

    mock_load.assert_called_once()


def test_workflow_calls_project_context_exactly_once():
    with patch("services.workflow_service.ProjectContextService.load") as mock_load, \
         patch("services.workflow_service.PromptBuilderService.build", return_value="p"), \
         patch("services.workflow_service.AITaskService") as mock_ai_cls:
        mock_load.return_value = {k: None for k in
            ["project_context","project_rules","coding_rules","workflow","architecture","backlog"]}
        mock_ai_cls.return_value.generate.return_value = "result"

        from services.workflow_service import WorkflowService
        svc = WorkflowService()
        svc.run_implementation(Path("spec.md"), Path("plan.md"), "task")
        svc.run_implementation(Path("spec.md"), Path("plan.md"), "task")

    assert mock_load.call_count == 2


# ── PromptBuilder receives loaded paths ───────────────────────────────────────

def test_prompt_builder_receives_context_paths():
    ctx_path = Path("/fake/project-context.md")
    rules_path = Path("/fake/project-rules.md")
    coding_path = Path("/fake/coding-rules.md")

    context = {
        "project_context": ctx_path,
        "project_rules": rules_path,
        "coding_rules": coding_path,
        "workflow": None,
        "architecture": None,
        "backlog": None,
    }

    with patch("services.workflow_service.ProjectContextService.load", return_value=context), \
         patch("services.workflow_service.PromptBuilderService.build", return_value="p") as mock_build, \
         patch("services.workflow_service.AITaskService") as mock_ai_cls:
        mock_ai_cls.return_value.generate.return_value = "result"

        from services.workflow_service import WorkflowService
        svc = WorkflowService()
        svc.run_implementation(Path("spec.md"), Path("plan.md"), "task")

    kwargs = mock_build.call_args[1]
    assert kwargs["project_context"] == ctx_path
    assert kwargs["project_rules"] == rules_path
    assert kwargs["coding_rules"] == coding_path


def test_prompt_builder_receives_none_when_files_missing():
    context = {k: None for k in
        ["project_context","project_rules","coding_rules","workflow","architecture","backlog"]}

    with patch("services.workflow_service.ProjectContextService.load", return_value=context), \
         patch("services.workflow_service.PromptBuilderService.build", return_value="p") as mock_build, \
         patch("services.workflow_service.AITaskService") as mock_ai_cls:
        mock_ai_cls.return_value.generate.return_value = "result"

        from services.workflow_service import WorkflowService
        svc = WorkflowService()
        svc.run_implementation(Path("spec.md"), Path("plan.md"), "task")

    kwargs = mock_build.call_args[1]
    assert kwargs["project_context"] is None
    assert kwargs["project_rules"] is None
    assert kwargs["coding_rules"] is None


def test_prompt_builder_still_receives_spec_and_plan():
    spec = Path("my_spec.md")
    plan = Path("my_plan.md")
    context = {k: None for k in
        ["project_context","project_rules","coding_rules","workflow","architecture","backlog"]}

    with patch("services.workflow_service.ProjectContextService.load", return_value=context), \
         patch("services.workflow_service.PromptBuilderService.build", return_value="p") as mock_build, \
         patch("services.workflow_service.AITaskService") as mock_ai_cls:
        mock_ai_cls.return_value.generate.return_value = "result"

        from services.workflow_service import WorkflowService
        svc = WorkflowService()
        svc.run_implementation(spec, plan, "do it")

    kwargs = mock_build.call_args[1]
    assert kwargs["specification"] == spec
    assert kwargs["implementation_plan"] == plan
    assert kwargs["user_prompt"] == "do it"


if __name__ == "__main__":
    tests = [
        test_all_files_present_returns_all_paths,
        test_all_files_present_returns_correct_paths,
        test_result_has_all_keys,
        test_missing_files_return_none,
        test_partial_files_correct_nones,
        test_no_files_all_none,
        test_no_files_never_raises,
        test_nonexistent_root_never_raises,
        test_workflow_calls_project_context_service,
        test_workflow_calls_project_context_exactly_once,
        test_prompt_builder_receives_context_paths,
        test_prompt_builder_receives_none_when_files_missing,
        test_prompt_builder_still_receives_spec_and_plan,
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
