import os
import re
from typing import List, Optional
from src.layout.notes_models import Block, Theme, Note


class NotesProcessor:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def _read_file(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _sanitize_title(self, filename: str) -> str:
        # Strip extension
        name = os.path.splitext(filename)[0]
        # Replace underscores with spaces for better readability and wrapping
        name = name.replace("_", " ")
        # Strip leading numbers (logic from advanced_pdf.sh)
        # sed -E 's/^[0-9]+([._-][0-9]+)*[.)]?[[:space:]]+//'
        return re.sub(r"^[0-9]+([._-][0-9]+)*[.)]?\s+", "", name)

    def _get_sorted_items(self, path: str, item_type="all"):
        try:
            items = os.listdir(path)
        except OSError:
            return []

        filtered = []
        for item in items:
            full_path = os.path.join(path, item)
            if item_type == "dir" and not os.path.isdir(full_path):
                continue
            if item_type == "file" and (
                not os.path.isfile(full_path) or not item.endswith(".md")
            ):
                continue
            filtered.append(item)

        # Sort naturally (version sort)
        # Using a simple alphanumeric sort since python doesn't have native "version sort" like `sort -V`
        # But we can approximate with re.split
        def natural_keys(text):
            return [
                int(c) if c.isdigit() else c.lower() for c in re.split(r"(\d+)", text)
            ]

        return sorted(filtered, key=natural_keys)

    def load_structure(self) -> List[Block]:
        blocks_data = []

        # Find Blocks
        block_dirs = self._get_sorted_items(self.root_dir, "dir")

        # Filter for "Блок" prefix if they exist, otherwise take all dirs
        filtered_blocks = [d for d in block_dirs if d.startswith("Блок")]
        if not filtered_blocks and block_dirs:
            # If no "Блок" dirs, but there are dirs, treat all as blocks
            filtered_blocks = block_dirs

        if not filtered_blocks:
            # Check if root_dir itself has markdown files. If so, treat root_dir as a block.
            md_files = self._get_sorted_items(self.root_dir, "file")
            if md_files:
                # Treat root_dir as a single block
                return [
                    self._process_block(self.root_dir, os.path.basename(self.root_dir))
                ]
            return []

        for block_name in filtered_blocks:
            block_path = os.path.join(self.root_dir, block_name)
            blocks_data.append(self._process_block(block_path, block_name))

        return blocks_data

    def _process_block(self, block_path: str, block_name: str) -> Block:
        themes_data = []

        # Find Themes (subdirectories)
        theme_dirs = self._get_sorted_items(block_path, "dir")

        for theme_folder in theme_dirs:
            theme_path = os.path.join(block_path, theme_folder)

            # Look for intro note: block_dir/theme_name.md
            intro_path = os.path.join(block_path, f"{theme_folder}.md")
            intro_note = None
            if os.path.exists(intro_path):
                intro_note = Note(
                    title=self._sanitize_title(os.path.basename(intro_path)),
                    content=self._read_file(intro_path),
                    file_path=intro_path,
                )

            notes = []
            note_files = self._get_sorted_items(theme_path, "file")
            for note_file in note_files:
                n_path = os.path.join(theme_path, note_file)
                notes.append(
                    Note(
                        title=self._sanitize_title(note_file),
                        content=self._read_file(n_path),
                        file_path=n_path,
                    )
                )

            themes_data.append(
                Theme(title=theme_folder, notes=notes, intro_note=intro_note)
            )

        # Find direct notes in block directory that aren't theme intros
        direct_notes = []
        theme_intro_files = {f"{d}.md" for d in theme_dirs}
        block_files = self._get_sorted_items(block_path, "file")
        for f in block_files:
            if f not in theme_intro_files:
                f_path = os.path.join(block_path, f)
                direct_notes.append(
                    Note(
                        title=self._sanitize_title(f),
                        content=self._read_file(f_path),
                        file_path=f_path,
                    )
                )

        return Block(title=block_name, themes=themes_data, direct_notes=direct_notes)
