from pydantic import BaseModel
from enum import Enum
from typing import Optional


class ToolbarSide(str, Enum):
    LEFT = "left"
    RIGHT = "right"
    NONE = "none"


class SafeZone(BaseModel):
    x: float
    y: float
    w: float
    h: float
    toolbar_width: float
    side: ToolbarSide


class LayoutManager:
    """
    Standardizes the 'Safe Zone' for reMarkable devices to avoid overlap
    with system UI (Toolbar).
    """

    @staticmethod
    def calculate_safe_zone(
        canvas_width: float,
        canvas_height: float,
        toolbar_width: float = 120,
        side: ToolbarSide = ToolbarSide.LEFT,
    ) -> SafeZone:
        if side == ToolbarSide.LEFT:
            return SafeZone(
                x=toolbar_width,
                y=0,
                w=canvas_width - toolbar_width,
                h=canvas_height,
                toolbar_width=toolbar_width,
                side=side,
            )
        elif side == ToolbarSide.RIGHT:
            return SafeZone(
                x=0,
                y=0,
                w=canvas_width - toolbar_width,
                h=canvas_height,
                toolbar_width=toolbar_width,
                side=side,
            )
        else:
            return SafeZone(
                x=0,
                y=0,
                w=canvas_width,
                h=canvas_height,
                toolbar_width=0,
                side=ToolbarSide.NONE,
            )
