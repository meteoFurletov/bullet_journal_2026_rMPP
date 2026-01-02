from datetime import date, timedelta
from pydantic import BaseModel
from typing import Dict, List, Tuple, Optional


class JournalMap(BaseModel):
    # (year, month, day) -> link_id
    day_links: Dict[Tuple[int, int, int], int] = {}
    # (year, month) -> link_id (Timeline)
    month_timeline_links: Dict[Tuple[int, int], int] = {}
    # (year, month) -> link_id (Action Plan)
    month_action_links: Dict[Tuple[int, int], int] = {}
    # week_num -> link_id (Action Plan)
    week_action_links: Dict[int, int] = {}
    # week_num -> link_id (Reflection)
    week_reflection_links: Dict[int, int] = {}
    # Special pages
    index_link: int = 0


class NavigationSpine:
    def __init__(self, pdf_interface):
        self.pdf = pdf_interface
        self.journal_map = JournalMap()

    def initialize_links(self, start_date: date, total_weeks: int, target_year: int):
        # Pass 1: Calculate Page Numbers and Create Links

        current_page = 1

        # Index (2 pages)
        self.journal_map.index_link = self.pdf.add_link()
        self.pdf.set_link(self.journal_map.index_link, page=current_page)
        current_page += 2

        current_date = start_date
        unique_months = []
        for i in range(total_weeks):
            d = start_date + timedelta(weeks=i)
            if d.year < target_year:
                continue
            m_key = (d.year, d.month)
            if m_key not in unique_months:
                unique_months.append(m_key)

        # We need to simulate the loop to get exact page numbers
        month_idx = 0
        last_month_key = None

        for week_num in range(1, total_weeks + 1):
            monday = start_date + timedelta(weeks=week_num - 1)
            m_key = (monday.year, monday.month)

            if m_key != last_month_key and m_key in unique_months:
                # Monthly Timeline
                self.journal_map.month_timeline_links[m_key] = self.pdf.add_link()
                self.pdf.set_link(
                    self.journal_map.month_timeline_links[m_key], page=current_page
                )
                current_page += 1

                # Monthly Action Plan
                self.journal_map.month_action_links[m_key] = self.pdf.add_link()
                self.pdf.set_link(
                    self.journal_map.month_action_links[m_key], page=current_page
                )
                current_page += 1

                last_month_key = m_key

            # Weekly Action Plan
            self.journal_map.week_action_links[week_num] = self.pdf.add_link()
            self.pdf.set_link(
                self.journal_map.week_action_links[week_num], page=current_page
            )
            current_page += 1

            # Daily Pages
            for day_offset in range(7):
                day_date = monday + timedelta(days=day_offset)
                d_key = (day_date.year, day_date.month, day_date.day)
                self.journal_map.day_links[d_key] = self.pdf.add_link()
                self.pdf.set_link(self.journal_map.day_links[d_key], page=current_page)
                current_page += 1

            # Weekly Reflection
            self.journal_map.week_reflection_links[week_num] = self.pdf.add_link()
            self.pdf.set_link(
                self.journal_map.week_reflection_links[week_num], page=current_page
            )
            current_page += 1

        return self.journal_map
