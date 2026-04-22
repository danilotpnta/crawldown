from crawldown.extractor import extract_links, normalize_url, url_to_path


def test_normalize_strips_fragment():
    assert normalize_url("https://example.com/page#section") == "https://example.com/page"


def test_normalize_strips_trailing_slash():
    assert normalize_url("https://example.com/page/") == "https://example.com/page"


def test_normalize_root():
    assert normalize_url("https://example.com/") == "https://example.com/"


def test_extract_links_filters_external():
    base = "https://example.com"
    links = ["https://example.com/about", "https://other.com/page", "/contact"]
    result = extract_links(base, links)
    assert "https://example.com/about" in result
    assert "https://example.com/contact" in result
    assert not any("other.com" in link for link in result)


def test_extract_links_deduplicates():
    base = "https://example.com"
    links = ["/about", "/about/", "https://example.com/about"]
    result = extract_links(base, links)
    assert len(result) == 1


def test_url_to_path_simple():
    result = url_to_path("https://example.com", "https://example.com/docs/intro")
    assert result == ["docs", "intro"]


def test_url_to_path_root():
    assert url_to_path("https://example.com", "https://example.com") == ["index"]


def test_url_to_path_with_base_prefix():
    result = url_to_path("https://example.com/help", "https://example.com/help/getting-started")
    assert result == ["getting-started"]
