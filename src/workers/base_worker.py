from src.infrastructure.interfaces import PDFInterface
from src.workers.grid_worker import GridWorker, GridInput
import config


class BaseWorker:
    def __init__(self, pdf: PDFInterface):
        self.pdf = pdf
        self.grid_worker = GridWorker(pdf)

    def draw_common_elements(self, grid_input: GridInput):
        # Background
        self.pdf.set_fill_color(*config.COLOR_PAPER)
        self.pdf.rect(0, 0, config.CANVAS_WIDTH, config.CANVAS_HEIGHT, "F")

        # Grid
        grid_output = self.grid_worker.draw_grid(grid_input, config.COLOR_DOTS)
        return grid_output

    def draw_navigation_links(self, links, font_name, start_x, start_y):
        self.pdf.set_font(font_name, size=config.SIZE_NAV_LINKS)
        self.pdf.set_text_color(*config.COLOR_TEXT)

        curr_y = start_y
        for label, link in links:
            if link is not None:
                self.pdf.set_xy(start_x, curr_y)
                self.pdf.cell(0, config.LINE_HEIGHT_NAV_LINKS, f"<- {label}", link=link)
                curr_y += config.LINE_HEIGHT_NAV_LINKS + 10

    def draw_instruction_block(self, title, subtitle, instructions, margin_left):
        # Title
        if title:
            self.pdf.set_font(config.FONT_NAME, "B", size=config.SIZE_INSTRUCT_TITLE)
            self.pdf.set_xy(margin_left, config.Y_HEADER_TITLE)
            self.pdf.set_text_color(*config.COLOR_TEXT)
            self.pdf.cell(0, config.SIZE_INSTRUCT_TITLE, title)

        # Subtitle
        if subtitle:
            self.pdf.set_font(config.FONT_NAME, size=config.SIZE_INSTRUCT_SUBTITLE)
            self.pdf.set_xy(margin_left, config.Y_HEADER_SUBTITLE)
            self.pdf.cell(0, config.SIZE_INSTRUCT_SUBTITLE, subtitle)

        # Instructions (Bottom)
        if instructions:
            self._set_instruction_font()
            self.pdf.set_text_color(*config.COLOR_INSTRUCT)

            line_height = config.LINE_HEIGHT_INSTRUCT_TEXT
            margin = 80
            width = config.CANVAS_WIDTH - margin * 2

            # Calculate height
            lines = self.pdf.multi_cell(
                width - 60,
                line_height,
                instructions,
                dry_run=True,
                output="LINES",
            )
            h = len(lines) * line_height

            y_start = config.CANVAS_HEIGHT - h - 100

            # Draw horizontal line
            self.pdf.set_text_color(*config.COLOR_DOTS)  # Using dot color for line
            self.pdf.line(
                margin, y_start - 20, config.CANVAS_WIDTH - margin, y_start - 20
            )

            # Draw lightning bolt (simple polygon)
            self.pdf.set_fill_color(*config.COLOR_TEXT)
            bx, by = margin, y_start
            self.pdf.polygon(
                [
                    (bx + 10, by),
                    (bx, by + 20),
                    (bx + 8, by + 20),
                    (bx + 2, by + 40),
                    (bx + 15, by + 15),
                    (bx + 7, by + 15),
                    (bx + 12, by),
                ],
                style="F",
            )

            self.pdf.set_xy(margin + 40, y_start)
            self.pdf.multi_cell(width - 40, line_height, instructions, align="L")

        # Reset color
        self.pdf.set_text_color(*config.COLOR_TEXT)

    def _set_instruction_font(self):
        # Try to use Italic if available, else Regular
        try:
            self.pdf.set_font(config.FONT_NAME, "I", size=config.SIZE_INSTRUCT_TEXT)
        except:
            self.pdf.set_font(config.FONT_NAME, "", size=config.SIZE_INSTRUCT_TEXT)
