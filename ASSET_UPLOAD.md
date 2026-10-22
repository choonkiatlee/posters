# Add page 001 artwork and previews

The repository contains the source code, YAML manuscript, and design configuration.
The binary images are in the prepared `posters_repo_ready.zip` from the ChatGPT
conversation. The GitHub connector cannot upload those image bytes directly.

## One-time upload

1. Download [the prepared ZIP from the conversation](https://chatgpt.com/) and save it locally, e.g. to `~/Downloads/posters_repo_ready.zip`.
2. In a terminal with Git access to your account, run:

```bash
git clone https://github.com/choonkiatlee/posters.git
cd posters
python scripts/import_book_assets.py ~/Downloads/posters_repo_ready.zip
git add projects/xiao-judan-world-tasting/assets projects/xiao-judan-world-tasting/generated
git commit -m "Add page 001 illustrations, original lettering and previews"
git push origin master
```

The importer only reads the archive's `assets/` and `generated/` folders, never
overwrites existing files, and preserves all source files already committed.

## Verify

The `Book page previews` GitHub Actions workflow checks both
original-lettering and editable-text render modes when the assets exist.
To regenerate locally:

```bash
cd projects/xiao-judan-world-tasting
python -m pip install -r requirements.txt
python render_book.py
python render_book.py --text-mode editable
```

No font binaries are included; editable-text mode uses a local replacement font.
These 1086×1448 illustrations are prototypes rather than print-resolution masters.
