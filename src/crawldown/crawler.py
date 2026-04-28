import asyncio
import urllib.robotparser
from collections import deque
from pathlib import Path
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler

from crawldown.extractor import extract_links, is_html_url, normalize_url, url_allowed
from crawldown.models import CrawlConfig, PageResult
from crawldown.writer import resolve_output_path, write_page

_MAX_RETRIES = 3


async def _fetch_robots(url: str) -> urllib.robotparser.RobotFileParser:
    parsed = urlparse(url)
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{parsed.scheme}://{parsed.netloc}/robots.txt")
    try:
        await asyncio.to_thread(rp.read)
    except Exception:
        rp.allow_all = True  # treat as "allow all" when robots.txt is unreachable
    return rp


async def _fetch_with_retry(crawler_instance, url: str):
    last_exc: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            return await crawler_instance.arun(url=url)
        except Exception as exc:
            last_exc = exc
            if attempt < _MAX_RETRIES - 1:
                await asyncio.sleep(2**attempt)  # 1 s, 2 s before attempts 2 and 3
    raise last_exc  # type: ignore[misc]


async def _crawl(config: CrawlConfig, on_page=None, on_skip=None) -> list[PageResult]:
    results: list[PageResult] = []
    visited: set[str] = set()
    queue: deque[tuple[str, int]] = deque([(normalize_url(config.url), 0)])

    robots: urllib.robotparser.RobotFileParser | None = None
    if config.respect_robots:
        robots = await _fetch_robots(config.url)

    try:
        async with AsyncWebCrawler() as crawler:
            while queue:
                url, depth = queue.popleft()

                if url in visited:
                    continue
                if config.max_depth is not None and depth > config.max_depth:
                    continue
                if not is_html_url(url):
                    continue
                if not url_allowed(url, config.include, config.exclude):
                    continue
                if robots and not robots.can_fetch("*", url):
                    if on_skip:
                        on_skip(url, "robots")
                    continue

                visited.add(url)

                try:
                    result = await _fetch_with_retry(crawler, url)
                    markdown = result.markdown or ""
                    raw_links = result.links.get("internal", [])
                    hrefs = [lnk.get("href", "") for lnk in raw_links if lnk.get("href")]
                    links = extract_links(url, hrefs)

                    output_path = resolve_output_path(config.root_url, url, config.output_dir)
                    write_page(output_path, url, markdown)

                    page = PageResult(
                        url=url,
                        markdown=markdown,
                        output_path=output_path,
                        depth=depth,
                        links=links,
                    )
                    results.append(page)

                    if on_page:
                        on_page(page)

                    for link in links:
                        if link not in visited:
                            queue.append((link, depth + 1))

                except Exception as exc:
                    page = PageResult(
                        url=url,
                        markdown="",
                        output_path=resolve_output_path(config.url, url, config.output_dir),
                        depth=depth,
                        error=str(exc),
                    )
                    results.append(page)
                    if on_page:
                        on_page(page)

                if config.delay > 0:
                    await asyncio.sleep(config.delay)

    except asyncio.CancelledError:
        pass  # return partial results on Ctrl-C
    except Exception as exc:
        if "Executable doesn't exist" in str(exc):
            raise RuntimeError("Browser not found. Run: crawl4ai-setup") from None
        raise

    return results


async def crawl(
    url_or_config: str | CrawlConfig,
    output_dir: str | Path = "crawldown-output",
    **kwargs,
):
    """Crawl url_or_config and write each page as a Markdown file under output_dir.

    Pass a plain URL string for defaults, or a CrawlConfig for full control.
    Any extra kwargs are forwarded to CrawlConfig when a string URL is given.
    Returns a list of PageResult objects (one per visited URL).
    """
    if isinstance(url_or_config, str):
        config = CrawlConfig(url=url_or_config, output_dir=Path(output_dir), **kwargs)
    else:
        config = url_or_config
    return await _crawl(config)
