from unittest.mock import AsyncMock, patch

from typer.testing import CliRunner

from crawldown.cli import app

runner = CliRunner()


class _FakeResult:
    markdown = "# Hello from mock"
    links = {"internal": [{"href": "/about"}]}


def _mock_crawler():
    mock_instance = AsyncMock()
    mock_instance.arun.return_value = _FakeResult()
    ctx = AsyncMock()
    ctx.__aenter__ = AsyncMock(return_value=mock_instance)
    ctx.__aexit__ = AsyncMock(return_value=None)
    return ctx


def test_cli_creates_output_file(tmp_path):
    with patch("crawldown.crawler.AsyncWebCrawler", return_value=_mock_crawler()):
        result = runner.invoke(
            app,
            ["https://example.com", "--output", str(tmp_path), "--depth", "0"],
        )

    assert result.exit_code == 0, result.output
    md_files = list(tmp_path.rglob("*.md"))
    assert len(md_files) >= 1
    content = md_files[0].read_text()
    assert "Hello from mock" in content


def test_cli_respects_depth_zero(tmp_path):
    """With --depth 0 only the root URL is crawled, not discovered links."""
    with patch("crawldown.crawler.AsyncWebCrawler", return_value=_mock_crawler()):
        result = runner.invoke(
            app,
            ["https://example.com", "--output", str(tmp_path), "--depth", "0"],
        )

    assert result.exit_code == 0
    md_files = list(tmp_path.rglob("*.md"))
    # /about should NOT be crawled
    assert not any("about" in str(f) for f in md_files)


def test_cli_version_flag():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "crawldown" in result.output


def test_cli_ok_line_in_output(tmp_path):
    with patch("crawldown.crawler.AsyncWebCrawler", return_value=_mock_crawler()):
        result = runner.invoke(
            app,
            ["https://example.com", "--output", str(tmp_path), "--depth", "0"],
        )

    assert "OK" in result.output
    assert "https://example.com" in result.output
