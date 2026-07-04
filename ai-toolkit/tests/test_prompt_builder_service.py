import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from services.prompt_builder_service import PromptBuilderService


def write(tmp: Path, name: str, content: str) -> Path:
    p = tmp / name
    p.write_text(content, encoding="utf-8")
    return p


# ── All files present ─────────────────────────────────────────────────────────

def test_all_files_included():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        ctx   = write(d, "context.md",    "Context text")
        rules = write(d, "rules.md",      "Rules text")
        code  = write(d, "coding.md",     "Coding rules")
        spec  = write(d, "spec.md",       "Spec text")
        plan  = write(d, "plan.md",       "Plan text")

        result = PromptBuilderService.build(
            project_context=ctx,
            project_rules=rules,
            coding_rules=code,
            specification=spec,
            implementation_plan=plan,
            user_prompt="Do the task",
        )

        assert "Context text"    in result
        assert "Rules text"      in result
        assert "Coding rules"    in result
        assert "Spec text"       in result
        assert "Plan text"       in result
        assert "Do the task"     in result


# ── Missing / None files ──────────────────────────────────────────────────────

def test_none_paths_skipped():
    result = PromptBuilderService.build(
        project_context=None,
        project_rules=None,
        coding_rules=None,
        specification=None,
        implementation_plan=None,
        user_prompt="Only the task",
    )
    assert "Only the task" in result
    assert "Project Context" not in result


def test_nonexistent_path_skipped():
    with tempfile.TemporaryDirectory() as tmp:
        missing = Path(tmp) / "does_not_exist.md"
        result = PromptBuilderService.build(
            project_context=missing,
            user_prompt="task",
        )
    assert "Project Context" not in result
    assert "task" in result


def test_partial_files_only_present_included():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        spec = write(d, "spec.md", "Spec only")
        result = PromptBuilderService.build(
            specification=spec,
            user_prompt="partial",
        )
    assert "Spec only" in result
    assert "Project Context" not in result
    assert "Project Rules" not in result


# ── Ordering ──────────────────────────────────────────────────────────────────

def test_ordering_is_context_rules_coding_spec_plan_task():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        ctx   = write(d, "context.md", "CONTEXT")
        rules = write(d, "rules.md",   "RULES")
        code  = write(d, "coding.md",  "CODING")
        spec  = write(d, "spec.md",    "SPEC")
        plan  = write(d, "plan.md",    "PLAN")

        result = PromptBuilderService.build(
            project_context=ctx,
            project_rules=rules,
            coding_rules=code,
            specification=spec,
            implementation_plan=plan,
            user_prompt="TASK",
        )

        positions = {
            label: result.index(label)
            for label in ("CONTEXT", "RULES", "CODING", "SPEC", "PLAN", "TASK")
        }

        assert positions["CONTEXT"] < positions["RULES"]
        assert positions["RULES"]   < positions["CODING"]
        assert positions["CODING"]  < positions["SPEC"]
        assert positions["SPEC"]    < positions["PLAN"]
        assert positions["PLAN"]    < positions["TASK"]


def test_user_prompt_always_last():
    with tempfile.TemporaryDirectory() as tmp:
        spec = write(Path(tmp), "spec.md", "spec content")
        result = PromptBuilderService.build(
            specification=spec,
            user_prompt="FINAL TASK",
        )
    assert result.rindex("FINAL TASK") > result.index("spec content")


# ── Empty files ───────────────────────────────────────────────────────────────

def test_empty_file_skipped():
    with tempfile.TemporaryDirectory() as tmp:
        empty = write(Path(tmp), "empty.md", "")
        result = PromptBuilderService.build(
            project_context=empty,
            user_prompt="task",
        )
    assert "Project Context" not in result


def test_whitespace_only_file_skipped():
    with tempfile.TemporaryDirectory() as tmp:
        blank = write(Path(tmp), "blank.md", "   \n\n   ")
        result = PromptBuilderService.build(
            project_context=blank,
            user_prompt="task",
        )
    assert "Project Context" not in result


# ── User prompt ───────────────────────────────────────────────────────────────

def test_user_prompt_always_present_even_with_no_files():
    result = PromptBuilderService.build(user_prompt="standalone task")
    assert "standalone task" in result


def test_user_prompt_content_unmodified():
    prompt = "Fix the bug in line 42\n- step one\n- step two"
    result = PromptBuilderService.build(user_prompt=prompt)
    assert "Fix the bug in line 42" in result
    assert "- step one" in result
    assert "- step two" in result


def test_sections_clearly_separated():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        ctx  = write(d, "context.md", "Context")
        spec = write(d, "spec.md",    "Spec")

        result = PromptBuilderService.build(
            project_context=ctx,
            specification=spec,
            user_prompt="Task",
        )

    assert "---" in result


def test_document_contents_not_modified():
    with tempfile.TemporaryDirectory() as tmp:
        original = "# Title\n\nSome **markdown** content."
        p = write(Path(tmp), "spec.md", original)
        result = PromptBuilderService.build(specification=p, user_prompt="x")
    assert "Some **markdown** content." in result


if __name__ == "__main__":
    tests = [
        test_all_files_included,
        test_none_paths_skipped,
        test_nonexistent_path_skipped,
        test_partial_files_only_present_included,
        test_ordering_is_context_rules_coding_spec_plan_task,
        test_user_prompt_always_last,
        test_empty_file_skipped,
        test_whitespace_only_file_skipped,
        test_user_prompt_always_present_even_with_no_files,
        test_user_prompt_content_unmodified,
        test_sections_clearly_separated,
        test_document_contents_not_modified,
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
