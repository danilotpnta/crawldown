"""Basic example: crawl a documentation site and save it as Markdown files."""

import asyncio

from crawldown import crawl

# Replace this URL with any site you want to crawl.
# crawl() returns a list of PageResult objects — one per visited page.
results = asyncio.run(
    crawl(
        "https://docs.python.org/3/tutorial/",
        output_dir="./output",  # directory created automatically if it doesn't exist
    )
)

print(f"Crawled {len(results)} pages.")
print(f"  OK:   {sum(1 for r in results if r.success)}")
print(f"  Fail: {sum(1 for r in results if not r.success)}")
