#!/usr/bin/env python3
"""Copy illustration assets and page previews from the prepared project ZIP.

Run from a clone of choonkiatlee/posters:
    python scripts/import_book_assets.py ~/Downloads/posters_repo_ready.zip

Imports only the book's assets/ and generated/ folders.
"""
from pathlib import Path, PurePosixPath
import sys
from zipfile import ZipFile

REPO_ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = PurePosixPath('posters/projects/xiao-judan-world-tasting')
TARGET_ROOT = Path('projects/xiao-judan-world-tasting')
ALLOWED = ('assets/', 'generated/')


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python scripts/import_book_assets.py PATH_TO_ZIP')
    archive = Path(sys.argv[1]).expanduser()
    n = 0
    with ZipFile(archive) as z:
        for member in z.infolist():
            relative = PurePosixPath(member.filename)
            try:
                subpath = relative.relative_to(ARCHIVE_ROOT)
            except ValueError:
                continue
            if member.is_dir() or not any(str(subpath).startswith(p) for p in ALLOWED):
                continue
            if '..' in subpath.parts or subpath.is_absolute():
                raise ValueError(f'Unsafe path in archive: {member.filename}')
            destination = REPO_ROOT / TARGET_ROOT / Path(*subpath.parts)
            if destination.exists():
                print('EXISTS', destination.relative_to(REPO_ROOT))
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(z.read(member))
            print('ADDED ', destination.relative_to(REPO_ROOT))
            n += 1
    print(f'Imported {n} new files. Review and commit the assets to GitHub.')


if __name__ == '__main__':
    main()
