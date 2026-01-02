from pydantic import BaseModel
from src.infrastructure.interfaces import PDFInterface
from src.workers.base_worker import BaseWorker
from src.workers.grid_worker import GridInput
from datetime import date
from typing import List, Tuple, Optional
import config


# --- SECTION A: DATA CONTRACTS ---
class MonthlyInput(BaseModel):
    month_name: str
    month: int
    year: int
    days_in_month: int
    instructions: str
    nav_links: List[Tuple[str, Optional[int]]]
    grid_input: GridInput
    day_links: List[int]  # List of link IDs for each day


class MonthlyOutput(BaseModel):
    nav_start_x: int
    nav_start_y: int
    timeline_start_row: int
    v_adjust: float


# --- SECTION B: PURE LOGIC ---
class MonthlyLogic:
    def process(self, data: MonthlyInput) -> MonthlyOutput:
        # Calculate row that clears the header
        header_end_y = config.Y_HEADER_SUBTITLE + config.SIZE_H2
        start_row = (header_end_y // config.GRID_SIZE) + 2

        return MonthlyOutput(
            nav_start_x=config.X_NAV_LINKS_RIGHT,
            nav_start_y=config.Y_NAV_LINKS,
            timeline_start_row=int(start_row),
            v_adjust=1.0,
        )


# --- SECTION C: WORKFLOW ---
class MonthlyWorker(BaseWorker):
    def __init__(self, pdf: PDFInterface):
        super().__init__(pdf)
        self.logic = MonthlyLogic()

    def draw_timeline(self, data: MonthlyInput):
        output = self.logic.process(data)
        self.pdf.add_page()
        grid_output = self.draw_common_elements(data.grid_input)

        # Days
        self.pdf.set_font(config.FONT_NAME, size=config.SIZE_MONTHLY_TIMELINE_DAY)

        # Find the first dot column that respects the toolbar buffer
        num_x = next(
            x for x in grid_output.x_coords if x >= data.grid_input.toolbar_buffer
        )

        for day in range(1, data.days_in_month + 1):
            row = output.timeline_start_row + (day - 1)
            if row >= len(grid_output.y_coords):
                break
            y_dot = grid_output.y_coords[row]

            link_id = data.day_links[day - 1]

            day_w = int(config.SIZE_MONTHLY_TIMELINE_DAY * 1.8)
            self.pdf.set_xy(
                num_x - day_w + config.MONTHLY_TIMELINE_X_OFFSET,
                y_dot
                - (config.GRID_SIZE / 2)
                + output.v_adjust
                + config.MONTHLY_TIMELINE_Y_OFFSET,
            )
            self.pdf.cell(day_w, config.GRID_SIZE, str(day), align="C", link=link_id)

            # Draw week separator line if it's Sunday
            current_date = date(data.year, data.month, day)
            if current_date.weekday() == 6:  # Sunday
                line_y = (
                    y_dot
                    + (config.GRID_SIZE / 2)
                    + config.MONTHLY_TIMELINE_Y_OFFSET
                    - 4
                )
                self.pdf.set_draw_color(*config.COLOR_DOTS)
                self.pdf.set_line_width(2.0)
                self.pdf.line(
                    data.grid_input.toolbar_buffer,
                    line_y,
                    config.CANVAS_WIDTH - data.grid_input.toolbar_buffer,
                    line_y,
                )

        self.draw_instruction_block(
            "Monthly Log",
            data.month_name,
            data.instructions,
            data.grid_input.toolbar_buffer,
        )
        self.draw_navigation_links(
            data.nav_links, config.FONT_NAME, output.nav_start_x, output.nav_start_y
        )

    def draw_action_plan(self, data: MonthlyInput):
        output = self.logic.process(data)
        self.pdf.add_page()
        self.draw_common_elements(data.grid_input)

        self.draw_instruction_block(
            "Monthly Action Plan",
            data.month_name,
            data.instructions,
            data.grid_input.toolbar_buffer,
        )
        self.draw_navigation_links(
            data.nav_links, config.FONT_NAME, output.nav_start_x, output.nav_start_y
        )
