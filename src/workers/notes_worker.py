from fpdf import FPDF
from fpdf.fonts import FontFace
from src.layout.notes_models import Block, Theme, Note
from src.infrastructure import config
from typing import List
import os
import re
import markdown


class NotesPDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass


class NotesWorker:
    def __init__(self):
        self.pdf = NotesPDF()
        self.font_name = config.FONT_NAME
        self.note_idx = 0

        # Configure Heading Styles
        # Restoration of distinct, bold heading sizes
        self.tag_styles = {
            "h1": FontFace(
                emphasis="B",
                size_pt=24,
                color=(0, 0, 0),
            ),
            "h2": FontFace(
                emphasis="B",
                size_pt=20,
                color=(0, 0, 0),
            ),
            "h3": FontFace(
                emphasis="B",
                size_pt=18,
                color=(0, 0, 0),
            ),
            "h4": FontFace(
                emphasis="B",
                size_pt=16,
                color=(0, 0, 0),
            ),
        }

    def generate(self, blocks: List[Block], output_path: str):
        if not blocks:
            print("No blocks to generate.")
            return

        # Start PDF setup
        self._setup_pdf(self.pdf)
        self.note_idx = 0

        # 1. Title Page
        self.pdf.add_page()
        self.pdf.set_font(self.font_name, "B", 36)
        self.pdf.ln(80)
        self.pdf.multi_cell(self.pdf.epw, 20, "Philosophy & Science", align="C")
        self.pdf.set_font(self.font_name, "", 18)
        self.pdf.multi_cell(self.pdf.epw, 10, "Bullet Journal Compilation", align="C")

        # 2. Content (TOC removed as requested)
        for block in blocks:
            self._render_block(block)

        # Create output directory and save
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.pdf.output(output_path)
        print(f"PDF generated: {output_path}")

    def _setup_pdf(self, pdf):
        pdf.set_left_margin(config.MARGIN_LEFT)
        pdf.set_right_margin(config.MARGIN_RIGHT)
        pdf.set_top_margin(config.MARGIN_TOP)
        pdf.set_auto_page_break(auto=True, margin=config.MARGIN_BOTTOM)

        if os.path.exists(config.FONT_REGULAR):
            pdf.add_font(self.font_name, "", config.FONT_REGULAR)
            pdf.add_font(self.font_name, "B", config.FONT_BOLD)
            pdf.add_font(self.font_name, "I", config.FONT_ITALIC)
            pdf.add_font(self.font_name, "BI", config.FONT_BOLD_ITALIC)
            pdf.set_font(self.font_name, size=config.BASE_FONT_SIZE)

    def _render_block(self, block: Block):
        # Check for page break if we aren't at the top
        if self.pdf.get_y() > config.MARGIN_TOP + 10:
            if self.pdf.get_y() > (self.pdf.page_break_trigger - 40):
                self.pdf.add_page()
            else:
                self.pdf.ln(10)

        self.pdf.start_section(block.title, level=0)

        # Block Title
        self.pdf.set_font(self.font_name, "B", 26)
        self.pdf.set_text_color(*config.COLOR_HEADER)
        self.pdf.multi_cell(self.pdf.epw, 15, block.title, align="C")
        self.pdf.ln(5)
        self.pdf.set_font(self.font_name, "", config.BASE_FONT_SIZE)
        self.pdf.set_text_color(0, 0, 0)

        # Direct Notes
        for note in block.direct_notes:
            self._render_note(note, level=1)

        # Themes
        for theme in block.themes:
            self._render_theme(theme)

    def _render_theme(self, theme: Theme):
        # Theme Title - Flowing instead of new page
        if self.pdf.get_y() > (self.pdf.page_break_trigger - 30):
            self.pdf.add_page()
        else:
            self.pdf.ln(5)

        self.pdf.set_font(self.font_name, "B", 22)
        self.pdf.set_text_color(*config.COLOR_HEADER)
        self.pdf.start_section(theme.title, level=1)
        self.pdf.multi_cell(self.pdf.epw, 12, theme.title)
        self.pdf.ln(3)
        self.pdf.set_font(self.font_name, "", config.BASE_FONT_SIZE)
        self.pdf.set_text_color(0, 0, 0)

        if theme.intro_note:
            self._render_note_content(theme.intro_note)

        for note in theme.notes:
            self._render_note(note, level=2)

    def _render_note(self, note: Note, level=2):
        self.note_idx += 1
        prefix = f"{self.note_idx}"

        # Extract title from H1 if present
        match = re.search(r"^#\s+(.*)", note.content.strip(), re.MULTILINE)
        raw_title = match.group(1).strip() if match else note.title
        display_title = f"{prefix}. {raw_title}"

        self.pdf.start_section(display_title, level=level)

        # Check for page break - reduced buffer for more compact flow
        if self.pdf.get_y() > (self.pdf.page_break_trigger - 25):
            self.pdf.add_page()
        else:
            self.pdf.ln(config.SEPARATOR_SPACE)
            self.pdf.set_draw_color(*config.COLOR_SEPARATOR)
            self.pdf.line(
                self.pdf.l_margin,
                self.pdf.get_y(),
                self.pdf.w - self.pdf.r_margin,
                self.pdf.get_y(),
            )
            self.pdf.ln(config.SEPARATOR_SPACE)

        # Demote internal headers by 1 to make them H2, H3 etc.
        self._render_note_content(note, demote_by=1, prefix=prefix)

    def _render_note_content(self, note: Note, demote_by=0, prefix=""):
        text = note.content

        # 1. Numbering and Demoting Headers
        processed_lines = []
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("#"):
                match = re.match(r"(#+)\s*(.*)", stripped)
                if match:
                    hashes, title = match.groups()
                    original_lvl = len(hashes)

                    if original_lvl == 1 and prefix:
                        if not re.match(r"^\d+\.", title):
                            title = f"{prefix}. {title}"
                    elif original_lvl == 2 and prefix:
                        sub_match = re.match(r"(\d+)\.\s*(.*)", title)
                        if sub_match:
                            num, rest = sub_match.groups()
                            title = f"{prefix}.{num}. {rest}"

                    line = "#" * (original_lvl + demote_by) + " " + title
            processed_lines.append(line)

        text = "\n".join(processed_lines)

        # 2. Convert to HTML and Render
        try:
            html_text = markdown.markdown(text)
            html_text = html_text.replace("<pre>", "").replace("</pre>", "")
            html_text = html_text.replace("<code>", "").replace("</code>", "")

            self.pdf.write_html(html_text, tag_styles=self.tag_styles)
        except Exception as e:
            print(f"Error rendering markdown for {note.title}: {e}")
            self.pdf.set_font(self.font_name, "", config.BASE_FONT_SIZE)
            self.pdf.multi_cell(self.pdf.epw, config.LINE_HEIGHT, text)
