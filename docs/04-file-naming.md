# File Naming: Years and Events

A file named `IMG_4821.jpg` is a mystery to whoever opens the folder after you — including future you. This chapter defines a naming scheme built on **years and events**: sortable, readable, and self-documenting.

## The pattern

```
YYYY-MM-DD_event_description_NNN
```

- `YYYY-MM-DD` — the date the photo was **taken** (best) or the event's approximate date.
- `event` — a short human label: `reunion`, `christmas`, `lake-trip`.
- `description` — optional, only when the event needs splitting.
- `NNN` — a zero-padded sequence number so files sort correctly.

### Examples

```
1962-06-15_wedding-ellen-ceremony_001.tif
1974-12-25_christmas-living-room_014.tif
1987-07-00_family-reunion-lake_003.tif     ← month known, day unknown
1990-00-00_vacation-florida_021.tif        ← year known only
```

## Handling unknown dates

Old photos rarely come labeled. Use zeros for unknown parts — **never guess a specific day you don't know**:

- Year known only: `1974-00-00_christmas_001`
- Year and month known: `1974-12-00_christmas_001`
- Year uncertain: use the best estimate and mark it: `1974c-00-00_christmas_001` (`c` = circa)

Zeros keep everything sortable, and "1974-00-00" honestly says *1974, sometime* instead of pretending to be June 3rd.

## Why years-and-events works

1. **Sorts chronologically for free.** Alphabetical order *is* chronological order. Open the folder and the family story reads top to bottom.
2. **Answers the two questions anyone actually asks:** *when was this?* and *what was happening?*
3. **Survives being copied.** The description travels inside the filename, so a file emailed to a cousin still explains itself years later.
4. **No database required.** No app, no catalog, no cloud service holding the metadata hostage.

## Rules that keep the scheme clean

1. **Lowercase everything.** `Christmas` and `christmas` will eventually both exist; prevent it.
2. **Hyphens between words, underscores between fields.** `1974-12-25_christmas-morning_001` — the eye separates fields instantly.
3. **Never use spaces or special characters** (`/ \ : * ? " < > | # & %`). They break on other operating systems and in web contexts.
4. **Zero-pad sequence numbers to 3 digits** (`001`, not `1`), so 100 sorts after 099.
5. **Keep event names short and consistent.** Pick `christmas`, not `xmas` one year and `dec-holiday` the next. Consistency beats cleverness.
6. **One event = one batch = one scan session**, ideally. Chapter 9's worksheet tracks this.

## What about people's names?

Use them in the description field when the event is generic: `1987-07-00_reunion-gramma-and-ellen_004.tif`. But don't overload filenames — if a photo's story is long, that belongs in a `notes.txt` inside the event folder (chapter 5) or in the photo's embedded metadata if your tools support it.

## Renaming what your phone/scanner produced

Your camera or scanner will emit `IMG_4821.jpg` or `scan0002.tif`. Rename **at the end of each batch**, while the session is fresh in your mind — never "later." A batch of 40 photos takes ten minutes to name at session's end and an hour to archaeology a year later.

Rename in place (your operating system's bulk-rename or a small script) and check the sort order immediately: if `010` appears before `002`, your padding is wrong.

## Next

Names need a home. [Chapter 5](05-folder-trees.md) builds the folder tree they live in.
