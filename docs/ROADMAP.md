# crawldown — Roadmap

This file lists planned future features. Contributions are welcome — open an issue or PR.

---

## Known limitations

### Button-based navigation

Some sites (e.g. React/Next.js SPAs) render footer and navigation links as `<button>` elements with JavaScript click handlers instead of `<a href="...">` anchors. Standard link extraction only reads `<a>` tags, so these pages are invisible to the crawler regardless of depth or JS-rendering settings. The workaround for affected sites is to seed the crawl with the specific URLs you need (e.g. `crawldown https://example.com/terms-and-conditions`), or wait for sitemap.xml support (see below) which bypasses link discovery entirely.

---

## Planned features

### `[Feature] Add index.json output`

After a crawl completes, write an `index.json` manifest alongside the Markdown files. The manifest would list every crawled URL with its title, relative output path, and crawl depth. This gives downstream tools (search indexers, RAG pipelines, static site generators) a structured entry point without having to parse Markdown files.

### `[Feature] Incremental / resume crawl`

Save crawl state to disk so a run can be resumed after interruption. On restart, already-crawled URLs would be skipped and only new or changed pages fetched. Essential for large sites that take minutes or hours to fully crawl.

### `[Feature] Sitemap.xml support`

Accept a `sitemap.xml` URL as the seed list instead of (or in addition to) following links. Sitemaps are faster and more complete for sites that publish one, and they remove the dependency on rendered HTML for link discovery.

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for branch, commit, and PR conventions.
