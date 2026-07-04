import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from services.numbering_service import NumberingService


def _patch_output(tmp: Path):
    return patch("services.numbering_service.OUTPUT_DIR", tmp)


# ── No output directory ───────────────────────────────────────────────────────

def test_returns_1_when_output_dir_does_not_exist():
    with _patch_output(Path("/nonexistent/output/dir")):
        result = NumberingService.get_next_number("BUG")
    assert result == 1


# ── Empty output directory ────────────────────────────────────────────────────

def test_returns_1_when_output_dir_is_empty():
    with tempfile.TemporaryDirectory() as tmp:
        with _patch_output(Path(tmp)):
            result = NumberingService.get_next_number("BUG")
    assert result == 1


# ── Sequential numbering ──────────────────────────────────────────────────────

def test_returns_next_number_after_existing():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "BUG-001-Some-Title").mkdir()
        with _patch_output(d):
            result = NumberingService.get_next_number("BUG")
    assert result == 2


def test_returns_highest_plus_one():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "BUG-001-Alpha").mkdir()
        (d / "BUG-003-Gamma").mkdir()
        (d / "BUG-002-Beta").mkdir()
        with _patch_output(d):
            result = NumberingService.get_next_number("BUG")
    assert result == 4


def test_returns_correct_number_with_large_existing():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "BUG-042-Big-Number").mkdir()
        with _patch_output(d):
            result = NumberingService.get_next_number("BUG")
    assert result == 43


# ── Prefix isolation ──────────────────────────────────────────────────────────

def test_prefix_isolated_from_other_prefixes():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "FEAT-005-Some-Feature").mkdir()
        (d / "REF-010-Some-Refactor").mkdir()
        with _patch_output(d):
            result = NumberingService.get_next_number("BUG")
    assert result == 1


def test_feat_prefix_independent_of_bug():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "BUG-001-A").mkdir()
        (d / "BUG-002-B").mkdir()
        (d / "FEAT-001-C").mkdir()
        with _patch_output(d):
            bug_next = NumberingService.get_next_number("BUG")
            feat_next = NumberingService.get_next_number("FEAT")
    assert bug_next == 3
    assert feat_next == 2


# ── Robustness ────────────────────────────────────────────────────────────────

def test_ignores_non_directory_files():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "BUG-001-Dir").mkdir()
        (d / "BUG-002-not-a-dir.txt").write_text("file", encoding="utf-8")
        with _patch_output(d):
            result = NumberingService.get_next_number("BUG")
    assert result == 2


def test_ignores_folder_with_non_numeric_number():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "BUG-abc-Bad-Folder").mkdir()
        (d / "BUG-001-Good").mkdir()
        with _patch_output(d):
            result = NumberingService.get_next_number("BUG")
    assert result == 2


def test_ignores_folder_with_no_dash():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "BUGNODASH").mkdir()
        with _patch_output(d):
            result = NumberingService.get_next_number("BUG")
    assert result == 1


def test_no_exception_on_malformed_folders():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "BUG-").mkdir()
        (d / "BUG-001-valid").mkdir()
        with _patch_output(d):
            try:
                result = NumberingService.get_next_number("BUG")
                assert result == 2
            except Exception as e:
                assert False, f"Should not raise: {e}"


if __name__ == "__main__":
    tests = [
        test_returns_1_when_output_dir_does_not_exist,
        test_returns_1_when_output_dir_is_empty,
        test_returns_next_number_after_existing,
        test_returns_highest_plus_one,
        test_returns_correct_number_with_large_existing,
        test_prefix_isolated_from_other_prefixes,
        test_feat_prefix_independent_of_bug,
        test_ignores_non_directory_files,
        test_ignores_folder_with_non_numeric_number,
        test_ignores_folder_with_no_dash,
        test_no_exception_on_malformed_folders,
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
