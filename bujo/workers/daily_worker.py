from pydantic import BaseModel
from src.infrastructure.interfaces import PDFInterface
from bujo.workers.base_worker import BaseWorker
from src.workers.grid_worker import GridInput
from datetime import date
from typing import List, Tuple, Optional
import bujo.config as config


# --- SECTION A: DATA CONTRACTS ---
class DailyInput(BaseModel):
    day_date: date
    nav_links: List[Tuple[str, Optional[int]]]  # (label, link_id)
    grid_input: GridInput


class DailyOutput(BaseModel):
    title_y: int
    subtitle_y: int
    nav_start_x: int
    nav_start_y: int


# --- SECTION B: PURE LOGIC ---
class DailyLogic:
    def process(self, data: DailyInput) -> DailyOutput:
        # Pure math for positioning
        return DailyOutput(
            title_y=config.Y_HEADER_TITLE,
            subtitle_y=config.Y_HEADER_SUBTITLE,
            nav_start_x=config.X_NAV_LINKS_RIGHT,
            nav_start_y=config.Y_NAV_LINKS,
        )


# --- SECTION C: WORKFLOW ---
class DailyWorker(BaseWorker):
    def __init__(self, pdf: PDFInterface):
        super().__init__(pdf)
        self.logic = DailyLogic()

    def draw_page(self, data: DailyInput):
        output = self.logic.process(data)

        self.pdf.add_page()

        # Common elements (Background + Grid)
        self.draw_common_elements(data.grid_input)

        # Header
        self.pdf.set_text_color(*config.COLOR_TEXT)
        self.pdf.set_font(config.FONT_NAME, "B", size=config.SIZE_DAILY_TITLE)
        self.pdf.set_xy(data.grid_input.toolbar_buffer, output.title_y)
        self.pdf.cell(0, config.LINE_HEIGHT_DAILY_TITLE, data.day_date.strftime("%A"))

        self.pdf.set_font(config.FONT_NAME, size=config.SIZE_DAILY_SUBTITLE)
        self.pdf.set_xy(data.grid_input.toolbar_buffer, output.subtitle_y)
        self.pdf.cell(
            0, config.LINE_HEIGHT_DAILY_SUBTITLE, data.day_date.strftime("%B %d")
        )

        # Navigation Links
        self.draw_navigation_links(
            data.nav_links, config.FONT_NAME, output.nav_start_x, output.nav_start_y
        )
