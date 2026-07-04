import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, call

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from models.work_item import WorkItem
from services.work_item_service import WorkItemService


def make_work_item(prefix="BUG", number=1, title="Test bug") -> WorkItem:
    return WorkItem(prefix=prefix, number=number, work_type="bug", title=title)


def _patch_all(tmp: Path):
    """Patch filesystem, metadata, and template services to use tmp dir."""
    mock_fs = patch(
        "services.work_item_service.FileSystemService.create_work_item_folder",
        return_value=tmp,
    )
    mock_meta = patch(
        "services.work_item_service.MetadataService.write",
        return_value=tmp / "metadata.yaml",
    )
    mock_tmpl = patch(
        "services.work_item_service.TemplateService.write_all",
        return_value=[tmp / "specification.md"],
    )
    return mock_fs, mock_meta, mock_tmpl


# ── Return value ──────────────────────────────────────────────────────────────

def test_returns_path_from_filesystem_service():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item()
        fs, meta, tmpl = _patch_all(d)
        with fs, meta, tmpl:
            result = WorkItemService.create(item)
        assert result == d


def test_returns_a_path_object():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item()
        fs, meta, tmpl = _patch_all(d)
        with fs, meta, tmpl:
            result = WorkItemService.create(item)
        assert isinstance(result, Path)


# ── Service orchestration ─────────────────────────────────────────────────────

def test_filesystem_service_called():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item()
        fs, meta, tmpl = _patch_all(d)
        with fs as mock_fs, meta, tmpl:
            WorkItemService.create(item)
        mock_fs.assert_called_once_with(item)


def test_metadata_service_called_with_folder_and_item():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item()
        fs, meta, tmpl = _patch_all(d)
        with fs, meta as mock_meta, tmpl:
            WorkItemService.create(item)
        mock_meta.assert_called_once_with(folder=d, work_item=item)


def test_template_service_called_with_folder_and_item():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item()
        fs, meta, tmpl = _patch_all(d)
        with fs, meta, tmpl as mock_tmpl:
            WorkItemService.create(item)
        mock_tmpl.assert_called_once_with(folder=d, work_item=item)


def test_all_three_services_called_once():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item()
        fs, meta, tmpl = _patch_all(d)
        with fs as mock_fs, meta as mock_meta, tmpl as mock_tmpl:
            WorkItemService.create(item)
        assert mock_fs.call_count == 1
        assert mock_meta.call_count == 1
        assert mock_tmpl.call_count == 1


# ── Call ordering ─────────────────────────────────────────────────────────────

def test_filesystem_called_before_metadata():
    call_order = []
    item = make_work_item()

    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        with patch(
            "services.work_item_service.FileSystemService.create_work_item_folder",
            side_effect=lambda wi: call_order.append("fs") or d,
        ), patch(
            "services.work_item_service.MetadataService.write",
            side_effect=lambda **kw: call_order.append("meta") or d / "metadata.yaml",
        ), patch(
            "services.work_item_service.TemplateService.write_all",
            side_effect=lambda **kw: call_order.append("tmpl") or [],
        ):
            WorkItemService.create(item)

    assert call_order.index("fs") < call_order.index("meta")
    assert call_order.index("meta") < call_order.index("tmpl")


# ── Error propagation ─────────────────────────────────────────────────────────

def test_filesystem_error_propagates():
    item = make_work_item()
    with patch(
        "services.work_item_service.FileSystemService.create_work_item_folder",
        side_effect=OSError("disk full"),
    ):
        try:
            WorkItemService.create(item)
            assert False, "Should have raised OSError"
        except OSError as e:
            assert "disk full" in str(e)


def test_metadata_error_propagates():
    item = make_work_item()
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        with patch(
            "services.work_item_service.FileSystemService.create_work_item_folder",
            return_value=d,
        ), patch(
            "services.work_item_service.MetadataService.write",
            side_effect=IOError("cannot write"),
        ):
            try:
                WorkItemService.create(item)
                assert False, "Should have raised IOError"
            except IOError as e:
                assert "cannot write" in str(e)


# ── Real integration (no mocks) ───────────────────────────────────────────────

def test_real_integration_creates_folder_and_files():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        item = make_work_item()
        with patch("services.filesystem_service.OUTPUT_DIR", d), \
             patch("services.work_item_service.FileSystemService.create_work_item_folder",
                   return_value=d / item.folder_name):
            (d / item.folder_name).mkdir(parents=True, exist_ok=True)
            result = WorkItemService.create(item)
        assert (result / "metadata.yaml").exists()
        assert (result / "specification.md").exists()


if __name__ == "__main__":
    tests = [
        test_returns_path_from_filesystem_service,
        test_returns_a_path_object,
        test_filesystem_service_called,
        test_metadata_service_called_with_folder_and_item,
        test_template_service_called_with_folder_and_item,
        test_all_three_services_called_once,
        test_filesystem_called_before_metadata,
        test_filesystem_error_propagates,
        test_metadata_error_propagates,
        test_real_integration_creates_folder_and_files,
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
