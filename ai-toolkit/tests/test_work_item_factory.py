import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from factories.work_item_factory import WorkItemFactory
from models.work_item import WorkItem


def _create(work_type="bug", title="Test bug", start_number=1):
    with patch("factories.work_item_factory.NumberingService.get_next_number", return_value=start_number):
        return WorkItemFactory.create(work_type=work_type, title=title)


# ── Valid work types ──────────────────────────────────────────────────────────

def test_creates_bug_with_correct_prefix():
    item = _create("bug", "Dashboard crash")
    assert item.prefix == "BUG"


def test_creates_feature_with_correct_prefix():
    item = _create("feature", "Add login")
    assert item.prefix == "FEAT"


def test_creates_refactor_with_correct_prefix():
    item = _create("refactor", "Clean up auth")
    assert item.prefix == "REF"


def test_returns_work_item_instance():
    item = _create("bug", "Test")
    assert isinstance(item, WorkItem)


def test_id_format_is_prefix_dash_padded_number():
    item = _create("bug", "Test", start_number=5)
    assert item.id == "BUG-005"


def test_title_stored_on_work_item():
    item = _create("bug", "My title")
    assert item.title == "My title"


def test_work_type_stored_on_work_item():
    item = _create("feature", "My feature")
    assert item.work_type == "feature"


def test_default_status_is_draft():
    item = _create()
    assert item.status == "Draft"


def test_default_priority_is_medium():
    item = _create()
    assert item.priority == "Medium"


# ── Case insensitive work type ────────────────────────────────────────────────

def test_work_type_is_case_insensitive_upper():
    item = _create("BUG", "Test")
    assert item.prefix == "BUG"


def test_work_type_is_case_insensitive_mixed():
    item = _create("Feature", "Test")
    assert item.prefix == "FEAT"


def test_work_type_strips_whitespace():
    item = _create("  bug  ", "Test")
    assert item.prefix == "BUG"


# ── Invalid work type ─────────────────────────────────────────────────────────

def test_unsupported_work_type_raises_value_error():
    try:
        _create("task", "Test")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "task" in str(e)


def test_empty_work_type_raises_value_error():
    try:
        _create("", "Test")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# ── Title validation ──────────────────────────────────────────────────────────

def test_empty_title_raises_value_error():
    try:
        _create("bug", "")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "empty" in str(e).lower()


def test_whitespace_only_title_raises_value_error():
    try:
        _create("bug", "   ")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "empty" in str(e).lower()


def test_whitespace_only_tab_raises_value_error():
    try:
        _create("bug", "\t\n")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_valid_title_with_leading_spaces_is_accepted():
    item = _create("bug", "  Real title  ")
    assert item.title == "  Real title  "


# ── NumberingService integration ──────────────────────────────────────────────

def test_factory_calls_numbering_service():
    with patch("factories.work_item_factory.NumberingService.get_next_number") as mock_num:
        mock_num.return_value = 7
        item = WorkItemFactory.create("bug", "Test")
    mock_num.assert_called_once_with("BUG")
    assert item.number == 7


if __name__ == "__main__":
    tests = [
        test_creates_bug_with_correct_prefix,
        test_creates_feature_with_correct_prefix,
        test_creates_refactor_with_correct_prefix,
        test_returns_work_item_instance,
        test_id_format_is_prefix_dash_padded_number,
        test_title_stored_on_work_item,
        test_work_type_stored_on_work_item,
        test_default_status_is_draft,
        test_default_priority_is_medium,
        test_work_type_is_case_insensitive_upper,
        test_work_type_is_case_insensitive_mixed,
        test_work_type_strips_whitespace,
        test_unsupported_work_type_raises_value_error,
        test_empty_work_type_raises_value_error,
        test_empty_title_raises_value_error,
        test_whitespace_only_title_raises_value_error,
        test_whitespace_only_tab_raises_value_error,
        test_valid_title_with_leading_spaces_is_accepted,
        test_factory_calls_numbering_service,
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
