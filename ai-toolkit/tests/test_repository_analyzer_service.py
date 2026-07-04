import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from services.repository_analyzer_service import RepositoryAnalyzerService


def write(root: Path, rel: str, content: str = "x") -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


def read_map(root: Path) -> str:
    return (root / ".ai" / "project-map.md").read_text(encoding="utf-8")


# ── project-map.md generated ──────────────────────────────────────────────────

def test_generates_project_map_file():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "src/main.js")
        output = RepositoryAnalyzerService.generate_map(root)
    assert output.name == "project-map.md"
    assert output.parent.name == ".ai"


def test_returns_path_to_generated_file():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        output = RepositoryAnalyzerService.generate_map(root)
    assert isinstance(output, Path)
    assert output == root / ".ai" / "project-map.md"


def test_output_file_exists_after_generation():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "server/api.js")
        RepositoryAnalyzerService.generate_map(root)
        assert (root / ".ai" / "project-map.md").exists()


def test_output_starts_with_project_map_header():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        RepositoryAnalyzerService.generate_map(root)
        content = read_map(root)
    assert content.startswith("# Project Map")


# ── Empty project ─────────────────────────────────────────────────────────────

def test_empty_project_generates_header_only():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        RepositoryAnalyzerService.generate_map(root)
        content = read_map(root)
    assert "# Project Map" in content
    assert "##" not in content


def test_empty_project_no_exception():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        try:
            RepositoryAnalyzerService.generate_map(root)
        except Exception as e:
            assert False, f"Should not raise: {e}"


# ── Nested folders ────────────────────────────────────────────────────────────

def test_nested_files_included():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "src/features/auth/login.js")
        write(root, "src/features/auth/logout.js")
        RepositoryAnalyzerService.generate_map(root)
        content = read_map(root)
    assert "src/features/auth/login.js" in content
    assert "src/features/auth/logout.js" in content


def test_multiple_scan_folders_included():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "src/app.js")
        write(root, "server/index.js")
        write(root, "pages/home.js")
        RepositoryAnalyzerService.generate_map(root)
        content = read_map(root)
    assert "## src" in content
    assert "## server" in content
    assert "## pages" in content


def test_nonexistent_scan_folders_omitted():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "src/app.js")
        RepositoryAnalyzerService.generate_map(root)
        content = read_map(root)
    assert "## components" not in content
    assert "## app" not in content
    assert "## lib" not in content
    assert "## api" not in content


# ── Ignored folders ───────────────────────────────────────────────────────────

def test_node_modules_ignored():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "src/node_modules/lodash/index.js")
        write(root, "src/app.js")
        RepositoryAnalyzerService.generate_map(root)
        content = read_map(root)
    assert "node_modules" not in content
    assert "src/app.js" in content


def test_dot_git_ignored():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "src/.git/config")
        write(root, "src/main.js")
        RepositoryAnalyzerService.generate_map(root)
        content = read_map(root)
    assert ".git" not in content
    assert "src/main.js" in content


def test_pycache_ignored():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "src/__pycache__/module.pyc")
        write(root, "src/module.py")
        RepositoryAnalyzerService.generate_map(root)
        content = read_map(root)
    assert "__pycache__" not in content
    assert "src/module.py" in content


def test_dist_and_build_ignored():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "src/dist/bundle.js")
        write(root, "src/build/output.js")
        write(root, "src/index.js")
        RepositoryAnalyzerService.generate_map(root)
        content = read_map(root)
    assert "dist" not in content
    assert "build" not in content
    assert "src/index.js" in content


# ── Alphabetical output ───────────────────────────────────────────────────────

def test_files_within_section_are_alphabetical():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "src/zebra.js")
        write(root, "src/alpha.js")
        write(root, "src/middle.js")
        RepositoryAnalyzerService.generate_map(root)
        content = read_map(root)
    lines = [l for l in content.splitlines() if l.startswith("- src/")]
    assert lines == sorted(lines)


def test_sections_appear_in_defined_order():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "server/s.js")
        write(root, "src/a.js")
        write(root, "pages/p.js")
        RepositoryAnalyzerService.generate_map(root)
        content = read_map(root)
    src_pos = content.index("## src")
    server_pos = content.index("## server")
    pages_pos = content.index("## pages")
    assert src_pos < server_pos < pages_pos


def test_paths_use_forward_slashes():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "src/deep/nested/file.js")
        RepositoryAnalyzerService.generate_map(root)
        content = read_map(root)
    assert "src/deep/nested/file.js" in content


if __name__ == "__main__":
    tests = [
        test_generates_project_map_file,
        test_returns_path_to_generated_file,
        test_output_file_exists_after_generation,
        test_output_starts_with_project_map_header,
        test_empty_project_generates_header_only,
        test_empty_project_no_exception,
        test_nested_files_included,
        test_multiple_scan_folders_included,
        test_nonexistent_scan_folders_omitted,
        test_node_modules_ignored,
        test_dot_git_ignored,
        test_pycache_ignored,
        test_dist_and_build_ignored,
        test_files_within_section_are_alphabetical,
        test_sections_appear_in_defined_order,
        test_paths_use_forward_slashes,
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
