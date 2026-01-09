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
    align_mode: str = "CENTER"
    absolute_offset_x: int = 0
    absolute_offset_y: int = 0


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
        # 1. Available Space (Horizontal)
        # We use the full provided canvas width
        available_w = data.canvas_width

        if data.align_mode == "ABSOLUTE":
            # Global Alignment
            # Find first global grid line >= absolute_offset_x
            # P_global = k * grid_size
            # P_global >= absolute_offset_x
            start_k_x = (
                data.absolute_offset_x + data.grid_size - 1
            ) // data.grid_size  # ceil
            if (
                start_k_x * data.grid_size < data.absolute_offset_x
            ):  # Check just in case
                start_k_x += 1

            # Since we want coordinates relative to the start of the region (which is at absolute_offset_x),
            # but usually GridCalculator returns coordinates relative to 0 (canvas start).
            # Here 'canvas_width' is the width of the region.
            # So actual global pixel is absolute_offset_x + local_x.
            # We want absolute_offset_x + local_x = k * grid_size.
            # local_x = k * grid_size - absolute_offset_x.

            # Start loop k from start_k_x
            x_coords = []
            k = start_k_x
            while True:
                pos = k * data.grid_size - data.absolute_offset_x
                if pos > available_w:
                    break
                if (
                    pos >= 0
                ):  # Should be true by definition of start_k_x but good to be safe
                    x_coords.append(pos)
                k += 1

            margin_left = x_coords[0] if x_coords else 0
            num_cols = len(x_coords)

        else:
            # 2. Grid Columns (Integer Division)
            num_cols_div = available_w // data.grid_size
            grid_w = num_cols_div * data.grid_size

            # 3. Margins (Center the grid in the available space)
            remaining_w = available_w - grid_w
            margin_left = remaining_w // 2

            x_coords = [
                margin_left + (i * data.grid_size) for i in range(num_cols_div + 1)
            ]
            num_cols = len(x_coords)

        # Vertical calculation
        available_h = data.canvas_height

        if data.align_mode == "ABSOLUTE":
            start_k_y = (data.absolute_offset_y + data.grid_size - 1) // data.grid_size

            y_coords = []
            k = start_k_y
            while True:
                pos = k * data.grid_size - data.absolute_offset_y
                if pos > available_h:
                    break
                if pos >= 0:
                    y_coords.append(pos)
                k += 1

            margin_top = y_coords[0] if y_coords else 0
            num_rows = len(y_coords)

        else:
            num_rows_div = available_h // data.grid_size
            grid_h = num_rows_div * data.grid_size
            remaining_h = data.canvas_height - grid_h
            margin_top = remaining_h // 2

            y_coords = [
                margin_top + (j * data.grid_size) for j in range(num_rows_div + 1)
            ]
            num_rows = len(y_coords)

        return GridOutput(
            x_coords=x_coords,
            y_coords=y_coords,
            margin_left=margin_left,
            margin_top=margin_top,
            num_cols=num_cols,
            num_rows=num_rows,
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
