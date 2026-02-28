# Markdown to PDF Notes Generator

A sophisticated tool for converting structured Markdown notes into a professional, readable PDF compilation. Optimized for exam preparation and scientific notes, with full support for Cyrillic and hierarchical document structure.

## Features

- **Continuous Flow Layout**: Notes and themes flow seamlessly across pages to save space, with intelligent page break triggers to avoid orphan headers.
- **Hierarchical Numbering**: Automatically numbers notes (1, 2, 3...) and demotes internal headers to maintain a logical document structure in the PDF.
- **Service Object Architecture**: Built with a clean 3-layer structure (Models, Logic, Workers) for maintainability.
- **Total Typography Control**: Centralized `config.py` allows adjusting fonts, sizes, line heights, and margins without touching the logic.
- **Professional Fonts**: Uses `Liberation Serif` for high readability and full Cyrillic support.
- **PDF Outlines**: Generates a clickable sidebar (bookmarks) in your PDF viewer for instant navigation.

## Project Structure

```text
bullet_journal/
├── create_notes_pdf.py       # Main entry point (CLI)
├── pyproject.toml            # Dependencies (managed by uv)
├── src/
│   ├── infrastructure/
│   │   └── config.py         # Typography and layout settings
│   ├── layout/
│   │   └── notes_models.py   # Pydantic data contracts (Block, Theme, Note)
│   ├── logic/
│   │   └── notes_processor.py # Filesystem scanner and title sanitizer
│   └── workers/
│       └── notes_worker.py    # Core PDF generation logic using fpdf2
└── output/                   # Default output directory
```

## Setup

This project uses `uv` for lightning-fast dependency management.

1. Install dependencies:

   ```bash
   uv sync
   ```

2. (Optional) Ensure Liberation fonts are installed on your system:

   ```bash
   # Ubuntu/Debian
   sudo apt-get install fonts-liberation
   ```

## Usage

Run the generator by pointing it to your notes directory:

```bash
uv run create_notes_pdf.py --notes ./notes --output ./output/philosophy_notes.pdf
```

### CLI Arguments

- `--notes`: Path to the root directory containing your MD files.
- `--output`: Path where the PDF should be saved.
- `--block`: (Optional) Process only a specific block directory by name.

## Configuration

Edit `src/infrastructure/config.py` to customize the look and feel:

- `BASE_FONT_SIZE`: Base size for text.
- `LINE_HEIGHT`: Spacing between lines (standard is usually 5-8).
- `MARGINS`: Adjust margins for printing or digital reading.
- `COLORS`: Change header colors and separator lines.

## How it processes files

1. **Blocks**: Top-level folders (e.g., `Philosophy`).
2. **Themes**: Sub-folders inside blocks.
3. **Notes**: `.md` files.
4. **Sanitization**: Filenames like `01_Subject_Name.md` are automatically cleaned to `Subject Name`.
5. **Numbering**: The tool tracks note indices across the whole block for consistent cross-referencing.
