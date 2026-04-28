from crawldown.models import CrawlConfig


def test_root_url_defaults_to_netloc_root():
    config = CrawlConfig(url="https://example.com/privacy-policy")
    assert config.root_url == "https://example.com/"


def test_root_url_unchanged_when_url_is_root():
    config = CrawlConfig(url="https://example.com/")
    assert config.root_url == "https://example.com/"


def test_root_url_explicit_override():
    config = CrawlConfig(url="https://example.com/blog", root_url="https://example.com/")
    assert config.root_url == "https://example.com/"


def test_root_url_subpage_no_trailing_slash():
    config = CrawlConfig(url="https://example.com/terms-and-conditions")
    assert config.root_url == "https://example.com/"
