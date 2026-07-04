# AI Engineering Toolkit

A lightweight Python CLI that turns engineering work items into AI-assisted implementations. Create structured work items, fill in specifications and implementation plans, then let the toolkit read your codebase and generate implementation responses using an AI provider of your choice.

---

## Features

- **Work item management** — create Bug, Feature, and Refactor work items with sequential IDs (BUG-001, FEAT-002, REF-003)
- **Template engine** — auto-populates specification, investigation, implementation plan, summary, review, and notes files per work item
- **AI provider abstraction** — supports Anthropic Claude and OpenRouter (free models included); swap providers via a single environment variable
- **Context-aware prompts** — automatically scans the host project, selects relevant source files by keyword scoring, and injects them into the AI prompt
- **Project context** — reads `.ai/project-context.md`, `.ai/project-rules.md`, and `.ai/coding-rules.md` from the host project to ground every prompt

---

## Architecture

```
.ai-toolkit/
├── src/
│   ├── cli.py                          Entry point — routes commands
│   ├── config/config.py                Paths and provider defaults
│   ├── models/work_item.py             WorkItem dataclass
│   ├── factories/work_item_factory.py  Creates validated WorkItem objects
│   ├── commands/implement_command.py   `implement` subcommand logic
│   ├── providers/                      AI provider abstraction layer
│   │   ├── base_provider.py            Abstract base class
│   │   ├── claude_provider.py          Anthropic Claude
│   │   ├── openrouter_provider.py      OpenRouter (free models)
│   │   └── provider_factory.py         Registry + factory
│   └── services/
│       ├── ai_task_service.py          Facade over ProviderFactory
│       ├── context_optimizer_service.py  Keyword-scores project files
│       ├── filesystem_service.py       Creates work item folders
│       ├── metadata_service.py         Writes metadata.yaml
│       ├── numbering_service.py        Sequential ID generation
│       ├── project_context_service.py  Loads .ai/ context files
│       ├── prompt_builder_service.py   Assembles the final AI prompt
│       ├── repository_analyzer_service.py  Scans host project → project-map.md
│       ├── repository_reader_service.py    Reads + formats selected files
│       ├── template_service.py         Renders and writes template files
│       ├── work_item_service.py        Orchestrates work item creation
│       └── workflow_service.py         Full implement pipeline
├── tests/                              One test file per service/module
├── src/templates/                      Markdown templates with {{PLACEHOLDERS}}
├── specifications/                     Internal feature specs and roadmap
├── output/                             Generated work item folders (gitignored)
├── requirements.txt
├── pytest.ini
└── .env.example
```

The toolkit lives inside the host project as `.ai-toolkit/`. `CONTEXT_ROOT` is always the parent directory (the actual project being worked on).

---

## Requirements

- Python 3.12+
- An OpenRouter account (free tier is sufficient) **or** an Anthropic API key

---

## Installation

```bash
# From inside the host project root
cd .ai-toolkit

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Configuration

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `AI_PROVIDER` | Yes | `openrouter` or `claude` |
| `OPENROUTER_API_KEY` | When using OpenRouter | API key from openrouter.ai/keys |
| `ANTHROPIC_API_KEY` | When using Claude | API key from console.anthropic.com |

**Example `.env` (OpenRouter):**

```dotenv
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-...
```

**Example `.env` (Claude):**

```dotenv
AI_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-...
```

> **Privacy note:** All prompt content — including code context read from the host project — is sent to the selected AI provider's API. Do not use this tool with source code that must not leave your machine.

---

## Quick Start

```bash
# 1. Create a work item
python src/cli.py

# Follow the prompts:
#   Work Item Type (bug/feature/refactor): bug
#   Title: Login page crashes on empty password

# Output:
#   ID      : BUG-001
#   Folder  : output/BUG-001-Login-page-crashes-on-empty-password

# 2. Fill in the work item
#    Edit output/BUG-001-.../specification.md
#    Edit output/BUG-001-.../implementation-plan.md

