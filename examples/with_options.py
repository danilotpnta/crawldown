"""Example: crawl with depth limit, delay, robots enforcement, and URL filters."""

import asyncio
from pathlib import Path

from crawldown import crawl
from crawldown.models import CrawlConfig

config = CrawlConfig(
    url="https://docs.python.org/3/tutorial/",
    output_dir=Path("./output"),
    max_depth=2,          # stop after following 2 levels of links from the start URL
    delay=0.5,            # wait 0.5 s between page fetches to be polite to the server
    respect_robots=True,  # honour robots.txt disallow rules (default: True)
    include=["/3/*"],     # only crawl paths matching this glob (empty = allow all)
    exclude=["/3/c-api/*"],  # skip paths matching this glob (empty = block nothing)
)

# Pass a CrawlConfig directly when you need full control.
results = asyncio.run(crawl(config))

print(f"Crawled {len(results)} pages.")
for r in results:
    status = "OK  " if r.success else "FAIL"
    print(f"  [{status}] {r.url}")
