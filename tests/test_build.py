#!/usr/bin/env python3
"""Tests for the Photo Digitizing Guide.

Run:  python3 -m unittest discover -s tests -v
      or: python3 tests/test_build.py

Standard library only, matching the project's local-first, zero-dependency rule.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
BUILD = ROOT / "build.py"

sys.path.insert(0, str(ROOT))
import build  # noqa: E402

REQUIRED_TOPICS = {
    "00-start-here.md": ["phone", "flatbed", "archive", "Asdale Dynamics"],
    "01-phone-vs-flatbed.md": ["phone", "flatbed", "slide", "negative", "album"],
    "02-lighting-setups.md": ["glare", "45", "window", "flash", "light pad"],
    "03-resolution-honesty.md": ["300 dpi", "600 dpi", "TIFF", "JPEG"],
    "04-file-naming.md": ["YYYY-MM-DD", "event", "zero-pad", "sort"],
    "05-folder-trees.md": ["masters", "shares", "projects", "notes.txt", "decade"],
    "06-backup-two-places.md": ["3-2-1", "off-site", "external drive", "verify"],
    "07-sharing-with-relatives.md": ["shares", "USB", "relatives", "JPEG"],
    "08-printing-a-keepsake.md": ["print", "book", "300 pixels per inch", "caption"],
    "09-scanner-worksheets.md": ["Worksheet A", "Worksheet B", "Worksheet C",
                                 "Worksheet D", "Worksheet E"],
    "10-glossary.md": ["3-2-1 rule", "DPI", "TIFF", "masters", "off-site"],
}

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]


class TestDocs(unittest.TestCase):
    def test_all_docs_exist(self):
        expected = set(REQUIRED_TOPICS)
        actual = {p.name for p in DOCS.glob("*.md")}
        self.assertEqual(expected, actual)

    def test_each_doc_starts_with_h1_title(self):
        for path in sorted(DOCS.glob("*.md")):
            first_heading = None
            for line in path.read_text(encoding="utf-8").split("\n"):
                if line.startswith("# "):
                    first_heading = line[2:].strip()
                    break
            self.assertTrue(first_heading, f"{path.name} has no H1 title")

    def test_required_topics_covered(self):
        for name, terms in REQUIRED_TOPICS.items():
            text = (DOCS / name).read_text(encoding="utf-8").lower()
            for term in terms:
                self.assertIn(term.lower(), text, f"{name} missing term: {term}")

    def test_internal_links_resolve(self):
        problems = build.check_links()
        self.assertEqual([], problems)


class TestMarkdownRenderer(unittest.TestCase):
    def test_headings(self):
        html = build.markdown_to_html("# Title\n\n## Sub")
        self.assertIn("<h1>Title</h1>", html)
        self.assertIn("<h2>Sub</h2>", html)

    def test_paragraph_and_bold_italic(self):
        html = build.markdown_to_html("This is **bold** and *italic*.")
        self.assertIn("<p>This is <strong>bold</strong> and <em>italic</em>.</p>", html)

    def test_inline_code_protected(self):
        html = build.markdown_to_html("Use `YYYY-MM-DD_event` names with *stars*.")
        self.assertIn("<code>YYYY-MM-DD_event</code>", html)
        self.assertNotIn("<em>", html.split("<code>")[1].split("</code>")[0])

    def test_links(self):
        html = build.markdown_to_html("See [chapter 2](02-lighting-setups.md).")
        self.assertIn('<a href="02-lighting-setups.html">chapter 2</a>', html)

    def test_external_links_untouched(self):
        html = build.markdown_to_html("See [docs](https://example.com/guide.md).")
        self.assertIn('<a href="https://example.com/guide.md">docs</a>', html)

    def test_unordered_list(self):
        html = build.markdown_to_html("- one\n- two\n- three")
        self.assertEqual(3, html.count("<li>"))
        self.assertIn("<ul>", html)

    def test_ordered_list(self):
        html = build.markdown_to_html("1. one\n2. two")
        self.assertEqual(2, html.count("<li>"))
        self.assertIn("<ol>", html)

    def test_table(self):
        md = "| a | b |\n|---|---|\n| 1 | 2 |"
        html = build.markdown_to_html(md)
        self.assertIn("<table>", html)
        self.assertIn("<th>a</th>", html)
        self.assertIn("<td>2</td>", html)

    def test_fenced_code_block_escapes(self):
        html = build.markdown_to_html("```\n<b>& raw\n```")
        self.assertIn("&lt;b&gt;&amp; raw", html)

    def test_blockquote(self):
        html = build.markdown_to_html("> A wise saying.")
        self.assertIn("<blockquote>", html)
        self.assertIn("A wise saying.", html)

    def test_horizontal_rule(self):
        html = build.markdown_to_html("above\n\n---\n\nbelow")
        self.assertIn("<hr>", html)

    def test_html_is_escaped_in_text(self):
        html = build.markdown_to_html("Use <script> carefully.")
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)


class TestBuildOutput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            [sys.executable, str(BUILD), "--check"],
            capture_output=True, text=True, cwd=ROOT,
        )
        cls.result = result

    def test_build_succeeds(self):
        self.assertEqual(0, self.result.returncode,
                         f"build failed:\n{self.result.stdout}\n{self.result.stderr}")

    def test_site_contains_all_pages(self):
        for path in DOCS.glob("*.md"):
            page = ROOT / "site" / (path.stem + ".html")
            self.assertTrue(page.exists(), f"missing site page: {page.name}")

    def test_pages_have_nav_and_footer(self):
        for page in (ROOT / "site").glob("*.html"):
            html = page.read_text(encoding="utf-8")
            self.assertIn('class="toc"', html, page.name)
            self.assertIn("Asdale Dynamics, LLC", html, page.name)
            self.assertIn("<!DOCTYPE html>", html, page.name)

    def test_prev_next_pager(self):
        first = (ROOT / "site" / "00-start-here.html").read_text(encoding="utf-8")
        self.assertNotIn("Previous", first.split("<main>")[1].split("</main>")[0].split('class="pager"')[1])
        self.assertIn("Next", first)
        last = (ROOT / "site" / "10-glossary.html").read_text(encoding="utf-8")
        self.assertIn("Previous", last)

    def test_content_links_point_to_html(self):
        html = (ROOT / "site" / "10-glossary.html").read_text(encoding="utf-8")
        body = html.split("<main>")[1]
        self.assertIn('href="03-resolution-honesty.html"', body)
        self.assertNotIn('.md"', body)

    def test_all_site_pages_have_no_md_hrefs_in_content(self):
        for page in (ROOT / "site").glob("*.html"):
            body = page.read_text(encoding="utf-8").split("<main>")[1]
            self.assertNotIn('.md"', body, f"{page.name} has unrewritten .md link")


class TestProjectIntegrity(unittest.TestCase):
    def test_license_exact_copyright(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", license_text)
        self.assertIn("MIT", license_text)

    def test_readme_credits_and_instructions(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", readme)
        self.assertIn("python3 build.py", readme)

    def test_no_secrets_in_text_files(self):
        offenders = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or "site" in path.parts:
                continue
            if path.suffix.lower() not in {".md", ".py", ".txt", ".html", ".cfg", ".toml", ".json"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    offenders.append(f"{path.name}: {pattern.pattern}")
        self.assertEqual([], offenders)

    def test_verify_backup_tool_detects_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            src, dst = tmp / "a", tmp / "b"
            (src / "sub").mkdir(parents=True)
            (dst / "sub").mkdir(parents=True)
            (src / "sub" / "x.txt").write_text("same")
            (dst / "sub" / "x.txt").write_text("same")
            ok = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "verify_backup.py"), str(src), str(dst)],
                capture_output=True, text=True,
            )
            self.assertEqual(0, ok.returncode)
            (dst / "sub" / "x.txt").write_text("changed")
            bad = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "verify_backup.py"), str(src), str(dst)],
                capture_output=True, text=True,
            )
            self.assertEqual(1, bad.returncode)
            self.assertIn("MISMATCH", bad.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
