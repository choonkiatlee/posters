# 《小巨蛋世界試吃計畫》

Traditional Chinese illustrated picture book combining botanical specimen pages with story pages. The current prototype is page 001 (青草), in the textured gouache style.

## Project files

- `book.yaml`: source manuscript, including specimen facts and story captions.
- `design.yaml`: typographic styles and layout coordinates.
- `render_book.py`: builds layered portrait SVGs, page PNG previews and a combined spread preview.
- `extract_original_text.py`: separates original lettering from the reference spread.
- `assets/illustrations/`: text-free portrait artwork (binary assets to be uploaded).
- `assets/reference/`: original reference spreads (binary assets to be uploaded).
- `assets/text_original/`: transparent original lettering PNGs (binary assets to be uploaded).
- `generated/`: outputs created by the renderer.

## Rebuild

Install dependencies and run these commands from this directory:

```bash
python -m pip install -r requirements.txt
python extract_original_text.py
python render_book.py
```

Original mode uses **raster original lettering**, which looks authentic but does not update when the YAML text changes.

For editable SVG text generated from YAML:

```bash
python render_book.py --text-mode editable
```

The font in editable mode is temporary and does not yet match the originals. Both modes keep illustration and lettering in separate SVG layers.

**Status:** All source files are committed; the PNG assets need to be added from the [prepared archive](../../ASSET_UPLOAD.md) before rendering works.
