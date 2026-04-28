# crawldown — Project Plan

> Last updated: 2026-04-28  
> Maintainer: @danilotpnta

---

## What is crawldown?

`crawldown` is a Python tool and library that crawls any website and saves every page as a Markdown file, organized in a directory tree that mirrors the site's URL structure. It is installable via `pip install crawldown` and usable both from the terminal and from Python code.

---

## Guiding principles

1. **One command, one result** — `crawldown https://example.com` should just work.
2. **Mirror the URL** — output paths match the URL path so files are predictable.
3. **Library-first** — the CLI is a thin wrapper over a clean Python API.
4. **Batteries included, not bloated** — sane defaults, explicit overrides.
5. **Respects servers** — `robots.txt` support, configurable rate limiting.

---

## Repository structure

```
crawldown/                   ← repo root
├── src/
│   └── crawldown/
│       ├── __init__.py      ← public API surface
│       ├── cli.py           ← Typer-based CLI entry point
│       ├── crawler.py       ← async crawl engine (crawl4ai wrapper)
│       ├── extractor.py     ← link discovery and URL normalization
│       ├── writer.py        ← markdown file writing + directory creation
│       └── models.py        ← CrawlConfig, PageResult data classes
├── tests/
│   ├── __init__.py
│   ├── test_crawler.py
│   ├── test_extractor.py
│   └── test_writer.py
├── docs/
│   ├── PLAN.md              ← this file
│   └── ROADMAP.md           ← public-facing future features
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── workflows/
│       └── ci.yml
├── pyproject.toml
├── README.md
├── CONTRIBUTING.md
└── LICENSE                  ← MIT
```

---

## Phases

### Phase 0 — Repo bootstrap _(current)_

**Branch:** `main` (direct, one-time setup)

Goals:
- [x] Rename project to `crawldown`
- [x] Set up `src/` layout
- [x] `pyproject.toml` with proper metadata, CLI entry point
- [x] `README.md` with install + quickstart
- [x] `CONTRIBUTING.md` with branch/PR/commit conventions
- [x] `LICENSE` (MIT)
- [x] `.gitignore`
- [x] GitHub Actions CI (lint + tests on every PR)
- [x] Issue templates

**Done when:** repo is clean, CI is green, `pip install -e .` works locally.

---

### Phase 1 — Core library `feature/core-crawler` ✅

**Branch:** `feature/core-crawler` → PR → merge to `main`

Goals:
- [x] `models.py` — `CrawlConfig` (url, output_dir, max_depth, delay, respect_robots) and `PageResult`
- [x] `extractor.py` — extract all same-domain links from a crawled page
- [x] `crawler.py` — async BFS crawl loop using `crawl4ai`, respects `max_depth`
- [x] `writer.py` — maps URL path → filesystem path, writes `.md` files
- [x] `__init__.py` — exports `crawl(url, output_dir, **kwargs)` as the public API
- [x] Tests for extractor and writer (unit, no network) — 12/12 passing

**Done when:** `python -c "from crawldown import crawl; import asyncio; asyncio.run(crawl('https://example.com', './out'))"` produces files.

---

### Phase 2 — CLI `feature/cli` ✅

**Branch:** `feature/cli` → PR → merge to `main`

Goals:
- [x] `cli.py` with Typer — `crawldown <url> [--output DIR] [--depth N] [--delay FLOAT] [--no-robots]`
- [x] Progress display using `rich` (spinner + per-page OK/FAIL lines)
- [x] `--version` flag
- [x] End-to-end test: invoke CLI via `subprocess`, assert files are created

**Done when:** `crawldown https://example.com --output ./out` runs and shows progress.

---

### Phase 3 — Robustness `feature/robustness` ✅

**Branch:** `feature/robustness` → PR → merge to `main`

Goals:
- [x] `robots.txt` parsing and enforcement
- [x] Retry logic for failed pages (3 attempts, exponential backoff)
- [x] `--include` / `--exclude` URL pattern filters
- [x] Skip non-HTML content (PDFs, images, etc.)
- [x] Graceful Ctrl-C: save what was crawled so far

**Done when:** crawling a large real site completes without crashes.

---

### Phase 4 — Docs & polish `feature/docs-polish` ✅

**Branch:** `feature/docs-polish` → PR → merge to `main`

Goals:
- [x] `docs/ROADMAP.md` with three planned future features
- [x] Inline docstrings on all public functions
- [x] `CHANGELOG.md` (keep a changelog format)
- [x] Example scripts in `examples/` reviewed and updated
- [ ] README badges (CI, PyPI version, license)

---

### Phase 5 — PyPI release `feature/release` ✅

**Branch:** `feature/release` → PR → merge to `main`

Goals:
- [x] GitHub Actions release workflow (triggers on `v*` tags)
- [x] `__version__` wired to `pyproject.toml` via `importlib.metadata`
- [ ] Configure Trusted Publisher on TestPyPI and PyPI (one-time manual step)
- [ ] Test on TestPyPI first: `git tag v0.1.0-rc1 && git push --tags`
- [ ] Tag `v0.1.0` and push to trigger automated publish

**Done when:** `pip install crawldown` installs the real package.

---

## Open issues to file after Phase 0

| # | Title | Why |
|---|-------|-----|
| 1 | `[Feature] Add index.json output` | Programmatic access: a JSON manifest listing all crawled URLs, titles, and output paths would let other tools (search indexers, RAG pipelines, site maps) consume crawldown output without parsing markdown files. |
| 2 | `[Feature] Incremental / resume crawl` | Large sites can take minutes. Saving state and resuming where we left off avoids re-crawling pages. |
| 3 | `[Feature] Sitemap.xml support` | Parse `sitemap.xml` as a seed list instead of following links — faster and more complete for sites that have one. |

---

## Branch & PR conventions

- `main` is always releasable — never commit broken code directly.
- Branch names: `feature/<name>`, `fix/<name>`, `docs/<name>`, `chore/<name>`.
- Every change goes through a PR, even if it's just one person.
- Commits: imperative mood, present tense — `add crawler BFS loop`, not `added` or `adding`.
- PRs must: pass CI, have a description that explains *why*, reference an issue if one exists.
- **Never delete merged branches** — they are the historical record.
- Versioning: [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`.

---

## Tech stack

| Concern | Choice | Why |
|---------|--------|-----|
| Web crawling | `crawl4ai` | Handles JS-heavy sites, returns clean markdown |
| CLI | `typer` | Clean, type-annotated CLI with zero boilerplate |
| Progress display | `rich` | Beautiful terminal output |
| Testing | `pytest` + `pytest-asyncio` | Standard, works well with async code |
| Linting | `ruff` | Fast, single tool for lint + format |
| Package build | `hatchling` (via uv) | Modern, PEP 517-compliant |
| CI | GitHub Actions | Free for public repos |
