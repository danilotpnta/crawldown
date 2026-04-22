from pathlib import Path

from crawldown.extractor import url_to_path


def resolve_output_path(base_url: str, page_url: str, output_dir: Path) -> Path:
    parts = url_to_path(base_url, page_url)
    # If the last part has no extension, treat it as a directory with index.md
    last = parts[-1]
    if "." not in last:
        parts[-1] = last
        path = output_dir.joinpath(*parts) / "index.md"
    else:
        parts[-1] = last + ".md"
        path = output_dir.joinpath(*parts)
    return path


def write_page(path: Path, url: str, markdown: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = f"# Source: {url}\n\n"
    path.write_text(header + markdown, encoding="utf-8")
