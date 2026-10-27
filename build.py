#!/usr/bin/env python3
"""Build the Photo Digitizing Guide static site.

Converts docs/*.md into site/*.html with shared navigation and styling.
Zero third-party dependencies: standard library only.

Usage:
    python3 build.py            # build site/
    python3 build.py --check    # build and validate internal links
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

SITE_TITLE = "Photo Digitizing Guide"
SITE_TAGLINE = "Rescue printed photos, slides, and film into a safe digital archive"


# --------------------------------------------------------------------------
# Minimal Markdown -> HTML
# --------------------------------------------------------------------------

def escape(text: str) -> str:
    return html.escape(text, quote=True)


def inline(text: str) -> str:
    """Inline markdown: code, bold, italic, links."""
    placeholders: list[str] = []

    def stash(html_frag: str) -> str:
        placeholders.append(html_frag)
        return f"\x00{len(placeholders) - 1}\x00"

    # Inline code first, protected from other rules.
    text = re.sub(r"`([^`]+)`", lambda m: stash(f"<code>{escape(m.group(1))}</code>"), text)
    # Links [label](target); internal .md targets become .html pages.
    def link(m: re.Match) -> str:
        target = m.group(2)
        if not target.startswith(("http://", "https://", "mailto:")) and target.endswith(".md"):
            target = target[:-3] + ".html"
        return stash(f'<a href="{escape(target)}">{escape(m.group(1))}</a>')

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    # Escape before inserting our own tags, so user HTML stays escaped.
    text = escape(text)
    # Bold, italic (safe on escaped text: '*' is never escaped)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    # Restore stashed fragments.
    text = re.sub(r"\x00(\d+)\x00", lambda m: placeholders[int(m.group(1))], text)
    return text


def table_html(rows: list[str]) -> str:
    header = [c.strip() for c in rows[0].strip().strip("|").split("|")]
    body_rows = rows[2:]  # skip separator row
    out = ["<table>", "<thead><tr>"]
    out += [f"<th>{inline(c)}</th>" for c in header]
    out.append("</tr></thead><tbody>")
    for row in body_rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def markdown_to_html(md: str) -> str:
    lines = md.split("\n")
    out: list[str] = []
    i = 0
    para: list[str] = []

    def flush_para() -> None:
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]

        # Fenced code block
        if line.startswith("```"):
            flush_para()
            i += 1
            code: list[str] = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1  # closing fence
            out.append(f"<pre><code>{escape(chr(10).join(code))}</code></pre>")
            continue

        # Heading
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_para()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2).strip())}</h{level}>")
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^-{3,}$", line.strip()) or re.match(r"^\*{3,}$", line.strip()):
            flush_para()
            out.append("<hr>")
            i += 1
            continue

        # Table (header row, separator, then rows)
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            flush_para()
            block = [line]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            out.append(table_html(block))
            continue

        # Blockquote
        if line.startswith("> "):
            flush_para()
            quote: list[str] = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> "))
                i += 1
            out.append(f"<blockquote><p>{inline(' '.join(q for q in quote if q))}</p></blockquote>")
            continue

        # Unordered list
        if re.match(r"^\s*[-*]\s+", line):
            flush_para()
            items: list[str] = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ul>")
            continue

        # Ordered list
        if re.match(r"^\s*\d+\.\s+", line):
            flush_para()
            oitems: list[str] = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                oitems.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(it)}</li>" for it in oitems) + "</ol>")
            continue

        # Blank line
        if not line.strip():
            flush_para()
            i += 1
            continue

        para.append(line.strip())
        i += 1

    flush_para()
    return "\n".join(out)


# --------------------------------------------------------------------------
# Site assembly
# --------------------------------------------------------------------------

def doc_title(md_text: str, fallback: str) -> str:
    for line in md_text.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def slug_of(path: Path) -> str:
    return path.stem + ".html"


def load_docs() -> list[tuple[Path, str, str]]:
    """Return [(path, title, markdown)] for docs/*.md sorted by filename."""
    docs = []
    for path in sorted(DOCS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        docs.append((path, doc_title(text, path.stem), text))
    return docs


STYLE = """
:root {
  --ink: #1f2430;
  --muted: #5b6472;
  --paper: #fbfaf7;
  --card: #ffffff;
  --accent: #7a4a1f;
  --accent-soft: #f3e7d8;
  --line: #e4ded2;
  --code-bg: #f1efe8;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Georgia, 'Times New Roman', serif;
  color: var(--ink);
  background: var(--paper);
  line-height: 1.65;
}
header.site {
  background: var(--accent);
  color: #fff;
  padding: 1.2rem 1.5rem;
}
header.site h1 { margin: 0; font-size: 1.4rem; font-family: Georgia, serif; }
header.site p { margin: 0.2rem 0 0; font-size: 0.95rem; opacity: 0.9; }
header.site a { color: #fff; text-decoration: none; }
.layout { display: flex; flex-wrap: wrap; max-width: 70rem; margin: 0 auto; }
nav.toc {
  flex: 0 0 16rem;
  padding: 1.5rem 1rem;
  border-right: 1px solid var(--line);
}
nav.toc ol { list-style: none; margin: 0; padding: 0; }
nav.toc li { margin: 0.35rem 0; }
nav.toc a { color: var(--accent); text-decoration: none; display: block; padding: 0.25rem 0.5rem; border-radius: 4px; }
nav.toc a:hover { background: var(--accent-soft); }
nav.toc a.active { background: var(--accent-soft); font-weight: bold; }
main { flex: 1 1 30rem; padding: 1.5rem 2rem 3rem; max-width: 46rem; }
main h1 { font-size: 1.9rem; margin-top: 0; border-bottom: 2px solid var(--accent-soft); padding-bottom: 0.4rem; }
main h2 { font-size: 1.35rem; margin-top: 2rem; }
main a { color: var(--accent); }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.95rem; }
th, td { border: 1px solid var(--line); padding: 0.45rem 0.6rem; text-align: left; vertical-align: top; }
th { background: var(--accent-soft); }
pre {
  background: var(--code-bg);
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 0.9rem 1rem;
  overflow-x: auto;
  font-size: 0.85rem;
  line-height: 1.45;
}
code { font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; font-size: 0.9em; background: var(--code-bg); padding: 0.1em 0.3em; border-radius: 3px; }
pre code { background: none; padding: 0; }
blockquote {
  margin: 1rem 0; padding: 0.6rem 1rem;
  border-left: 4px solid var(--accent);
  background: var(--accent-soft);
  font-style: italic;
}
.pager { display: flex; justify-content: space-between; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--line); }
.pager a { color: var(--accent); text-decoration: none; }
.pager a:hover { text-decoration: underline; }
footer.site { text-align: center; color: var(--muted); font-size: 0.85rem; padding: 1.5rem; border-top: 1px solid var(--line); }
@media (max-width: 50rem) {
  nav.toc { flex: 1 1 100%; border-right: none; border-bottom: 1px solid var(--line); }
}
@media print {
  header.site, nav.toc, .pager, footer.site { display: none; }
  main { max-width: none; padding: 0; }
  pre { white-space: pre-wrap; border: 1px solid #ccc; }
  body { background: #fff; }
}
"""


def page_html(title: str, body: str, docs: list[tuple[Path, str, str]], current: str, prev: str | None, nxt: str | None) -> str:
    nav_items = []
    for path, dtitle, _ in docs:
        slug = slug_of(path)
        cls = ' class="active"' if slug == current else ""
        nav_items.append(f'<li><a href="{slug}"{cls}>{escape(dtitle)}</a></li>')
    prev_link = f'<a href="{prev}">&larr; Previous</a>' if prev else "<span></span>"
    next_link = f'<a href="{nxt}">Next &rarr;</a>' if nxt else "<span></span>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} &middot; {SITE_TITLE}</title>
<style>{STYLE}</style>
</head>
<body>
<header class="site">
<h1><a href="index.html">{SITE_TITLE}</a></h1>
<p>{SITE_TAGLINE}</p>
</header>
<div class="layout">
<nav class="toc" aria-label="Chapters">
<ol>
{chr(10).join(nav_items)}
</ol>
</nav>
<main>
{body}
<div class="pager">{prev_link}{next_link}</div>
</main>
</div>
<footer class="site">
<p>Photo Digitizing Guide &middot; &copy; 2026 Asdale Dynamics, LLC &middot; MIT licensed &middot; local-first, no accounts required</p>
</footer>
</body>
</html>
"""


def build() -> list[str]:
    """Build site/. Returns list of relative page names written."""
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    docs = load_docs()
    if not docs:
        sys.exit("No markdown files found in docs/")

    slugs = [slug_of(p) for p, _, _ in docs]
    written: list[str] = []

    for idx, (path, title, md) in enumerate(docs):
        body = markdown_to_html(md)
        prev = slugs[idx - 1] if idx > 0 else None
        nxt = slugs[idx + 1] if idx < len(docs) - 1 else None
        page = page_html(title, body, docs, slug_of(path), prev, nxt)
        out = SITE / slug_of(path)
        out.write_text(page, encoding="utf-8")
        written.append(slug_of(path))

    # Copy the raw markdown alongside the site for offline completeness.
    raw = SITE / "markdown"
    raw.mkdir()
    for path, _, _ in docs:
        shutil.copy(path, raw / path.name)
        written.append(f"markdown/{path.name}")

    return written


def check_links() -> list[str]:
    """Validate that every internal markdown link resolves to a doc file."""
    problems: list[str] = []
    doc_names = {p.name for p, _, _ in load_docs()}
    for path, title, md in load_docs():
        for target in re.findall(r"\]\(([^)\s]+)\)", md):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            name = target.split("#")[0]
            if name and name not in doc_names:
                problems.append(f"{path.name}: broken internal link -> {target}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the Photo Digitizing Guide site")
    parser.add_argument("--check", action="store_true", help="also validate internal links")
    args = parser.parse_args()

    written = build()
    print(f"Built {len(written)} files into {SITE.relative_to(ROOT)}/")

    if args.check:
        problems = check_links()
        if problems:
            for p in problems:
                print(f"LINK ERROR: {p}", file=sys.stderr)
            return 1
        print("All internal links resolve.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
