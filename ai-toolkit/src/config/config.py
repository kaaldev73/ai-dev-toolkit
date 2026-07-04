import os
from pathlib import Path


# ------------------------------------------------------------------
# Project Directories
# ------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

OUTPUT_DIR = PROJECT_ROOT / "output"

TEMPLATES_DIR = PROJECT_ROOT / "src" / "templates"

# Root of the host project that the toolkit operates on.
# The toolkit lives inside <host-project>/.ai-toolkit/, so the host
# project root is one level up.
CONTEXT_ROOT = PROJECT_ROOT.parent

# ------------------------------------------------------------------
# AI Provider
# ------------------------------------------------------------------

DEFAULT_PROVIDER = os.environ.get("AI_PROVIDER", "claude")