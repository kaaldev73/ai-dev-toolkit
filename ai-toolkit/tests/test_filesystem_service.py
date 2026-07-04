import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from models.work_item import WorkItem
from services.filesystem_service import FileSystemService


def make_work_item(prefix="BUG", number=1, title="Dashboard crash") -> WorkItem:
    return WorkItem(prefix=prefix, number=number, work_type="bug", title=title)


def _patch_output(tmp: Path):
    return patch("services.filesystem_service.OUTPUT_DIR", tmp)


# ── Folder creation ───────────────────────────────────────────────────────────

def test_creates_folder_under_output_dir():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item()
        with _patch_output(d):
            folder = FileSystemService.create_work_item_folder(item)
        assert folder.exists()
        assert folder.is_dir()


def test_returns_path_to_created_folder():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item()
        with _patch_output(d):
            folder = FileSystemService.create_work_item_folder(item)
        assert isinstance(folder, Path)
        assert folder.parent == d


def test_folder_name_contains_work_item_id():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item(prefix="BUG", number=1, title="Login crash")
        with _patch_output(d):
            folder = FileSystemService.create_work_item_folder(item)
        assert "BUG-001" in folder.name


def test_folder_name_contains_title_words():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item(title="Login crash fix")
        with _patch_output(d):
            folder = FileSystemService.create_work_item_folder(item)
        assert "Login" in folder.name
        assert "crash" in folder.name


def test_folder_name_replaces_spaces_with_dashes():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item(title="Two Words")
        with _patch_output(d):
            folder = FileSystemService.create_work_item_folder(item)
        assert " " not in folder.name


# ── Idempotency ───────────────────────────────────────────────────────────────

def test_calling_twice_does_not_raise():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item()
        with _patch_output(d):
            try:
                FileSystemService.create_work_item_folder(item)
                FileSystemService.create_work_item_folder(item)
            except Exception as e:
                assert False, f"Should not raise: {e}"


def test_calling_twice_returns_same_path():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item()
        with _patch_output(d):
            path1 = FileSystemService.create_work_item_folder(item)
            path2 = FileSystemService.create_work_item_folder(item)
        assert path1 == path2


# ── Different work item types ─────────────────────────────────────────────────

def test_feat_prefix_folder():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = WorkItem(prefix="FEAT", number=3, work_type="feature", title="Dark mode")
        with _patch_output(d):
            folder = FileSystemService.create_work_item_folder(item)
        assert "FEAT-003" in folder.name


def test_ref_prefix_folder():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = WorkItem(prefix="REF", number=10, work_type="refactor", title="Auth cleanup")
        with _patch_output(d):
            folder = FileSystemService.create_work_item_folder(item)
        assert "REF-010" in folder.name


# ── Output dir creation ───────────────────────────────────────────────────────

def test_creates_output_dir_if_not_exists():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "output" / "nested"
        item = make_work_item()
        with _patch_output(d):
            folder = FileSystemService.create_work_item_folder(item)
        assert folder.exists()


if __name__ == "__main__":
    tests = [
        test_creates_folder_under_output_dir,
        test_returns_path_to_created_folder,
        test_folder_name_contains_work_item_id,
        test_folder_name_contains_title_words,
        test_folder_name_replaces_spaces_with_dashes,
        test_calling_twice_does_not_raise,
        test_calling_twice_returns_same_path,
        test_feat_prefix_folder,
        test_ref_prefix_folder,
        test_creates_output_dir_if_not_exists,
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
