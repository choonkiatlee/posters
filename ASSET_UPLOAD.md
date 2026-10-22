# Upload the book's image assets

The connected GitHub integration can commit text files but cannot transfer the binary PNG assets from the prepared local archive. The `posters` source files are committed; finish by uploading the PNG assets from the ZIP provided in the ChatGPT conversation.

1. Download and unzip `posters_repo_ready.zip`.
2. Clone `https://github.com/choonkiatlee/posters.git`.
3. Copy the contents of the extracted `posters/projects/xiao-judan-world-tasting/assets/` folder into the same location in your clone.
4. You can also copy the `generated/` folder to include ready-made SVG masters and PNG previews. The SVGs use relative links to the PNGs.
5. Run `git add projects/xiao-judan-world-tasting/assets projects/xiao-judan-world-tasting/generated`, commit, and push.

The archive also contains scripts and documentation; do **not** overwrite newer files in the repository when copying. No font binaries should be committed.

The original image masters are 1086×1448 pixels each. This is a prototype, not a print-ready resolution.
