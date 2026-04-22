# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-04-22

### Added

- `crawl(url, output_dir, **kwargs)` public API in `crawldown` package
- `CrawlConfig` dataclass for full control over crawl behaviour (depth, delay, robots, include/exclude patterns)
- `PageResult` dataclass returned per crawled page (url, markdown, output path, depth, error)
- Async BFS crawl engine using [crawl4ai](https://github.com/unclecode/crawl4ai) for JS-heavy sites
- URL-to-filesystem path mapping that mirrors the site structure under the output directory
- CLI entry point (`crawldown <url>`) with `--output`, `--depth`, `--delay`, `--no-robots`, `--include`, `--exclude`, and `--version` flags
- Rich terminal output — spinner and per-page OK/FAIL lines
- `robots.txt` enforcement (fetched async, opt-out via `--no-robots`)
- Retry logic: up to 3 attempts with exponential backoff on transient fetch errors
- URL pattern filtering via `--include` / `--exclude` glob flags
- Non-HTML resource filtering — skips PDFs, images, fonts, archives, CSS, JS before requesting
- Graceful Ctrl-C: saves partial results instead of crashing

[Unreleased]: https://github.com/danilotpnta/crawldown/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/danilotpnta/crawldown/releases/tag/v0.1.0
