from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CrawlConfig:
    url: str
    output_dir: Path = Path("crawldown-output")
    max_depth: int | None = None  # None = unlimited
    delay: float = 0.0
    respect_robots: bool = True
    include: list[str] = field(default_factory=list)  # glob patterns for URL paths to allow
    exclude: list[str] = field(default_factory=list)  # glob patterns for URL paths to block

    def __post_init__(self):
        self.output_dir = Path(self.output_dir)


@dataclass
class PageResult:
    url: str
    markdown: str
    output_path: Path
    depth: int
    links: list[str] = field(default_factory=list)
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.error is None
