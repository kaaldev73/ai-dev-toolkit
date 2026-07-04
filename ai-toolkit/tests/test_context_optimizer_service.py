import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from services.context_optimizer_service import ContextOptimizerService


def write(root: Path, rel: str, content: str = "") -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


def make_map(root: Path, file_paths: list[str]) -> Path:
    lines = ["# Project Map\n", "## src\n"]
    for fp in file_paths:
        lines.append(f"- {fp}")
    p = root / ".ai" / "project-map.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(lines), encoding="utf-8")
    return p


# ── Keyword matching ──────────────────────────────────────────────────────────

def test_matches_by_filename_keyword():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        pm = make_map(d, [
            "src/investor.js",
            "src/portfolio.js",
            "src/dashboard.js",
        ])
        result = ContextOptimizerService.select_files(
            project_map=pm,
            specification=Path(tmp) / "missing.md",
            implementation_plan=Path(tmp) / "missing.md",
            user_prompt="Fix the investor page",
        )
    names = [p.name for p in result]
    assert "investor.js" in names
    assert "dashboard.js" not in names


def test_matches_from_specification_text():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        pm = make_map(d, ["src/investor.js", "src/auth.js"])
        spec = write(d, "spec.md", "The investor page shows portfolio data.")
        result = ContextOptimizerService.select_files(
            project_map=pm,
            specification=spec,
            implementation_plan=d / "missing.md",
            user_prompt="fix bug",
        )
    names = [p.name for p in result]
    assert "investor.js" in names


def test_matches_from_implementation_plan_text():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        pm = make_map(d, ["src/banking.js", "src/auth.js"])
        plan = write(d, "plan.md", "Update the banking module to add transfers.")
        result = ContextOptimizerService.select_files(
            project_map=pm,
            specification=d / "missing.md",
            implementation_plan=plan,
            user_prompt="task",
        )
    names = [p.name for p in result]
    assert "banking.js" in names


def test_camelcase_file_matches_lowercase_keyword():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        pm = make_map(d, ["src/InvestorCard.tsx", "src/Dashboard.tsx"])
        result = ContextOptimizerService.select_files(
            project_map=pm,
            specification=d / "missing.md",
            implementation_plan=d / "missing.md",
            user_prompt="Fix investor display",
        )
    names = [p.name for p in result]
    assert "InvestorCard.tsx" in names
    assert "Dashboard.tsx" not in names


def test_hyphenated_filename_matches_keyword():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        pm = make_map(d, ["server/capital-calls.js", "server/investors.js"])
        result = ContextOptimizerService.select_files(
            project_map=pm,
            specification=d / "missing.md",
            implementation_plan=d / "missing.md",
            user_prompt="capital calls are broken",
        )
    names = [p.name for p in result]
    assert "capital-calls.js" in names


def test_no_keyword_match_returns_empty():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        pm = make_map(d, ["src/investor.js", "src/portfolio.js"])
        result = ContextOptimizerService.select_files(
            project_map=pm,
            specification=d / "missing.md",
            implementation_plan=d / "missing.md",
            user_prompt="xyz qrs completely unrelated",
        )
    assert result == []


# ── Duplicate removal ─────────────────────────────────────────────────────────

def test_no_duplicate_paths_returned():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        pm = make_map(d, [
            "src/investor.js",
            "src/investor.js",   # duplicate in map
            "src/investor.js",
        ])
        result = ContextOptimizerService.select_files(
            project_map=pm,
            specification=d / "missing.md",
            implementation_plan=d / "missing.md",
            user_prompt="investor",
        )
    posix = [p.as_posix() for p in result]
    assert len(posix) == len(set(posix))


# ── Deterministic ordering ────────────────────────────────────────────────────

def test_ordering_is_deterministic():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        pm = make_map(d, [
            "src/investor-card.js",
            "src/investor-list.js",
            "src/investor-service.js",
        ])
        result1 = ContextOptimizerService.select_files(
            project_map=pm,
            specification=d / "missing.md",
            implementation_plan=d / "missing.md",
            user_prompt="investor",
        )
        result2 = ContextOptimizerService.select_files(
            project_map=pm,
            specification=d / "missing.md",
            implementation_plan=d / "missing.md",
            user_prompt="investor",
        )
    assert [p.as_posix() for p in result1] == [p.as_posix() for p in result2]


def test_higher_score_ranked_first():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        # investor-service matches both 'investor' AND 'service' keywords
        # investor.js matches only 'investor'
        pm = make_map(d, [
            "src/investor-service.js",  # matches 2 keywords
            "src/investor.js",          # matches 1 keyword
        ])
        result = ContextOptimizerService.select_files(
            project_map=pm,
            specification=d / "missing.md",
            implementation_plan=d / "missing.md",
            user_prompt="investor service update",
        )
    posix = [p.as_posix() for p in result]
    assert posix.index("src/investor-service.js") < posix.index("src/investor.js")


# ── Max file limit ────────────────────────────────────────────────────────────

def test_max_20_files_returned():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        paths = [f"src/investor-{i}.js" for i in range(30)]
        pm = make_map(d, paths)
        result = ContextOptimizerService.select_files(
            project_map=pm,
            specification=d / "missing.md",
            implementation_plan=d / "missing.md",
            user_prompt="investor",
        )
    assert len(result) <= 20


def test_fewer_than_20_matches_returns_all():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        pm = make_map(d, ["src/investor.js", "src/investor-card.js"])
        result = ContextOptimizerService.select_files(
            project_map=pm,
            specification=d / "missing.md",
            implementation_plan=d / "missing.md",
            user_prompt="investor",
        )
    assert len(result) == 2


# ── Missing project map ───────────────────────────────────────────────────────

def test_missing_project_map_returns_empty():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        result = ContextOptimizerService.select_files(
            project_map=d / "nonexistent.md",
            specification=d / "missing.md",
            implementation_plan=d / "missing.md",
            user_prompt="investor",
        )
    assert result == []


def test_missing_project_map_no_exception():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        try:
            ContextOptimizerService.select_files(
                project_map=d / "nonexistent.md",
                specification=d / "missing.md",
                implementation_plan=d / "missing.md",
                user_prompt="anything",
            )
        except Exception as e:
            assert False, f"Should not raise: {e}"


def test_missing_spec_and_plan_still_uses_user_prompt():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        pm = make_map(d, ["src/banking.js", "src/auth.js"])
        result = ContextOptimizerService.select_files(
            project_map=pm,
            specification=d / "missing.md",
            implementation_plan=d / "missing.md",
            user_prompt="banking transfer issue",
        )
    names = [p.name for p in result]
    assert "banking.js" in names


if __name__ == "__main__":
    tests = [
        test_matches_by_filename_keyword,
        test_matches_from_specification_text,
        test_matches_from_implementation_plan_text,
        test_camelcase_file_matches_lowercase_keyword,
        test_hyphenated_filename_matches_keyword,
        test_no_keyword_match_returns_empty,
        test_no_duplicate_paths_returned,
        test_ordering_is_deterministic,
        test_higher_score_ranked_first,
        test_max_20_files_returned,
        test_fewer_than_20_matches_returns_all,
        test_missing_project_map_returns_empty,
        test_missing_project_map_no_exception,
        test_missing_spec_and_plan_still_uses_user_prompt,
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