# 3. Generate an implementation
python src/cli.py implement BUG-001

# Output:
#   output/BUG-001-.../implementation-response.md
```

---

## CLI Commands

### Create a work item

```bash
python src/cli.py
```

Launches an interactive prompt. Enter the work type (`bug`, `feature`, or `refactor`) and a title. A numbered work item folder is created under `output/` with all template files pre-populated.

**Supported types:**

| Input | Prefix | Example ID |
|---|---|---|
| `bug` | BUG | BUG-001 |
| `feature` | FEAT | FEAT-001 |
| `refactor` | REF | REF-001 |

### Generate an implementation

```bash
python src/cli.py implement <WORK-ITEM-ID> [optional prompt]
```

Reads `specification.md` and `implementation-plan.md` from the work item folder, scans the host project for relevant source files, builds a context-rich prompt, calls the AI provider, and writes the response to `implementation-response.md`.

**Examples:**

```bash
python src/cli.py implement BUG-001
python src/cli.py implement FEAT-003 "Focus only on the frontend changes"
```

---

## Folder Structure (per work item)

```
output/
└── BUG-001-Login-page-crashes-on-empty-password/
    ├── metadata.yaml              Work item metadata
    ├── specification.md           What needs to be built/fixed
    ├── investigation.md           Root cause analysis
    ├── implementation-plan.md     Step-by-step approach
    ├── implementation-summary.md  Post-implementation notes
    ├── review.md                  Code review checklist
    ├── notes.md                   General notes
    └── implementation-response.md AI-generated response (after `implement`)
```

---

## Project Context Files (optional)

Place these files in the host project root to give the AI persistent context about your project:

| File | Purpose |
|---|---|
| `.ai/project-context.md` | Project overview, domain concepts, key decisions |
| `.ai/project-rules.md` | Process rules, team norms, what NOT to do |
| `.ai/coding-rules.md` | Code style, patterns, conventions |

These files are automatically included in every AI prompt when they exist.

---

## Running Tests

```bash
# Run all tests with pytest
python -m pytest

# Run a specific test file
python -m pytest tests/test_providers.py

# Run with verbose output
python -m pytest -v
```

**Test suite summary (Version 1.0):**

| Suite | Tests |
|---|---|
| test_ai_task_service | 11 |
| test_context_optimizer_service | 14 |
| test_filesystem_service | 10 |
| test_implement_command | 14 |
| test_numbering_service | 11 |
| test_project_context_service | 13 |
| test_prompt_builder_service | 12 |
| test_providers | 25 |
| test_repository_analyzer_service | 16 |
| test_repository_reader_service | 19 |
| test_template_service | 10 |
| test_work_item_factory | 19 |
| test_work_item_service | 10 |
| test_workflow_service | 9 |
| **Total** | **193** |

---

## Troubleshooting

**`OPENROUTER_API_KEY is not set`**
Add your key to `.env` and ensure it starts with `sk-or-v1-`.

**`ANTHROPIC_API_KEY is not set`**
Add your Anthropic key to `.env` or set `AI_PROVIDER=openrouter`.

**`No work item folder found for 'BUG-001'`**
Run `python src/cli.py` first to create the work item.

**`specification.md not found`**
The work item folder exists but the file was deleted. Re-create it manually or delete the folder and recreate the work item.

**`OpenRouter API error: Rate limit exceeded`**
You have hit the free-tier rate limit. Wait a few minutes and try again, or switch to a paid model.

**`OpenRouter returned an empty response`**
The selected model may be temporarily unavailable. Try again, or set a different model via `OPENROUTER_MODEL` if configured.

---

## Roadmap

Version 1.0 delivers the core create-and-implement loop. Planned improvements for future versions:

- `list` command — show all work items with status
- `status` command — update work item status from CLI
- Staleness-aware project map caching
- Model selection per invocation (`--model` flag)
- Configurable max token limits

---

## License

MIT

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for any new behaviour
4. Run `python -m pytest` — all tests must pass
5. Open a pull request
