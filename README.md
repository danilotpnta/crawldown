# crawldown

[![CI](https://github.com/danilotpnta/crawldown/actions/workflows/ci.yml/badge.svg)](https://github.com/danilotpnta/crawldown/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/crawldown)](https://pypi.org/project/crawldown/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Crawl any website and save every page as organized Markdown files.**

`crawldown` mirrors a website's URL structure into a local directory of `.md` files — perfect for archiving documentation, feeding content into RAG pipelines, or reading offline.

```
crawldown https://docs.example.com --output ./docs-mirror
```

```
docs-mirror/
├── index.md
├── getting-started/
│   ├── index.md
│   └── installation.md
└── api/
    ├── reference.md
    └── authentication.md
```

---

## Installation

```bash
pip install crawldown
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv tool install crawldown
```

**First-time setup** — crawldown uses [crawl4ai](https://github.com/unclecode/crawl4ai) under the hood, which needs a browser installed once to handle JavaScript-rendered pages:

```bash
crawl4ai-setup
```

---

## Quickstart

### CLI

```bash
# Crawl an entire site
crawldown https://docs.example.com --output ./output

# Limit crawl depth
crawldown https://docs.example.com --output ./output --depth 2

# Add a delay between requests (seconds)
crawldown https://docs.example.com --output ./output --delay 0.5

# Only crawl URLs matching a pattern
crawldown https://docs.example.com --output ./output --include '/docs/*'

# Skip URLs matching a pattern
crawldown https://docs.example.com --output ./output --exclude '/api/*'

# Skip robots.txt enforcement
crawldown https://docs.example.com --output ./output --no-robots
```

### Python API

```python
import asyncio
from crawldown import crawl

asyncio.run(crawl("https://docs.example.com", output_dir="./output"))
```

With options:

```python
import asyncio
from crawldown import crawl
from crawldown.models import CrawlConfig

config = CrawlConfig(
    url="https://docs.example.com",
    output_dir="./output",
    max_depth=3,
    delay=0.5,
    respect_robots=True,
    include=["/docs/*"],   # only crawl these paths (glob)
    exclude=["/api/*"],    # skip these paths (glob)
)

asyncio.run(crawl(config))
```

To crawl specific subpages directly, use `max_depth=0`. Output paths are always anchored to the site root, so files land in the right place regardless of where the crawl starts:

```python
config = CrawlConfig(
    url="https://example.com/privacy-policy",
    output_dir="./output",
    max_depth=0,
    # Writes to ./output/privacy-policy/index.md  ✓
)
```

---

## How it works

1. Starts at the given URL and fetches the page using [crawl4ai](https://github.com/unclecode/crawl4ai) (handles JavaScript-rendered pages).
2. Extracts all links that stay within the same domain.
3. Converts each page to Markdown and saves it at a path matching the URL structure.
4. Repeats for every discovered link up to `max_depth` (default: unlimited).

---

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--output`, `-o` | `./crawldown-output` | Directory to save Markdown files |
| `--depth`, `-d` | unlimited | Max link-follow depth |
| `--delay` | `0.0` | Seconds to wait between requests |
| `--include` | — | Only crawl paths matching this glob (repeatable) |
| `--exclude` | — | Skip paths matching this glob (repeatable) |
| `--no-robots` | off | Ignore `robots.txt` |
| `--version` | — | Show version and exit |

---

## Contributing

We welcome contributions of all kinds. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to get started.

---

## License

MIT — see [LICENSE](LICENSE).
