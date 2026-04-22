"""Example: crawl the Recime help center and save it locally."""
import asyncio
from crawldown import crawl

asyncio.run(crawl("https://www.recime.app/help/en", output_dir="./recime-help-center"))
