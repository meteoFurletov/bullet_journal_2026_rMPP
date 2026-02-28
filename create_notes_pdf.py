import argparse
import sys
import os
from src.logic.notes_processor import NotesProcessor
from src.workers.notes_worker import NotesWorker


def main():
    parser = argparse.ArgumentParser(description="Generate PDF from Markdown Notes")
    parser.add_argument(
        "--notes_dir",
        default="../postgrad_intro_exams/Notes",
        help="Path to Notes directory",
    )
    parser.add_argument(
        "--output", default="output/notes_compilation.pdf", help="Output PDF path"
    )
    parser.add_argument("--block", help="Specific block to process (substring match)")

    args = parser.parse_args()

    notes_dir = os.path.abspath(args.notes_dir)
    if not os.path.isdir(notes_dir):
        print(f"Error: Notes directory not found: {notes_dir}")
        # Fallback to local notes if external not found (e.g. for testing)
        local_notes = os.path.abspath("notes")
        if os.path.isdir(local_notes):
            print(f"Falling back to local notes: {local_notes}")
            notes_dir = local_notes
        else:
            sys.exit(1)

    print(f"Scanning {notes_dir}...")
    processor = NotesProcessor(notes_dir)
    blocks = processor.load_structure()

    if not blocks:
        print(
            "No blocks found. Ensure directory structure matches 'Block X/Theme Y/Note.md' or similar."
        )
        sys.exit(1)

    # Filtering
    if args.block:
        filtered_blocks = [b for b in blocks if args.block in b.title]
        if not filtered_blocks:
            print(f"No blocks found matching '{args.block}'")
            sys.exit(1)
        blocks = filtered_blocks

    print(f"Found {len(blocks)} blocks to process:")
    for b in blocks:
        t_count = sum(len(t.notes) for t in b.themes)
        print(
            f" - {b.title}: {len(b.themes)} themes ({t_count} notes), {len(b.direct_notes)} direct notes"
        )

    print(f"Generating PDF to {args.output}...")
    worker = NotesWorker()
    worker.generate(blocks, args.output)


if __name__ == "__main__":
    main()
