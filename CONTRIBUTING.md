# Contributing to crawldown

Thank you for taking the time to contribute. This document explains how the project is organized and how to get your changes in.

---

## Table of contents

- [Getting started](#getting-started)
- [Project structure](#project-structure)
- [Branch & PR workflow](#branch--pr-workflow)
- [Commit style](#commit-style)
- [Running tests](#running-tests)
- [Linting](#linting)
- [Reporting bugs](#reporting-bugs)
- [Requesting features](#requesting-features)

---

## Getting started

**Requirements:** Python 3.10+, [uv](https://github.com/astral-sh/uv)

```bash
# 1. Fork the repo on GitHub, then clone your fork
git clone https://github.com/<your-username>/crawldown.git
cd crawldown

# 2. Install all dependencies including dev tools
uv sync --extra dev

# 3. Install crawl4ai browser dependencies (one-time)
uv run crawl4ai-setup

# 4. Verify everything works
uv run pytest
```

---

## Project structure

```
src/crawldown/      ← library source code
tests/              ← pytest test suite
docs/               ← internal docs and planning
examples/           ← runnable example scripts
.github/            ← CI workflows and issue templates
```

See [docs/PLAN.md](docs/PLAN.md) for the phased roadmap and what is currently being worked on.

---

## Branch & PR workflow

| Branch pattern | Purpose |
|----------------|---------|
| `main` | Always releasable. Protected. |
| `feature/<name>` | New functionality |
| `fix/<name>` | Bug fixes |
| `docs/<name>` | Documentation only |
| `chore/<name>` | Tooling, CI, dependency updates |

Steps:
1. Create a branch from `main`: `git checkout -b feature/my-thing`
2. Make your changes in small, focused commits.
3. Push and open a PR against `main`.
4. CI must pass before merging.
5. At least one approval is required for changes to `src/` or `tests/`.
6. **Never delete branches after merging** — they are the historical record.

---

## Commit style

Use the imperative mood, present tense, lowercase:

```
add robots.txt enforcement to crawler
fix URL normalization for relative links
update README with --delay flag docs
```

Not `Added...`, not `Adding...`, not `Fixed the bug with...`.

---

## Running tests

```bash
uv run pytest
```

To run a specific file:

```bash
uv run pytest tests/test_extractor.py
```

Tests that require network access are marked `@pytest.mark.network` and skipped by default in CI. Run them locally with:

```bash
uv run pytest -m network
```

---

## Linting

We use `ruff` for linting and formatting:

```bash
# Check
uv run ruff check src/ tests/

# Auto-fix
uv run ruff check --fix src/ tests/

# Format
uv run ruff format src/ tests/
```

CI will fail if ruff reports any errors.

---

## Reporting bugs

Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) issue template. Include:
- The URL you were crawling (if shareable)
- The exact command or Python code you ran
- The full error output
- Your Python version and OS

---

## Requesting features

Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) issue template. Describe what you want to do and why the current tool doesn't support it. A short example of how you'd expect the API or CLI to look is very helpful.
