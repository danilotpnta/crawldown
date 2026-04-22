from importlib.metadata import version

from crawldown.crawler import crawl

__version__ = version("crawldown")
__all__ = ["crawl"]
