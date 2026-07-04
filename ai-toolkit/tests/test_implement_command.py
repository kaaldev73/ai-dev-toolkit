import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import commands.implement_command as cmd


def _make_work_item_folder(root: Path, work_item_id: str = "BUG-001") -> Path:
    """Create a realistic work item folder with spec and plan files."""
    folder = root / f"{work_item_id}-Some-Title"
    folder.mkdir()
    (folder / "specification.md").write_text("# Spec\nDo the thing.", encoding="utf-8")
    (folder / "implementation-plan.md").write_text("# Plan\nStep 1.", encoding="utf-8")
    (folder / "metadata.yaml").write_text("id: BUG-001\n", encoding="utf-8")
    return folder


def _patch_output(tmp: Path):
    return patch("commands.implement_command.OUTPUT_DIR", tmp)


def _patch_workflow(response: str = "AI generated code"):
    mock_wf = MagicMock()
    mock_wf.run_implementation.return_value = response
    return patch("commands.implement_command.WorkflowService", return_value=mock_wf), mock_wf


# ── Work item loading ─────────────────────────────────────────────────────────

def test_locates_correct_work_item_folder():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        folder = _make_work_item_folder(d, "BUG-001")
        _make_work_item_folder(d, "BUG-002")

        wf_patch, mock_wf = _patch_workflow()
        with _patch_output(d), wf_patch:
            cmd.run("BUG-001")

        call_kwargs = mock_wf.run_implementation.call_args[1]
        assert str(folder) in str(call_kwargs["specification"])


def test_work_item_id_is_case_insensitive():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        _make_work_item_folder(d, "BUG-001")
        wf_patch, mock_wf = _patch_workflow()
        with _patch_output(d), wf_patch:
            cmd.run("bug-001")
        mock_wf.run_implementation.assert_called_once()


def test_missing_work_item_raises_file_not_found():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        with _patch_output(d):
            try:
                cmd.run("BUG-999")
                assert False, "Should have raised FileNotFoundError"
            except FileNotFoundError as e:
                assert "BUG-999" in str(e)


def test_missing_specification_raises_file_not_found():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        folder = _make_work_item_folder(d, "BUG-001")
        (folder / "specification.md").unlink()
        with _patch_output(d):
            try:
                cmd.run("BUG-001")
                assert False, "Should have raised FileNotFoundError"
            except FileNotFoundError as e:
                assert "specification.md" in str(e)


def test_missing_plan_raises_file_not_found():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        folder = _make_work_item_folder(d, "BUG-001")
        (folder / "implementation-plan.md").unlink()
        with _patch_output(d):
            try:
                cmd.run("BUG-001")
                assert False, "Should have raised FileNotFoundError"
            except FileNotFoundError as e:
                assert "implementation-plan.md" in str(e)


# ── WorkflowService called ────────────────────────────────────────────────────

def test_workflow_service_called():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        _make_work_item_folder(d, "BUG-001")
        wf_patch, mock_wf = _patch_workflow()
        with _patch_output(d), wf_patch:
            cmd.run("BUG-001")
    mock_wf.run_implementation.assert_called_once()


def test_workflow_receives_spec_and_plan_paths():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        folder = _make_work_item_folder(d, "BUG-001")
        wf_patch, mock_wf = _patch_workflow()
        with _patch_output(d), wf_patch:
            cmd.run("BUG-001")
    kwargs = mock_wf.run_implementation.call_args[1]
    assert kwargs["specification"] == folder / "specification.md"
    assert kwargs["implementation_plan"] == folder / "implementation-plan.md"


def test_workflow_receives_default_prompt_when_none_given():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        _make_work_item_folder(d, "BUG-001")
        wf_patch, mock_wf = _patch_workflow()
        with _patch_output(d), wf_patch:
            cmd.run("BUG-001")
    kwargs = mock_wf.run_implementation.call_args[1]
    assert kwargs["user_prompt"]


def test_workflow_receives_custom_prompt():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        _make_work_item_folder(d, "BUG-001")
        wf_patch, mock_wf = _patch_workflow()
        with _patch_output(d), wf_patch:
            cmd.run("BUG-001", user_prompt="Custom task description")
    kwargs = mock_wf.run_implementation.call_args[1]
    assert kwargs["user_prompt"] == "Custom task description"


# ── Response saved ────────────────────────────────────────────────────────────

def test_response_saved_as_implementation_response_md():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        folder = _make_work_item_folder(d, "BUG-001")
        wf_patch, _ = _patch_workflow("Generated implementation")
        with _patch_output(d), wf_patch:
            output_path = cmd.run("BUG-001")
        assert output_path == folder / "implementation-response.md"
        assert output_path.exists()


def test_response_content_written_correctly():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        folder = _make_work_item_folder(d, "BUG-001")
        wf_patch, _ = _patch_workflow("def solve(): pass")
        with _patch_output(d), wf_patch:
            cmd.run("BUG-001")
        content = (folder / "implementation-response.md").read_text(encoding="utf-8")
        assert content == "def solve(): pass"


def test_returns_path_to_response_file():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        _make_work_item_folder(d, "BUG-001")
        wf_patch, _ = _patch_workflow()
        with _patch_output(d), wf_patch:
            result = cmd.run("BUG-001")
    assert isinstance(result, Path)
    assert result.name == "implementation-response.md"


# ── Error propagation ─────────────────────────────────────────────────────────

def test_workflow_error_propagates():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        _make_work_item_folder(d, "BUG-001")
        mock_wf = MagicMock()
        mock_wf.run_implementation.side_effect = RuntimeError("provider failure")
        with _patch_output(d), patch("commands.implement_command.WorkflowService", return_value=mock_wf):
            try:
                cmd.run("BUG-001")
                assert False, "Should have raised RuntimeError"
            except RuntimeError as e:
                assert "provider failure" in str(e)


def test_no_response_file_written_on_error():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        folder = _make_work_item_folder(d, "BUG-001")
        mock_wf = MagicMock()
        mock_wf.run_implementation.side_effect = RuntimeError("failure")
        with _patch_output(d), patch("commands.implement_command.WorkflowService", return_value=mock_wf):
            try:
                cmd.run("BUG-001")
            except RuntimeError:
                pass
    assert not (folder / "implementation-response.md").exists()


if __name__ == "__main__":
    tests = [
        test_locates_correct_work_item_folder,
        test_work_item_id_is_case_insensitive,
        test_missing_work_item_raises_file_not_found,
        test_missing_specification_raises_file_not_found,
        test_missing_plan_raises_file_not_found,
        test_workflow_service_called,
        test_workflow_receives_spec_and_plan_paths,
        test_workflow_receives_default_prompt_when_none_given,
        test_workflow_receives_custom_prompt,
        test_response_saved_as_implementation_response_md,
        test_response_content_written_correctly,
        test_returns_path_to_response_file,
        test_workflow_error_propagates,
        test_no_response_file_written_on_error,
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
