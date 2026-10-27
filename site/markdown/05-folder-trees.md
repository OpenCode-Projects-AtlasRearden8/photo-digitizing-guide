# Folder Trees

File names give you chronology; folder structure gives you geography. This chapter lays out a tree simple enough to explain to a relative and sturdy enough for 10,000 photos.

## The recommended tree

```
family-photos/
├── masters/
│   ├── 1950s/
│   │   ├── 1957-00-00_house-warming/
│   │   │   ├── 1957-00-00_house-warming_001.tif
│   │   │   ├── 1957-00-00_house-warming_002.tif
│   │   │   └── notes.txt
│   │   └── 1959-06-00_ellen-graduation/
│   ├── 1960s/
│   │   └── 1962-06-15_wedding-ellen/
│   ├── 1970s/
│   ├── 1980s/
│   └── film/
│       ├── slides/
│       │   └── 1971-08-00_smoky-mountains/
│       └── negatives/
│           └── 1980-07-00_camping-trip/
├── shares/
│   └── 2026-03_family-album-for-aunt-ruth/
│       └── (JPEG copies for sharing)
├── projects/
│   └── 2026-12_gramma-keepsake-book/
│       └── (working files for chapter 8)
└── README.txt
```

## Why this shape

### Decade level: broad enough to never reorganize

Grouping by decade (`1950s`, `1960s`) means you never agonize over where `1962-06-15_wedding-ellen` goes — decades are unambiguous for any date that's known even to the year. Event folders inside carry the precise date from chapter 4's naming.

Uncertain dates? Use the decade of your best estimate. A photo labeled `1974c` lives in `1970s/`. Approximate-but-consistent beats precise-but-scattered.

### A `film/` branch for slides and negatives

Film originals are physically different objects (strips, mounts, sleeves) and were usually scanned in different sessions than prints. Giving them their own branch keeps scan batches and worksheets (chapter 9) clean. Their date/event folders use the same naming as prints.

### `masters/` is sacred

The `masters/` tree holds your **best, untouched files** — TIFFs from chapter 3, exactly as scanned. Nothing in `masters/` is ever edited, resized, renamed after filing, or deleted. Every other tree (`shares/`, `projects/`) contains *copies* made from masters.

This one separation prevents the most common archive disaster: editing a shared JPEG, sending it around, and losing the original.

### `shares/` and `projects/` are disposable by design

Everything in them can be deleted and rebuilt from masters. When a sharing batch for a relative is done, you can even empty it — chapter 6's backups stay focused on what's irreplaceable.

## The `notes.txt` habit

Each event folder gets a tiny `notes.txt`:

```
Event:   Smoky Mountains trip
Date:    August 1971 (approx)
People:  Gramma, Ellen, Dad (age ~12)
Source:  3 slide mounts, Kodachrome; scanned on Epson V600, 600 dpi
Notes:   The cabin photo is the one Mom always mentioned.
```

Five lines, written at the end of the scan session while memory is fresh. This is the cheapest archive technology that exists and one of the most valuable.

## The root `README.txt`

At the top of `family-photos/`, a short file explaining the scheme for whoever inherits it:

```
This folder is the family photo archive.
- masters/  : original scans, never edit these
- shares/   : copies made to send to relatives
- projects/ : working files for books and prints
Names are YYYY-MM-DD_event_NNN. Zeros mean "unknown".
Maintained by: (your name), last updated 2026.
```

## Rules

1. **Never nest event folders inside other event folders.** An event is one folder, however many photos it has.
2. **Never create a folder for fewer than ~5 photos** unless the event genuinely demands it — merge strays into a `_misc-1970s` folder per decade.
3. **Never rename or reorganize masters after backup** (chapter 6). Structure changes mean re-copying backups; do them together, deliberately.
4. **Folder count scales with events, not photos.** 10,000 photos in 150 event folders is manageable; 10,000 folders is not.

## Next

The tree exists on one disk. [Chapter 6](06-backup-two-places.md) makes sure it exists on at least two.
