"""Example: crawl with depth limit, delay, and a custom output directory."""
import asyncio
from crawldown import crawl
from crawldown.models import CrawlConfig
from pathlib import Path

config = CrawlConfig(
    url="https://docs.python.org/3/tutorial/",
    output_dir=Path("./output"),
    max_depth=2,
    delay=0.5,
    respect_robots=True,
)

asyncio.run(crawl(config))
