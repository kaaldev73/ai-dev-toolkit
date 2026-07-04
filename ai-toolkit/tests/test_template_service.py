import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from models.work_item import WorkItem
from services.template_service import TemplateService


def make_work_item(**overrides) -> WorkItem:
    defaults = dict(
        prefix="BUG",
        number=1,
        work_type="bug",
        title="Dashboard crash on load",
        status="Draft",
        priority="Medium",
        assignee="",
    )
    defaults.update(overrides)
    return WorkItem(**defaults)


# ── _build_context ────────────────────────────────────────────────────────────

def test_build_context_all_keys():
    item = make_work_item()
    ctx = TemplateService._build_context(item)
    assert ctx["{{ID}}"] == "BUG-001"
    assert ctx["{{TITLE}}"] == "Dashboard crash on load"
    assert ctx["{{TYPE}}"] == "bug"
    assert ctx["{{STATUS}}"] == "Draft"
    assert ctx["{{PRIORITY}}"] == "Medium"
    assert "{{CREATED}}" in ctx
    assert "{{UPDATED}}" in ctx
    assert ctx["{{ASSIGNEE}}"] == ""


# ── _render ───────────────────────────────────────────────────────────────────

def test_render_replaces_id():
    item = make_work_item()
    ctx = TemplateService._build_context(item)
    result = TemplateService._render("Issue: {{ID}}", ctx)
    assert result == "Issue: BUG-001"


def test_render_all_known_placeholders():
    template = "{{ID}} {{TITLE}} {{TYPE}} {{STATUS}} {{PRIORITY}} {{CREATED}} {{UPDATED}} {{ASSIGNEE}}"
    item = make_work_item()
    ctx = TemplateService._build_context(item)
    result = TemplateService._render(template, ctx)
    assert "{{" not in result


def test_render_unknown_placeholder_left_untouched():
    item = make_work_item()
    ctx = TemplateService._build_context(item)
    result = TemplateService._render("{{UNKNOWN}}", ctx)
    assert result == "{{UNKNOWN}}"


def test_render_empty_template():
    item = make_work_item()
    ctx = TemplateService._build_context(item)
    assert TemplateService._render("", ctx) == ""


def test_render_repeated_placeholder():
    item = make_work_item()
    ctx = TemplateService._build_context(item)
    result = TemplateService._render("{{TITLE}} and {{TITLE}}", ctx)
    assert result == "Dashboard crash on load and Dashboard crash on load"


# ── write_all ─────────────────────────────────────────────────────────────────

def test_write_all_creates_all_files():
    item = make_work_item()
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        written = TemplateService.write_all(folder, item)
        names = {p.name for p in written}
        assert names == {
            "specification.md",
            "investigation.md",
            "implementation-plan.md",
            "implementation-summary.md",
            "review.md",
            "notes.md",
        }
        for path in written:
            assert path.exists(), f"Missing: {path.name}"


def test_write_all_no_unreplaced_known_placeholders():
    item = make_work_item(assignee="Alice")
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        written = TemplateService.write_all(folder, item)
        for path in written:
            content = path.read_text(encoding="utf-8")
            for ph in ("{{ID}}", "{{TITLE}}", "{{TYPE}}", "{{STATUS}}",
                       "{{PRIORITY}}", "{{CREATED}}", "{{UPDATED}}", "{{ASSIGNEE}}"):
                assert ph not in content, f"{ph} not replaced in {path.name}"


def test_write_all_id_present_in_each_file():
    item = make_work_item()
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        written = TemplateService.write_all(folder, item)
        for path in written:
            content = path.read_text(encoding="utf-8")
            assert "BUG-001" in content, f"ID missing from {path.name}"


def test_write_all_returns_correct_paths():
    item = make_work_item()
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        written = TemplateService.write_all(folder, item)
        for path in written:
            assert path.parent == folder


if __name__ == "__main__":
    tests = [
        test_build_context_all_keys,
        test_render_replaces_id,
        test_render_all_known_placeholders,
        test_render_unknown_placeholder_left_untouched,
        test_render_empty_template,
        test_render_repeated_placeholder,
        test_write_all_creates_all_files,
        test_write_all_no_unreplaced_known_placeholders,
        test_write_all_id_present_in_each_file,
        test_write_all_returns_correct_paths,
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
