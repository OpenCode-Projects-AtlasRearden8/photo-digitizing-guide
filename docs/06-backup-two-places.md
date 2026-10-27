# Backup to Two Places

A scan that exists on one disk does not exist. This chapter turns the professional **3-2-1 rule** into something a household can actually maintain — no cloud accounts required.

## The 3-2-1 rule, plainly

- **3** copies of everything
- **2** different types of storage (e.g., an internal drive and an external drive)
- **1** copy somewhere else entirely (a different building)

For this project the honest, minimal version is:

> **Two full copies of `masters/`, in two devices, one of which lives outside your home.**

That's the "backup to two places" this guide promises: your working drive, plus an external drive you keep updated, plus — for the irreplaceable masters — a copy at a relative's house or in a safe deposit box.

## Choosing drives

- **External portable drive (1–2 TB, USB):** the workhorse. One is enough for a photo archive for years — 10,000 TIFFs at 600 dpi is roughly 25 GB; even generous collections stay under 100 GB.
- **Second external drive or a desktop backup drive:** the off-site copy. Cheap insurance.
- **USB flash drives:** acceptable for the off-site copy of a small archive, but they're easy to lose and slower to verify. Prefer a real drive.
- **Optical discs (DVD/BD):** still valid and long-lived, but drives are disappearing from new computers. Only choose this if you already burn discs confidently.

Avoid: keeping the only second copy on the *same physical drive* (a second partition is not a second place), and unpowered "cloud-adjacent" gadgets that need accounts.

## The backup routine

### After every scan session (5 minutes)

1. Copy the new event folders from your working drive to **external drive #1**.
2. Eject properly, label the drive ("photo archive — mirror"), done.

### Monthly (10 minutes)

1. Re-copy anything new since last month to drive #1.
2. Spot-check: open five random photos from drive #1 and confirm they display.

### Twice a year (30 minutes)

1. Make or refresh the **off-site copy** on drive #2.
2. Take drive #2 to a relative's house, office drawer, or safe deposit box. It should *live* there, not in the same bag as drive #1.
3. While you're at it, verify drive #1 fully (below).

## Verification: a backup is only real if it opens

The single most common backup failure is a copy that was made but never tested. Twice a year:

1. Pick 10 files at random across different years.
2. Open each from the backup drive — image displays fully, file size matches the master.
3. Compare folder counts: the backup's event-folder count equals the masters' count.

If you're comfortable with a terminal, a checksum check is stronger. This project ships a helper for exactly that — see `tools/verify_backup.py` and the "Bonus tool" section of the README:

```
python3 tools/verify_backup.py /path/to/masters /path/to/backup-drive/family-photos
```

It walks both trees and reports any file that is missing, extra, or has changed. Exit status 0 means the backup is verified.

## What about the cloud?

This guide is **local-first**: nothing here requires an account, a subscription, or an internet connection. Cloud backup is a legitimate *extra* layer if you already trust a provider — but it is not required for a safe archive, and it is not a substitute for the off-site drive. The two-place rule above stands on its own.

## Ransomware, accidents, and versioning

One refinement worth ten minutes: keep the off-site copy **disconnected** except during updates. A drive that's only plugged in twice a year is immune to anything that happens to your computer in between — malware, accidental mass deletion, a bad software update. Rotation *is* the versioning.

## The inheritance test

Your backup plan should be explainable in two sentences to the person who'd deal with it if you couldn't:

> "The family photos are in the `family-photos` folder on my computer. The dark gray drive in the safe box has the second copy — just copy the whole folder."

If you can't say that yet, write it into the root `README.txt` from chapter 5 and tell one person where the drive is.

## Next

With the archive safe, it's time to share it — [chapter 7](07-sharing-with-relatives.md).
