# Developer / Agent Onboarding Guide

> Hand this file to any developer or AI agent starting work on this repo.
> Read it fully before touching any code.

---

## 1. Read these files first, in this order

| File | What it tells you |
|------|------------------|
| `docs/PLAN.md` | Phased roadmap with checkboxes — shows what is done and what is next |
| `CHANGELOG.md` | What shipped in each release |
| `docs/ROADMAP.md` | Planned future features (not yet scheduled) |
| `CONTRIBUTING.md` | Branch names, commit style, how to run tests and lint |

Do not start writing code until you have read all four.

---

## 2. Understand the current state

- Check `docs/PLAN.md` to see which phase is active and which checkboxes are open.
- Run `git log --oneline -10` to see recent commits.
- Run `git branch -a` to see what branches exist.
- Run `uv run pytest` and `uv run ruff check src/ tests/` — both must be green before you change anything.

---

## 3. Local setup

```bash
uv sync --extra dev          # install all dependencies including dev tools
uv run crawl4ai-setup        # one-time browser install (needed for crawl4ai)
uv run pytest                # should be 36/36 green
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
```

---

## 4. Branch workflow — the rules

### Always start from main

```bash
git checkout main
git pull
git checkout -b feature/your-thing
```

Never branch from another feature branch. Never commit directly to `main`.

### Branch naming

| Prefix | When to use |
|--------|-------------|
| `feature/<name>` | New functionality |
| `fix/<name>` | Bug fixes |
| `docs/<name>` | Documentation only |
| `chore/<name>` | CI, tooling, dependency bumps |

### Never delete branches

After a PR is merged, leave the branch in place. Branches are the historical record of what was built and why. Do not pass `--delete-branch` to `gh pr merge`.

---

## 5. Commit conventions

**One logical change per commit.** Do not batch a week of work into one commit. Each commit should be a self-contained, passing snapshot.

Format: imperative mood, lowercase, present tense.

```
add robots.txt enforcement to crawler
fix URL normalization for trailing slashes
update README with --include/--exclude examples
```

Not `Added...`, `Fixes...`, `WIP`, or `misc changes`.

After every commit, run the full check:

```bash
uv run pytest && uv run ruff check src/ tests/ && uv run ruff format --check src/ tests/
```

If any of those fail, fix them before moving on.

---

## 6. The two ruff commands — both matter

CI runs both of these and will fail if either fails:

```bash
uv run ruff check src/ tests/      # linting (unused imports, style errors, etc.)
uv run ruff format --check src/ tests/  # formatting (spacing, line length, etc.)
```

To auto-fix both before committing:

```bash
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/
```

Running only `ruff check` and not `ruff format` is a common mistake that causes CI to fail after pushing.

---

## 7. What NOT to commit

These are either already in `.gitignore` or should never be staged:

| Path | Why |
|------|-----|
| `.claude/` | AI agent session memory — already in `.gitignore` |
| `output/`, `crawldown-output/` | Crawled site content — already in `.gitignore` |
| `.env` | Secrets — never commit |
| `dist/`, `*.egg-info/` | Build artifacts — already in `.gitignore` |
| `docs/HANDOFF.md` | Temporary handoff notes — delete when done, do not commit |

Before staging, always run `git status` and read the file list carefully.

---

## 8. PR workflow

1. Push your branch: `git push -u origin feature/your-thing`
2. Open a PR: `gh pr create --title "..." --body "..."`
3. Wait for CI to go green (lint + format + tests on Python 3.10/3.11/3.12)
4. Do not merge your own PR without review unless the owner has said it is fine
5. Merge with: `gh pr merge <number> --merge --delete-branch=false`

PR descriptions should explain *why*, not just *what*. The diff shows what changed; the description explains the motivation.

---

## 9. Releasing a new version

Releases are fully automated via `.github/workflows/release.yml`. To ship:

1. Update `version` in `pyproject.toml`
2. Add a new entry to `CHANGELOG.md`
3. Commit, merge to `main`
4. Tag and push:

```bash
git tag v0.x.0
git push origin v0.x.0
```

The workflow builds the package, publishes to TestPyPI first, then to PyPI. Both use OIDC Trusted Publishers (no API token needed).

---

## 10. Working style

- **Commit in milestones, not chunks.** Each phase in `docs/PLAN.md` maps to a branch. Each checkbox in that phase is roughly one commit. Do not finish an entire phase and then make one giant commit.
- **Verify before you move on.** Each commit should leave the repo in a passing state. Do not accumulate broken commits and fix them at the end.
- **Update `docs/PLAN.md`** when you complete a phase — check the boxes and mark the phase done.
- **Update `CHANGELOG.md`** for any user-facing change going into a release.
- **Delete `docs/HANDOFF.md`** at the end of your session if it exists — it is a temporary file, not meant to be committed.
