from pydantic import BaseModel
from src.infrastructure.interfaces import PDFInterface
from typing import List


# --- SECTION A: DATA CONTRACTS ---
class GridInput(BaseModel):
    canvas_width: int
    canvas_height: int
    grid_size: int
    toolbar_buffer: int
    dot_radius: int


class GridOutput(BaseModel):
    x_coords: List[int]
    y_coords: List[int]
    margin_left: int
    margin_top: int
    num_cols: int
    num_rows: int
    dot_size: int


# --- SECTION B: PURE LOGIC ---
class GridCalculator:
    def calculate(self, data: GridInput) -> GridOutput:
        # 1. Available Space (Horizontal) - Grid is centered on FULL canvas
        available_w = data.canvas_width

        # 2. Grid Columns (Integer Division)
        num_cols = available_w // data.grid_size
        grid_w = num_cols * data.grid_size

        # 3. Margins (Center the grid in the available space)
        remaining_w = available_w - grid_w
        margin_left = remaining_w // 2

        # Vertical calculation
        available_h = data.canvas_height
        num_rows = available_h // data.grid_size
        grid_h = num_rows * data.grid_size
        remaining_h = data.canvas_height - grid_h
        margin_top = remaining_h // 2

        x_coords = [margin_left + (i * data.grid_size) for i in range(num_cols + 1)]
        y_coords = [margin_top + (j * data.grid_size) for j in range(num_rows + 1)]

        return GridOutput(
            x_coords=x_coords,
            y_coords=y_coords,
            margin_left=margin_left,
            margin_top=margin_top,
            num_cols=num_cols + 1,
            num_rows=num_rows + 1,
            dot_size=data.dot_radius * 2,
        )


# --- SECTION C: WORKFLOW ---
class GridWorker:
    def __init__(self, pdf: PDFInterface):
        self.pdf = pdf
        self.logic = GridCalculator()

    def draw_grid(self, data: GridInput, color_dots: tuple):
        output = self.logic.calculate(data)

        self.pdf.set_fill_color(*color_dots)
        d = output.dot_size

        for x in output.x_coords:
            for y in output.y_coords:
                # Center the dot on the coordinate
                self.pdf.rect(x - d / 2, y - d / 2, d, d, "F")

        return output
