# STATUS.md — Photo Digitizing Guide

**Status:** Complete and verified
**Last updated:** 2026-10-27
**Maintainer:** Asdale Dynamics, LLC

## What was built

A complete, beginner-friendly manual for digitizing printed photos, slides, and film negatives into a safe digital archive, delivered as Markdown sources plus a generated static HTML site.

### Content (docs/, 10 chapters)

| File | Chapter |
|---|---|
| `docs/00-start-here.md` | Introduction, reading paths, the one rule that matters most |
| `docs/01-phone-vs-flatbed.md` | Phone-scan vs. flatbed decision guide, with an honest comparison table |
| `docs/02-lighting-setups.md` | Three lighting setups (free window → two lamps → LED jig), film backlighting, self-check |
| `docs/03-resolution-honesty.md` | 600 dpi vs. 300 dpi honesty: what dpi buys you, file-size reality, TIFF-master/JPEG-share policy |
| `docs/04-file-naming.md` | Years-and-events naming (`YYYY-MM-DD_event_NNN`), unknown-date zeros, circa markers |
| `docs/05-folder-trees.md` | `masters/` / `shares/` / `projects/` tree with decade grouping, `notes.txt` habit, root README.txt |
| `docs/06-backup-two-places.md` | 3-2-1 rule for households, backup routine, verification, cloud caveats, inheritance test |
| `docs/07-sharing-with-relatives.md` | Sharing copies (not masters), no-cloud and cloud paths, family etiquette |
| `docs/08-printing-a-keepsake.md` | Prints, albums, photo books, framing; resolution-in-reverse sharpness table |
| `docs/09-scanner-worksheets.md` | Five printable worksheets: inventory, session plan, batch log, close-out, verification |
| `docs/10-glossary.md` | Plain-English glossary of every term used in the guide |

### Code and tooling

- `build.py` — zero-dependency (stdlib-only) Markdown→HTML site generator: headings, lists, tables, fenced code, blockquotes, inline formatting, prev/next pager, sidebar nav, print stylesheet. `--check` flag validates all internal links. Copies raw Markdown into `site/markdown/` for offline completeness.
- `tools/verify_backup.py` — SHA-256 checksum verification of a backup copy against the masters; reports missing/extra/mismatched files, exit code 0 on success.
- `tests/test_build.py` — 26 automated tests (stdlib `unittest`).

### Supporting files

- `README.md` — project overview, quick-start commands, design principles, credits Asdale Dynamics, LLC.
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`.

## How to run it

```bash
# Build the static site (outputs to site/)
python3 build.py

# Build + validate internal links
python3 build.py --check

# Run the test suite
python3 -m unittest discover -s tests -v

# Preview the site locally
python3 -m http.server 8000 --directory site
# open http://localhost:8000

# Verify a backup against the masters
python3 tools/verify_backup.py /path/to/masters /path/to/backup
```

Requires Python 3.9+ only. No accounts, no network, no third-party packages.

## Verification results

- `python3 build.py --check` → **22 files built, all internal links resolve** ✅
- `python3 -m unittest discover -s tests -v` → **26 tests, 0 failures** ✅
  - Docs completeness: all 10 chapters present, every required topic term found
  - Renderer unit tests: headings, lists, tables, code blocks, escaping, links
  - Build output: every page has nav, footer, copyright, valid HTML structure, no unrewritten `.md` links
  - Project integrity: LICENSE copyright line exact, README credit present, no secret patterns in text files
  - `tools/verify_backup.py` behavior: detects identical copies and mismatches correctly
- Site structural sweep: all pages contain `<h1>`, DOCTYPE, closing `</html>`, no raw markdown leakage ✅

## Known gaps / future work

- No photos or diagrams in the docs yet — annotated lighting-diagram images would help chapter 2.
- The `--check` link validator does not fetch external URLs (by design, to stay offline); external links are unverified.
- Chapter 8 (keepsakes) is service-agnostic on purpose; a regional print-service appendix could be added later.
- No CI configuration is included; tests are runnable locally with one command.
- The site uses a single built-in CSS theme; theming/dark mode is unexplored.

## Related projects

- **photo-library-comfort-guide** — organizing digital photos you already have (complement, referenced in chapters 0 and 10)
- **backup-basics-handbook** — deeper backup hardware and habits (complement, referenced in chapter 0)
