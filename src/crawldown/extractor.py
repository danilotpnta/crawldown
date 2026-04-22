from urllib.parse import urljoin, urlparse


def normalize_url(url: str) -> str:
    """Strip fragment and trailing slash for consistent deduplication."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    return parsed._replace(fragment="", path=path, query="").geturl()


def same_domain(base_url: str, candidate: str) -> bool:
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
        relative = page_path[len(base_path):].lstrip("/")
    else:
        relative = page_path.lstrip("/")

    parts = [p for p in relative.split("/") if p]
    return parts if parts else ["index"]
