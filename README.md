# Photo Digitizing Guide

A plain-English manual for rescuing your family's printed photos, slides, and film negatives into a safe, organized digital archive — phone or flatbed, your choice, no cloud accounts required.

**Who it's for:** anyone with a shoebox of old prints, a carousel of slides, or envelopes of negatives, who wants them saved properly before time (and attic humidity) finishes the job. Written for beginners, step by step, never condescending.

## What's inside

| Chapter | Topic |
|---|---|
| 1 | Phone vs. flatbed: choosing your capture tool |
| 2 | Lighting setups — from a free window to a $20 LED jig |
| 3 | Resolution honesty: 600 dpi vs. 300 dpi, without the marketing |
| 4 | File naming with years and events |
| 5 | Folder trees that scale to 10,000 photos |
| 6 | Backup to two places (the 3-2-1 rule, household edition) |
| 7 | Sharing with relatives — cloud and no-cloud paths |
| 8 | Printing a keepsake: prints, albums, photo books |
| 9 | Printable scanner worksheets (inventory → session → verification) |
| 10 | Glossary of every term used |

## Quick start

Everything is local-first: plain Markdown sources, a zero-dependency Python build script, and a static HTML site it generates. Python 3.9+ is the only requirement.

```bash
# Build the static site into site/
python3 build.py

# Build and verify all internal links resolve
python3 build.py --check

# Run the test suite
python3 -m unittest discover -s tests -v

# Read the guide
python3 -m http.server 8000 --directory site
# then open http://localhost:8000
```

Prefer paper? Every chapter prints cleanly (the site hides navigation in print view), and the worksheets in chapter 9 are designed to be printed and filled in by hand.

## Bonus tool

`tools/verify_backup.py` verifies a backup copy of your archive byte-for-byte against the masters, using SHA-256 checksums:

```bash
python3 tools/verify_backup.py /path/to/masters /path/to/backup-drive/family-photos
```

## Companion guides

- **Photo Library Comfort Guide** — organizing the digital photos you already have
- **Backup Basics Handbook** — backup hardware and habits in more depth

## Design principles

- **Local-first.** No accounts, no subscriptions, no cloud required for any step.
- **Honest.** Resolution advice tells you when "good enough" is genuinely good enough.
- **Tested.** The build, every internal link, and the backup tool are covered by automated tests.
- **Beginner-friendly.** Plain English, printable checklists, decisions made *before* the first capture.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.

Part of the Asdale Dynamics collection of beginner-friendly guides and practical tools.
