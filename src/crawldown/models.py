from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse


@dataclass
class CrawlConfig:
    """Configuration for a single crawl run."""

    url: str
    output_dir: Path = Path("crawldown-output")
    root_url: str | None = None  # path anchor for output files; defaults to scheme://netloc/
    max_depth: int | None = None  # None = unlimited
    delay: float = 0.0  # seconds to wait between page fetches
    respect_robots: bool = True  # honour robots.txt disallow rules
    include: list[str] = field(default_factory=list)  # glob patterns for URL paths to allow
    exclude: list[str] = field(default_factory=list)  # glob patterns for URL paths to block

    def __post_init__(self):
        self.output_dir = Path(self.output_dir)
        if self.root_url is None:
            parsed = urlparse(self.url)
            self.root_url = f"{parsed.scheme}://{parsed.netloc}/"


@dataclass
class PageResult:
    """Result of crawling a single page."""

    url: str
    markdown: str
    output_path: Path
    depth: int
    links: list[str] = field(default_factory=list)
    error: str | None = None

    @property
    def success(self) -> bool:
        """Return True when the page was fetched and written without error."""
        return self.error is None
