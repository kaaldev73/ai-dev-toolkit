import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from services.repository_reader_service import RepositoryReaderService

_100KB = 100 * 1024
_1MB   = 1024 * 1024


def write(root: Path, rel: str, content: str = "hello") -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


def write_bytes(root: Path, rel: str, data: bytes) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    return p


# ── Multiple files ────────────────────────────────────────────────────────────

def test_multiple_files_all_included():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        a = write(d, "src/a.js", "const a = 1;")
        b = write(d, "src/b.py", "x = 2")
        result = RepositoryReaderService.read_files([a, b])
    assert "src/a.js" in result
    assert "src/b.py" in result
    assert "const a = 1;" in result
    assert "x = 2" in result


def test_file_content_not_modified():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        original = "function foo() {\n  // comment\n  return 42;\n}"
        f = write(d, "src/foo.js", original)
        result = RepositoryReaderService.read_files([f])
    assert original in result


def test_returns_empty_string_for_empty_input():
    result = RepositoryReaderService.read_files([])
    assert result == ""


def test_output_contains_file_header():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        f = write(d, "src/app.js", "const x = 1;")
        result = RepositoryReaderService.read_files([f])
    assert "# File" in result


def test_output_contains_language_fenced_block():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        f = write(d, "src/app.ts", "const x: number = 1;")
        result = RepositoryReaderService.read_files([f])
    assert "```ts" in result


def test_language_inferred_per_extension():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        py  = write(d, "a.py", "pass")
        tsx = write(d, "b.tsx", "<div/>")
        sql = write(d, "c.sql", "SELECT 1")
        result = RepositoryReaderService.read_files([py, tsx, sql])
    assert "```python" in result
    assert "```tsx" in result
    assert "```sql" in result


def test_separator_between_files():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        a = write(d, "a.py", "a")
        b = write(d, "b.py", "b")
        result = RepositoryReaderService.read_files([a, b])
    assert "---" in result


# ── Missing files ─────────────────────────────────────────────────────────────

def test_missing_file_skipped():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        real = write(d, "src/real.js", "real content")
        missing = d / "nonexistent.js"
        result = RepositoryReaderService.read_files([missing, real])
    assert "real content" in result
    assert "nonexistent" not in result


def test_all_missing_returns_empty():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        result = RepositoryReaderService.read_files([
            d / "missing1.js",
            d / "missing2.py",
        ])
    assert result == ""


def test_missing_file_no_exception():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        try:
            RepositoryReaderService.read_files([d / "does_not_exist.ts"])
        except Exception as e:
            assert False, f"Should not raise: {e}"


# ── Unsupported extensions skipped ───────────────────────────────────────────

def test_unsupported_extension_skipped():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        exe = write(d, "run.exe", "data")
        supported = write(d, "app.js", "const x = 1;")
        result = RepositoryReaderService.read_files([exe, supported])
    assert "run.exe" not in result
    assert "app.js" in result


# ── Binary files ignored ──────────────────────────────────────────────────────

def test_binary_file_skipped():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        # .js with null bytes → binary
        binary = write_bytes(d, "src/binary.js", b"PK\x03\x04\x00\x00binary data")
        text   = write(d, "src/real.js", "const ok = true;")
        result = RepositoryReaderService.read_files([binary, text])
    assert "real.js" in result
    assert "const ok = true;" in result


def test_binary_file_no_exception():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        binary = write_bytes(d, "img.js", b"\x00\x01\x02\xff")
        try:
            RepositoryReaderService.read_files([binary])
        except Exception as e:
            assert False, f"Should not raise: {e}"


# ── File size limit ───────────────────────────────────────────────────────────

def test_file_over_100kb_skipped():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        big   = write(d, "big.js", "x" * (_100KB + 1))
        small = write(d, "small.js", "const x = 1;")
        result = RepositoryReaderService.read_files([big, small])
    assert "big.js" not in result
    assert "small.js" in result


def test_file_at_100kb_included():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        exact = write(d, "exact.js", "x" * _100KB)
        result = RepositoryReaderService.read_files([exact])
    assert "exact.js" in result


# ── Total size limit ──────────────────────────────────────────────────────────

def test_total_output_stops_at_1mb():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        # 11 files × 100 KB each = 1.1 MB → last file(s) dropped
        files = []
        for i in range(11):
            f = write(d, f"file{i:02d}.js", "x" * _100KB)
            files.append(f)
        result = RepositoryReaderService.read_files(files)
    assert len(result.encode("utf-8")) <= _1MB + 10_000  # small formatting overhead


def test_total_limit_preserves_earlier_files():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        first  = write(d, "first.js", "const first = 1;")
        filler = [write(d, f"pad{i}.js", "x" * _100KB) for i in range(11)]
        last   = write(d, "last.js",  "const last = 1;")
        result = RepositoryReaderService.read_files([first] + filler + [last])
    assert "const first = 1;" in result


# ── Ordering ──────────────────────────────────────────────────────────────────

def test_output_ordering_matches_input_order():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        z = write(d, "z.py", "z content")
        a = write(d, "a.py", "a content")
        result = RepositoryReaderService.read_files([z, a])
    assert result.index("z content") < result.index("a content")


def test_ordering_is_deterministic():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        files = [write(d, f"f{i}.js", f"content {i}") for i in range(5)]
        r1 = RepositoryReaderService.read_files(files)
        r2 = RepositoryReaderService.read_files(files)
    assert r1 == r2


if __name__ == "__main__":
    tests = [
        test_multiple_files_all_included,
        test_file_content_not_modified,
        test_returns_empty_string_for_empty_input,
        test_output_contains_file_header,
        test_output_contains_language_fenced_block,
        test_language_inferred_per_extension,
        test_separator_between_files,
        test_missing_file_skipped,
        test_all_missing_returns_empty,
        test_missing_file_no_exception,
        test_unsupported_extension_skipped,
        test_binary_file_skipped,
        test_binary_file_no_exception,
        test_file_over_100kb_skipped,
        test_file_at_100kb_included,
        test_total_output_stops_at_1mb,
        test_total_limit_preserves_earlier_files,
        test_output_ordering_matches_input_order,
        test_ordering_is_deterministic,
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
