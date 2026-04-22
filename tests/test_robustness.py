from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from crawldown.crawler import _fetch_with_retry
from crawldown.extractor import is_html_url, url_allowed

# ---------------------------------------------------------------------------
# is_html_url
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://example.com/page", True),
        ("https://example.com/docs/intro", True),
        ("https://example.com/file.pdf", False),
        ("https://example.com/image.png", False),
        ("https://example.com/style.css", False),
        ("https://example.com/app.js", False),
        ("https://example.com/archive.zip", False),
        ("https://example.com/font.woff2", False),
        ("https://example.com/video.mp4", False),
    ],
)
def test_is_html_url(url, expected):
    assert is_html_url(url) is expected


# ---------------------------------------------------------------------------
# url_allowed (include / exclude patterns)
# ---------------------------------------------------------------------------


def test_url_allowed_no_filters():
    assert url_allowed("https://example.com/anything", [], []) is True


def test_url_allowed_exclude_matches():
    assert url_allowed("https://example.com/api/v1", [], ["/api/*"]) is False


def test_url_allowed_exclude_no_match():
    assert url_allowed("https://example.com/docs/intro", [], ["/api/*"]) is True


def test_url_allowed_include_matches():
    assert url_allowed("https://example.com/docs/intro", ["/docs/*"], []) is True


def test_url_allowed_include_no_match():
    assert url_allowed("https://example.com/blog/post", ["/docs/*"], []) is False


def test_url_allowed_exclude_takes_priority_over_include():
    # URL matches include but also matches exclude — exclude wins
    assert url_allowed("https://example.com/docs/private", ["/docs/*"], ["/docs/private*"]) is False


# ---------------------------------------------------------------------------
# _fetch_with_retry
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_fetch_with_retry_succeeds_first_try():
    fake = MagicMock()
    mock_crawler = AsyncMock()
    mock_crawler.arun.return_value = fake

    result = await _fetch_with_retry(mock_crawler, "https://example.com")

    assert result is fake
    assert mock_crawler.arun.call_count == 1


@pytest.mark.asyncio
async def test_fetch_with_retry_succeeds_on_third_attempt():
    fake = MagicMock()
    call_count = 0

    async def flaky_arun(url):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("temporary failure")
        return fake

    mock_crawler = MagicMock()
    mock_crawler.arun = flaky_arun

    with patch("crawldown.crawler.asyncio.sleep", new_callable=AsyncMock):
        result = await _fetch_with_retry(mock_crawler, "https://example.com")

    assert result is fake
    assert call_count == 3


@pytest.mark.asyncio
async def test_fetch_with_retry_raises_after_max_attempts():
    async def always_fail(url):
        raise ConnectionError("always fails")

    mock_crawler = MagicMock()
    mock_crawler.arun = always_fail

    with patch("crawldown.crawler.asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(ConnectionError):
            await _fetch_with_retry(mock_crawler, "https://example.com")


# ---------------------------------------------------------------------------
# robots.txt enforcement (via _crawl integration)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_crawl_skips_robots_disallowed_url(tmp_path):
    import urllib.robotparser

    from crawldown.crawler import _crawl
    from crawldown.models import CrawlConfig

    # robots.txt that disallows /private/
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(["User-agent: *", "Disallow: /private/"])

    fake_result = MagicMock()
    fake_result.markdown = "# Page"
    fake_result.links = {"internal": [{"href": "/private/secret"}]}

    mock_instance = AsyncMock()
    mock_instance.arun.return_value = fake_result
    ctx = AsyncMock()
    ctx.__aenter__ = AsyncMock(return_value=mock_instance)
    ctx.__aexit__ = AsyncMock(return_value=None)

    config = CrawlConfig(
        url="https://example.com",
        output_dir=tmp_path,
        max_depth=1,
        respect_robots=True,
    )

    with (
        patch("crawldown.crawler.AsyncWebCrawler", return_value=ctx),
        patch("crawldown.crawler._fetch_robots", return_value=rp),
    ):
        results = await _crawl(config)

    crawled_urls = [r.url for r in results]
    assert "https://example.com/private/secret" not in crawled_urls


# ---------------------------------------------------------------------------
# CLI --include / --exclude flags
# ---------------------------------------------------------------------------


def test_cli_exclude_flag(tmp_path):
    from unittest.mock import patch as _patch

    from typer.testing import CliRunner

    from crawldown.cli import app

    fake_result = MagicMock()
    fake_result.markdown = "# Content"
    fake_result.links = {"internal": []}

    mock_instance = AsyncMock()
    mock_instance.arun.return_value = fake_result
    ctx = AsyncMock()
    ctx.__aenter__ = AsyncMock(return_value=mock_instance)
    ctx.__aexit__ = AsyncMock(return_value=None)

    runner = CliRunner()
    with _patch("crawldown.crawler.AsyncWebCrawler", return_value=ctx):
        result = runner.invoke(
            app,
            [
                "https://example.com",
                "--output",
                str(tmp_path),
                "--depth",
                "0",
                "--exclude",
                "/api/*",
            ],
        )

    assert result.exit_code == 0
