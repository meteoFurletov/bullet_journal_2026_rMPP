import os
from pydantic import BaseModel
from typing import List, Tuple, Optional
from src.infrastructure.interfaces import PDFInterface
from src.workers.grid_worker import GridInput, GridCalculator
from src.layout.layout_manager import LayoutManager, ToolbarSide
import project_planner.config as config

# --- SECTION A: DATA CONTRACTS ---


class Region(BaseModel):
    x: float
    y: float
    w: float
    h: float


class PlannerInput(BaseModel):
    project_name: str
    canvas_width: int = config.CANVAS_WIDTH
    canvas_height: int = config.CANVAS_HEIGHT
    grid_size: int = config.GRID_SIZE
    right_rail_width: int = config.RIGHT_RAIL_WIDTH


class PlannerOutput(BaseModel):
    right_rail: Region
    nav_buttons: List[Region]  # 10 buttons
    hub_header: Region
    hub_scratchpad: Region
    hub_grid_points: List[Tuple[float, float]]
    map_architecture: Region
    map_arch_grid_points: List[Tuple[float, float]]
    map_tasks: Region
    task_rows: List[Region]
    lab_content: Region
    lab_grid_points: List[Tuple[float, float]]


# --- SECTION B: PURE LOGIC ---


class PlannerLogic:
    def __init__(self, grid_calculator: GridCalculator):
        self.grid_calc = grid_calculator

    def process(self, data: PlannerInput) -> PlannerOutput:
        # Calculate Safe Zone (Usable area horizontally between Toolbar and Right Rail)
        safe_zone = LayoutManager.calculate_safe_zone(
            data.canvas_width,
            data.canvas_height,
            config.TOOLBAR_BUFFER,
            ToolbarSide.LEFT,
        )

        # Right Rail calculation (independent of left toolbar)
        rr_x = data.canvas_width - data.right_rail_width
        right_rail = Region(x=rr_x, y=0, w=data.right_rail_width, h=data.canvas_height)

        button_h = data.canvas_height / 10
        nav_buttons = [
            Region(x=rr_x, y=i * button_h, w=data.right_rail_width, h=button_h)
            for i in range(10)
        ]

        # Content area is between toolbar and right rail
        content_x = safe_zone.x
        main_w = data.canvas_width - config.TOOLBAR_BUFFER - data.right_rail_width

        # Grid area is the full width available (up to the right rail)
        grid_w = data.canvas_width - data.right_rail_width

        hub_header = Region(
            x=content_x, y=0, w=main_w, h=data.canvas_height * config.HUB_HEADER_RATIO
        )
        hub_scratchpad = Region(
            x=content_x,
            y=hub_header.h,
            w=main_w,
            h=data.canvas_height * (1 - config.HUB_HEADER_RATIO),
        )
        # HUB Grid: Full width page
        hub_grid_points = self._get_grid_points(
            Region(x=0, y=0, w=grid_w, h=data.canvas_height),
            data.grid_size,
        )

        map_arch = Region(
            x=content_x, y=0, w=main_w, h=data.canvas_height * config.MAP_ARCH_RATIO
        )
        # MAP Grid: Full width page
        map_arch_grid_points = self._get_grid_points(
            Region(x=0, y=0, w=grid_w, h=data.canvas_height), data.grid_size
        )

        map_tasks = Region(
            x=content_x,
            y=map_arch.h,
            w=main_w,
            h=data.canvas_height * (1 - config.MAP_ARCH_RATIO),
        )
        task_row_h = 75
        num_tasks = int((map_tasks.h - 40) // task_row_h)
        task_rows = [
            Region(
                x=content_x + 40,
                y=map_tasks.y + 40 + i * task_row_h,
                w=main_w - 80,
                h=task_row_h,
            )
            for i in range(num_tasks)
        ]

        lab_content = Region(x=content_x, y=0, w=main_w, h=data.canvas_height)
        # LAB Grid: Full width page
        lab_grid_points = self._get_grid_points(
            Region(x=0, y=0, w=grid_w, h=data.canvas_height), data.grid_size
        )

        return PlannerOutput(
            right_rail=right_rail,
            nav_buttons=nav_buttons,
            hub_header=hub_header,
            hub_scratchpad=hub_scratchpad,
            hub_grid_points=hub_grid_points,
            map_architecture=map_arch,
            map_arch_grid_points=map_arch_grid_points,
            map_tasks=map_tasks,
            task_rows=task_rows,
            lab_content=lab_content,
            lab_grid_points=lab_grid_points,
        )

    def _get_grid_points(
        self, region: Region, grid_size: int
    ) -> List[Tuple[float, float]]:
        g_input = GridInput(
            canvas_width=int(region.w),
            canvas_height=int(region.h),
            grid_size=grid_size,
            toolbar_buffer=0,
            dot_radius=config.DOT_RADIUS,
            align_mode="ABSOLUTE",
            absolute_offset_x=int(region.x),
            absolute_offset_y=int(region.y),
        )
        g_output = self.grid_calc.calculate(g_input)
        points = []
        for x in g_output.x_coords:
            for y in g_output.y_coords:
                points.append((region.x + x, region.y + y))
        return points


# --- SECTION C: WORKFLOW ---


class ProjectPlannerWorker:
    def __init__(self, pdf: PDFInterface):
        self.pdf = pdf
        self.logic = PlannerLogic(GridCalculator())

    def draw_planner(self, data: PlannerInput, page_links: List[int]):
        output = self.logic.process(data)

        # HUB Page: Only navigation links (the background planner.pdf is overlayed in main.py)
        self.pdf.add_page()
        self._draw_base_page(output, page_links, "HUB")

        # MAP Page
        self.pdf.add_page()
        self._draw_base_page(output, page_links, "MAP")
        self._draw_map_content(output, data)

        # LAB Pages
        for i in range(3, 11):
            self.pdf.add_page()
            self._draw_base_page(output, page_links, str(i))
            self._draw_lab_content(output, data)

    def _draw_base_page(
        self, output: PlannerOutput, page_links: List[int], active_label: str
    ):
        # 1. Right Rail Background
        self.pdf.set_fill_color(*config.COLOR_SIDEBAR)
        self.pdf.rect(
            output.right_rail.x,
            output.right_rail.y,
            output.right_rail.w,
            output.right_rail.h,
            "F",
        )

        # 2. Navigation Buttons
        labels = ["HUB", "MAP", "3", "4", "5", "6", "7", "8", "9", "10"]
        for i, button in enumerate(output.nav_buttons):
            if i < len(page_links):
                self.pdf.link(button.x, button.y, button.w, button.h, page_links[i])

            self.pdf.set_text_color(*config.COLOR_TEXT)
            self.pdf.set_font(
                config.FONT_NAME,
                "B" if labels[i] == active_label else "",
                size=config.SIZE_NAV_LINKS,
            )

            text_x = button.x + (button.w / 2) - 30
            text_y = button.y + (button.h / 2) + 10
            self.pdf.set_xy(text_x, text_y)
            self.pdf.cell(60, 0, labels[i], align="C")

            self.pdf.set_draw_color(*config.COLOR_LINE)
            self.pdf.line(
                button.x, button.y + button.h, button.x + button.w, button.y + button.h
            )

    def _draw_grid(self, points: List[Tuple[float, float]]):
        self.pdf.set_fill_color(*config.COLOR_DOTS)
        d = config.DOT_RADIUS * 2
        for px, py in points:
            self.pdf.rect(px - d / 2, py - d / 2, d, d, "F")

    def _draw_hub_content(self, output: PlannerOutput, data: PlannerInput):
        self._draw_grid(output.hub_grid_points)
        self.pdf.set_draw_color(*config.COLOR_LINE)
        self.pdf.set_text_color(*config.COLOR_TEXT)

        # Title
        self.pdf.set_font(config.FONT_NAME, "B", size=config.SIZE_H1)
        self.pdf.set_xy(output.hub_header.x + config.HUB_TITLE_X, config.HUB_TITLE_Y)
        self.pdf.cell(0, 0, data.project_name)

    def _draw_map_content(self, output: PlannerOutput, data: PlannerInput):
        self._draw_grid(output.map_arch_grid_points)
        self.pdf.set_draw_color(*config.COLOR_LINE)
        self.pdf.set_line_width(2)

        # Vertical division: configured offset from the right side
        vertical_divider_x = (
            output.map_architecture.x
            + output.map_architecture.w
            - config.MAP_DIVIDER_OFFSET_X
        )

        # Vertical line dividing architecture (left) from tasks (right)
        self.pdf.line(
            vertical_divider_x,
            0,
            vertical_divider_x,
            data.canvas_height,
        )

        # Titles
        self.pdf.set_text_color(*config.COLOR_TEXT)
        self.pdf.set_font(config.FONT_NAME, "B", size=config.SIZE_H1)

        # Architecture label (left side)
        self.pdf.set_xy(output.map_architecture.x + 40, config.MAP_TITLE_Y)
        self.pdf.cell(0, 0, config.MAP_ARCHITECTURE_TITLE)

        # Tasklist label (right side)
        self.pdf.set_xy(vertical_divider_x + 40, config.MAP_TITLE_Y)
        self.pdf.cell(0, 0, config.MAP_TASKLIST_TITLE)

    def _draw_lab_content(self, output: PlannerOutput, data: PlannerInput):
        self._draw_grid(output.lab_grid_points)
