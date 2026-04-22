"""Basic example: crawl a documentation site and save it as Markdown files."""
import asyncio
from crawldown import crawl

# Replace this URL with any site you want to crawl
asyncio.run(crawl("https://docs.python.org/3/tutorial/", output_dir="./output"))
