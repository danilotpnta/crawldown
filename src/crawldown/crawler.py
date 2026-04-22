import asyncio
from collections import deque
from pathlib import Path

from crawl4ai import AsyncWebCrawler

from crawldown.extractor import extract_links, normalize_url
from crawldown.models import CrawlConfig, PageResult
from crawldown.writer import resolve_output_path, write_page


async def _crawl(config: CrawlConfig, on_page=None) -> list[PageResult]:
    results = []
    visited = set()
    queue = deque([(normalize_url(config.url), 0)])

    async with AsyncWebCrawler() as crawler:
        while queue:
            url, depth = queue.popleft()
            if url in visited:
                continue
            if config.max_depth is not None and depth > config.max_depth:
                continue

            visited.add(url)

            try:
                result = await crawler.arun(url=url)
                markdown = result.markdown or ""
                raw_links = result.links.get("internal", [])
                hrefs = [lnk.get("href", "") for lnk in raw_links if lnk.get("href")]
                links = extract_links(config.url, hrefs)

                output_path = resolve_output_path(config.url, url, config.output_dir)
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

    return results


async def crawl(
    url_or_config: str | CrawlConfig,
    output_dir: str | Path = "crawldown-output",
    **kwargs,
):
    """Public API entry point. Accepts a URL string or a CrawlConfig."""
    if isinstance(url_or_config, str):
        config = CrawlConfig(url=url_or_config, output_dir=Path(output_dir), **kwargs)
    else:
        config = url_or_config
    return await _crawl(config)
