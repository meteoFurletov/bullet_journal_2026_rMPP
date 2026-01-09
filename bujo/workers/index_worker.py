from pydantic import BaseModel
from src.infrastructure.interfaces import PDFInterface
from bujo.workers.base_worker import BaseWorker
from src.workers.grid_worker import GridInput
from datetime import date, timedelta
import calendar
from typing import List, Tuple, Optional
import bujo.config as config


# --- SECTION A: DATA CONTRACTS ---
class IndexInput(BaseModel):
    start_date: date
    total_weeks: int
    grid_input: GridInput
    month_links: List[Tuple[str, Optional[int]]]  # (name, link_id)
    week_links: List[Tuple[str, Optional[int]]]  # (label, link_id)
    daily_links: List[
        Tuple[str, int, List[Tuple[int, Optional[int]]]]
    ]  # (month_name, year, [(day, link_id)])


class IndexOutput(BaseModel):
    y_start: int
    month_col_w: int
    week_col_w: int
    week_col1_x: int
    week_col2_x: int


# --- SECTION B: PURE LOGIC ---
class IndexLogic:
    def process(self, data: IndexInput) -> IndexOutput:
        # Start below the header
        y_start = config.Y_HEADER_SUBTITLE + config.SIZE_H2 + 40
        margin_left = data.grid_input.toolbar_buffer

        return IndexOutput(
            y_start=int(y_start),
            month_col_w=350,
            week_col_w=450,
            week_col1_x=margin_left + 400,
            week_col2_x=margin_left + 850,
        )


# --- SECTION C: WORKFLOW ---
class IndexWorker(BaseWorker):
    def __init__(self, pdf: PDFInterface):
        super().__init__(pdf)
        self.logic = IndexLogic()

    def draw_months_and_weeks(self, data: IndexInput):
        output = self.logic.process(data)
        self.pdf.add_page()
        self.draw_common_elements(data.grid_input)

        self.draw_instruction_block(
            "Index", "Months & Weeks", None, data.grid_input.toolbar_buffer
        )

        y = output.y_start
        margin_left = data.grid_input.toolbar_buffer

        # Months
        self.pdf.set_font(config.FONT_NAME, "B", size=config.SIZE_INDEX_SECTION_TITLE)
        self.pdf.set_xy(margin_left, y)
        section_h = int(config.SIZE_INDEX_SECTION_TITLE * 1.5)
        self.pdf.cell(0, section_h, "Months")

        self.pdf.set_font(config.FONT_NAME, size=config.SIZE_INDEX_MONTH_NAME)
        y += section_h + 10
        for name, link in data.month_links:
            self.pdf.set_xy(margin_left, y)
            self.pdf.cell(
                output.month_col_w, config.LINE_HEIGHT_INDEX_MONTH, name, link=link
            )
            y += config.LINE_HEIGHT_INDEX_MONTH

        # Weeks
        y = output.y_start
        week_col1_x = output.week_col1_x
        week_col2_x = output.week_col2_x

        self.pdf.set_font(config.FONT_NAME, "B", size=config.SIZE_INDEX_SECTION_TITLE)
        self.pdf.set_xy(week_col1_x, y)
        self.pdf.cell(0, section_h, "Weeks")

        self.pdf.set_font(config.FONT_NAME, size=config.SIZE_INDEX_WEEK_LABEL)
        y += section_h + 10

        half_weeks = (len(data.week_links) + 1) // 2
        for i, (label, link) in enumerate(data.week_links):
            w = i + 1
            if w <= half_weeks:
                curr_x = week_col1_x
                curr_y = y + (w - 1) * config.LINE_HEIGHT_INDEX_WEEK
            else:
                curr_x = week_col2_x
                curr_y = y + (w - half_weeks - 1) * config.LINE_HEIGHT_INDEX_WEEK

            self.pdf.set_xy(curr_x, curr_y)
            self.pdf.cell(
                output.week_col_w, config.LINE_HEIGHT_INDEX_WEEK, label, link=link
            )

    def draw_daily_logs(self, data: IndexInput):
        output = self.logic.process(data)
        self.pdf.add_page()
        self.draw_common_elements(data.grid_input)

        self.draw_instruction_block(
            "Index", "Daily Logs", None, data.grid_input.toolbar_buffer
        )

        y = config.Y_HEADER_SUBTITLE + config.SIZE_H2 + 40
        margin_left = data.grid_input.toolbar_buffer

        for month_name, year, days in data.daily_links:
            # Month Name
            self.pdf.set_font(
                config.FONT_NAME, "B", size=config.SIZE_INDEX_DAILY_LOG_MONTH
            )
            self.pdf.set_xy(margin_left, y)
            self.pdf.cell(0, config.LINE_HEIGHT_INDEX_DAILY_LOG_MONTH, month_name)
            y += config.LINE_HEIGHT_INDEX_DAILY_LOG_MONTH + 5

            # Day Numbers
            self.pdf.set_font(config.FONT_NAME, size=config.SIZE_INDEX_DAILY_LOG_DAY)
            num_x = margin_left
            spacing = (config.CANVAS_WIDTH - margin_left * 2) / 31

            month_num = list(calendar.month_name).index(month_name)

            for day, link in days:
                self.pdf.set_xy(num_x, y)
                self.pdf.cell(
                    spacing,
                    config.LINE_HEIGHT_INDEX_DAILY_LOG_DAY,
                    str(day),
                    align="C",
                    link=link,
                )

                # Draw vertical week separator after Sunday
                try:
                    curr_date = date(year, month_num, day)
                    if curr_date.weekday() == 6:  # Sunday
                        line_x = num_x + spacing
                        self.pdf.set_draw_color(*config.COLOR_DOTS)
                        self.pdf.set_line_width(2.0)
                        self.pdf.line(
                            line_x,
                            y,
                            line_x,
                            y + config.LINE_HEIGHT_INDEX_DAILY_LOG_DAY,
                        )
                except ValueError:
                    pass

                num_x += spacing

            y += config.LINE_HEIGHT_INDEX_DAILY_LOG_DAY + 5
            # Underline
            self.pdf.set_text_color(*config.COLOR_DOTS)
            self.pdf.line(margin_left, y, config.CANVAS_WIDTH - margin_left, y)
            y += 25
            self.pdf.set_text_color(*config.COLOR_TEXT)
