from crawldown.writer import resolve_output_path, write_page


def test_resolve_output_path_nested(tmp_path):
    path = resolve_output_path("https://example.com", "https://example.com/docs/intro", tmp_path)
    assert path == tmp_path / "docs" / "intro" / "index.md"


def test_resolve_output_path_root(tmp_path):
    path = resolve_output_path("https://example.com", "https://example.com", tmp_path)
    assert path == tmp_path / "index" / "index.md"


def test_resolve_output_path_subpage_as_root_url(tmp_path):
    # Regression: when root_url is netloc root, crawling a subpage directly
    # must write to its own path, not silently to index/index.md
    path = resolve_output_path(
        "https://example.com/",
        "https://example.com/privacy-policy",
        tmp_path,
    )
    assert path == tmp_path / "privacy-policy" / "index.md"
    assert path != tmp_path / "index" / "index.md"


def test_write_page_creates_file(tmp_path):
    path = tmp_path / "docs" / "page.md"
    write_page(path, "https://example.com/docs/page", "# Hello")
    assert path.exists()
    content = path.read_text()
    assert "# Source: https://example.com/docs/page" in content
    assert "# Hello" in content


def test_write_page_creates_parent_dirs(tmp_path):
    path = tmp_path / "a" / "b" / "c" / "page.md"
    write_page(path, "https://example.com/a/b/c/page", "content")
    assert path.exists()
