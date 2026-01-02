from pydantic import BaseModel
from src.infrastructure.interfaces import PDFInterface
from src.workers.base_worker import BaseWorker
from src.workers.grid_worker import GridInput
from typing import List, Tuple, Optional
import config


# --- SECTION A: DATA CONTRACTS ---
class WeeklyInput(BaseModel):
    date_str: str
    nav_links: List[Tuple[str, Optional[int]]]
    grid_input: GridInput
    instructions: str


class WeeklyOutput(BaseModel):
    nav_start_x: int
    nav_start_y: int


# --- SECTION B: PURE LOGIC ---
class WeeklyLogic:
    def process(self, data: WeeklyInput) -> WeeklyOutput:
        return WeeklyOutput(
            nav_start_x=config.X_NAV_LINKS_RIGHT, nav_start_y=config.Y_NAV_LINKS
        )


# --- SECTION C: WORKFLOW ---
class WeeklyWorker(BaseWorker):
    def __init__(self, pdf: PDFInterface):
        super().__init__(pdf)
        self.logic = WeeklyLogic()

    def draw_action_plan(self, data: WeeklyInput):
        output = self.logic.process(data)
        self.pdf.add_page()
        self.draw_common_elements(data.grid_input)

        self.draw_instruction_block(
            title="Action Plan: Week",
            subtitle=data.date_str,
            instructions=data.instructions,
            margin_left=data.grid_input.toolbar_buffer,
        )

        self.draw_navigation_links(
            data.nav_links, config.FONT_NAME, output.nav_start_x, output.nav_start_y
        )

    def draw_reflection(self, data: WeeklyInput):
        output = self.logic.process(data)
        self.pdf.add_page()
        self.draw_common_elements(data.grid_input)

        self.draw_instruction_block(
            title="Reflection: Week",
            subtitle=None,
            instructions=data.instructions,
            margin_left=data.grid_input.toolbar_buffer,
        )

        self.draw_navigation_links(
            data.nav_links, config.FONT_NAME, output.nav_start_x, output.nav_start_y
        )
