import fnmatch
from pathlib import PurePosixPath
from urllib.parse import urljoin, urlparse

_NON_HTML_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".ico",
    ".zip",
    ".tar",
    ".gz",
    ".bz2",
    ".7z",
    ".mp4",
    ".mp3",
    ".avi",
    ".mov",
    ".webm",
    ".ogg",
    ".css",
    ".js",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".otf",
}


def is_html_url(url: str) -> bool:
    """Return False if the URL path has a known non-HTML file extension."""
    suffix = PurePosixPath(urlparse(url).path).suffix.lower()
    return suffix not in _NON_HTML_EXTENSIONS


def url_allowed(url: str, include: list[str], exclude: list[str]) -> bool:
    """Return False if url is excluded or not matched by any include pattern."""
    path = urlparse(url).path
    if exclude and any(fnmatch.fnmatch(path, pat) for pat in exclude):
        return False
    if include and not any(fnmatch.fnmatch(path, pat) for pat in include):
        return False
    return True


def normalize_url(url: str) -> str:
    """Strip fragment and trailing slash for consistent deduplication."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    return parsed._replace(fragment="", path=path, query="").geturl()


def same_domain(base_url: str, candidate: str) -> bool:
    """Return True if both URLs share the same netloc."""
    return urlparse(base_url).netloc == urlparse(candidate).netloc


def extract_links(base_url: str, raw_links: list[str]) -> list[str]:
    """Return normalized absolute URLs that stay on the same domain as base_url."""
    seen = set()
    result = []
    for link in raw_links:
        absolute = urljoin(base_url, link)
        normalized = normalize_url(absolute)
        if same_domain(base_url, normalized) and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def url_to_path(base_url: str, page_url: str) -> list[str]:
    """Convert a URL into a list of path parts relative to the base URL."""
    base_path = urlparse(base_url).path.rstrip("/")
    page_path = urlparse(page_url).path.rstrip("/") or "/"

    # Strip the base path prefix so output is relative to the crawl root
    if page_path.startswith(base_path):
        relative = page_path[len(base_path) :].lstrip("/")
    else:
        relative = page_path.lstrip("/")

    parts = [p for p in relative.split("/") if p]
    return parts if parts else ["index"]
