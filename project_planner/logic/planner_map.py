from pydantic import BaseModel
from typing import List
from src.infrastructure.interfaces import PDFInterface


class PlannerMap(BaseModel):
    page_links: List[int] = []


class SpineLogic:
    def __init__(self, pdf: PDFInterface):
        self.pdf = pdf
        self.planner_map = PlannerMap()

    def initialize_links(self, total_pages: int = 10) -> PlannerMap:
        for i in range(1, total_pages + 1):
            link_id = self.pdf.add_link()
            self.pdf.set_link(link_id, page=i)
            self.planner_map.page_links.append(link_id)
        return self.planner_map
