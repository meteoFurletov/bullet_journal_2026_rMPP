from fpdf import FPDF
from datetime import date, timedelta
import os
import calendar

# --- Configuration ---
PDF_W = 1620  # 22.50 inches * 72 pt/in
PDF_H = 2160  # 30.00 inches * 72 pt/in

# Scale factor relative to original 1696 height (to ensure vertical fit)
SCALE = PDF_H / 1696.0

# Layout
MARGIN_LEFT = 70 * SCALE  # Added offset for Remarkable tools
MARGIN_TOP = 80 * SCALE

# Dot Grid Settings: Exactly 34x47 dots
# We calculate spacing to fit 47 dots vertically within the margins
GRID_SPACING = (PDF_H - 2 * MARGIN_TOP) / 46
DOT_SIZE = 1.2 * SCALE

# Colors (R, G, B)
COLOR_PAPER = (252, 252, 250)
COLOR_DOTS = (100, 100, 100)
COLOR_TEXT = (40, 40, 40)
COLOR_INSTRUCT = (100, 100, 100)

# --- Font Configuration ---
# Standard Google Fonts Structure:
# main.py
# static/
#   Dosis-Regular.ttf
#   Dosis-Bold.ttf

FONT_NAME = "Dosis"
FONT_DIR = "fonts/Dosis/static"  # Matches the folder name from the Google Fonts zip

# Use os.path.join to handle folder paths correctly
FONT_REGULAR = os.path.join(FONT_DIR, "Dosis-Regular.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "Dosis-Bold.ttf")
FONT_ITALIC = os.path.join(FONT_DIR, "Dosis-Italic.ttf")


class BulletJournal(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.day_links = {}
        self.month_links = {}  # (year, month) -> link_id
        self.week_links = {}  # week_num -> link_id

    def get_day_link(self, year, month, day):
        key = (year, month, day)
        if key not in self.day_links:
            self.day_links[key] = self.add_link()
        return self.day_links[key]

    def get_month_link(self, year, month):
        key = (year, month)
        if key not in self.month_links:
            self.month_links[key] = self.add_link()
        return self.month_links[key]

    def get_week_link(self, week_num):
        if week_num not in self.week_links:
            self.week_links[week_num] = self.add_link()
        return self.week_links[week_num]

    def header(self):
        pass

    def draw_background(self):
        self.set_fill_color(*COLOR_PAPER)
        self.rect(0, 0, PDF_W, PDF_H, "F")

    def draw_dot_grid(self):
        self.set_fill_color(*COLOR_DOTS)

        num_cols = 34
        num_rows = 47

        # Calculate grid dimensions
        grid_w = (num_cols - 1) * GRID_SPACING
        grid_h = (num_rows - 1) * GRID_SPACING

        # Center the grid on the page
        self.grid_offset_x = (PDF_W - grid_w) / 2
        self.grid_offset_y = (PDF_H - grid_h) / 2

        # Optimization: Use rect instead of circle for dots
        d = DOT_SIZE
        for i in range(num_cols):
            x = self.grid_offset_x + (i * GRID_SPACING) - (d / 2)
            for j in range(num_rows):
                y = self.grid_offset_y + (j * GRID_SPACING) - (d / 2)
                self.rect(x, y, d, d, "F")

    def draw_instruction_block(self, title, date_subtitle, instructions):
        # Title
        if title:
            self.set_font(self.active_font, "B", size=60 * SCALE)
            self.set_xy(MARGIN_LEFT, 80 * SCALE)
            self.set_text_color(*COLOR_TEXT)
            self.cell(0, 0, title)

        # Date Subtitle
        if date_subtitle:
            self.set_font(self.active_font, size=36 * SCALE)
            self.set_xy(MARGIN_LEFT, 140 * SCALE)
            self.cell(0, 0, date_subtitle)

        # Instructions (Bottom)
        if instructions:
            style = "I" if self.has_italic else ""
            self.set_font(self.active_font, style, size=20 * SCALE)
            self.set_text_color(*COLOR_INSTRUCT)

            line_height = 28 * SCALE
            margin = 80 * SCALE
            width = PDF_W - margin * 2

            # Calculate height by splitting text into lines
            lines = self.multi_cell(
                width - 60 * SCALE,
                line_height,
                instructions,
                dry_run=True,
                output="LINES",
            )
            h = len(lines) * line_height

            y_start = PDF_H - h - 100 * SCALE

            # Draw horizontal line
            self.set_draw_color(*COLOR_DOTS)
            self.line(
                margin, y_start - 20 * SCALE, PDF_W - margin, y_start - 20 * SCALE
            )

            # Draw lightning bolt (simple polygon)
            self.set_fill_color(*COLOR_TEXT)
            bx, by = margin, y_start
            self.polygon(
                [
                    (bx + 10 * SCALE, by),
                    (bx, by + 20 * SCALE),
                    (bx + 8 * SCALE, by + 20 * SCALE),
                    (bx + 2 * SCALE, by + 40 * SCALE),
                    (bx + 15 * SCALE, by + 15 * SCALE),
                    (bx + 7 * SCALE, by + 15 * SCALE),
                    (bx + 12 * SCALE, by),
                ],
                style="F",
            )

            self.set_xy(margin + 40 * SCALE, y_start)
            self.multi_cell(width - 40 * SCALE, line_height, instructions, align="L")

        # Reset color
        self.set_text_color(*COLOR_TEXT)

    def draw_navigation_links(self, links):
        """
        Draws a list of navigation links in the style of '<- Text'.
        links: List of tuples (label, link_id)
        """
        self.set_font(self.active_font, size=24 * SCALE)
        self.set_text_color(*COLOR_TEXT)

        # Position in the top right area, but aligned to the left of the block
        start_x = PDF_W - 280 * SCALE
        start_y = 60 * SCALE

        for label, link in links:
            if link is None:
                continue
            self.set_xy(start_x, start_y)
            # Using <- for the arrow style as requested
            self.cell(0, 30 * SCALE, f"<- {label}", link=link)
            start_y += 40 * SCALE

    def link_to_page(self, page_no):
        """Helper to create a link to a specific page number."""
        if page_no is None or page_no <= 0:
            return None
        link = self.add_link()
        self.set_link(link, page=page_no)
        return link

    def draw_timeline(
        self, month_name, month, year, days_in_month, instructions, nav_links
    ):
        self.add_page()
        self.draw_background()
        self.draw_dot_grid()

        # Use the centered grid offsets
        offset_y = self.grid_offset_y
        offset_x = self.grid_offset_x

        # Start row (tuned to fit title and instructions)
        # We want to start around 300pt down
        start_row = int(300 * SCALE / GRID_SPACING)

        # Days
        font_size = int(GRID_SPACING * 0.7)
        self.set_font(self.active_font, size=font_size)

        # --- PRECISION TUNING ---
        V_ADJUST = 1.0
        # ------------------------

        # Align numbers to the first column of dots
        num_x = offset_x

        for day in range(1, days_in_month + 1):
            row = start_row + (day - 1)
            y_dot = offset_y + (row * GRID_SPACING)

            link_id = self.get_day_link(year, month, day)

            # We center a cell of height GRID_SPACING on the dot.
            # The top of the cell is y_dot - (GRID_SPACING / 2).
            self.set_xy(num_x - 70 * SCALE, y_dot - (GRID_SPACING / 2) + V_ADJUST)
            self.cell(60 * SCALE, GRID_SPACING, str(day), align="R", link=link_id)

        self.draw_navigation_links(nav_links)
        self.draw_instruction_block("Monthly Log", month_name, instructions)

    def draw_monthly_action_plan(self, month_name, instructions, nav_links):
        self.add_page()
        self.draw_background()
        self.draw_dot_grid()

        self.draw_instruction_block("Monthly Action Plan", month_name, instructions)
        self.draw_navigation_links(nav_links)

    def draw_index_content(self, start_date, total_weeks, index_page_idx):
        # Page 1: Months and Weeks
        self.page = index_page_idx
        self.draw_instruction_block("Index", "Months & Weeks", None)

        y_start = 200 * SCALE

        # --- Months (Left Column) ---
        self.set_font(self.active_font, "B", size=30 * SCALE)
        self.set_xy(MARGIN_LEFT, y_start)
        self.cell(0, 40 * SCALE, "Months")

        self.set_font(self.active_font, size=24 * SCALE)
        y = y_start + 50 * SCALE

        unique_months = []
        # Determine the target year (the year the journal is primarily for)
        actual_target_year = (
            start_date.year if start_date.month == 1 else start_date.year + 1
        )
        for i in range(total_weeks):
            d = start_date + timedelta(weeks=i)
            if d.year < actual_target_year:
                continue
            m_key = (d.year, d.month)
            if m_key not in unique_months:
                unique_months.append(m_key)

        for year, month in unique_months:
            month_name = calendar.month_name[month]
            link = self.get_month_link(year, month)
            self.set_xy(MARGIN_LEFT, y)
            self.cell(200 * SCALE, 35 * SCALE, month_name, link=link)
            y += 35 * SCALE

        # --- Weeks (Two Columns) ---
        self.set_font(self.active_font, "B", size=30 * SCALE)
        week_col1_x = MARGIN_LEFT + 250 * SCALE
        week_col2_x = MARGIN_LEFT + 550 * SCALE
        self.set_xy(week_col1_x, y_start)
        self.cell(0, 40 * SCALE, "Weeks")

        self.set_font(self.active_font, size=18 * SCALE)
        y = y_start + 50 * SCALE

        half_weeks = (total_weeks + 1) // 2
        for w in range(1, total_weeks + 1):
            monday = start_date + timedelta(weeks=w - 1)
            sunday = monday + timedelta(days=6)
            label = f"W{w}: {monday.strftime('%b %d')} - {sunday.strftime('%b %d')}"
            link = self.get_week_link(w)

            if w <= half_weeks:
                curr_x = week_col1_x
                curr_y = y + (w - 1) * 28 * SCALE
            else:
                curr_x = week_col2_x
                curr_y = y + (w - half_weeks - 1) * 28 * SCALE

            self.set_xy(curr_x, curr_y)
            self.cell(280 * SCALE, 25 * SCALE, label, link=link)

        # Page 2: Daily Logs (Horizontal Layout)
        self.page = index_page_idx + 1
        self.draw_instruction_block("Index", "Daily Logs", None)

        y = 220 * SCALE

        # We want to show Jan to Dec for the target year
        target_year = start_date.year
        # If start_date is late Dec, target_year might be the next one
        if start_date.month == 12 and start_date.day > 20:
            target_year = start_date.year + 1

        for month in range(1, 13):
            month_name = calendar.month_name[month]
            days_in_month = calendar.monthrange(target_year, month)[1]

            # Month Name
            self.set_font(self.active_font, "B", size=24 * SCALE)
            self.set_xy(MARGIN_LEFT, y)
            self.cell(0, 30 * SCALE, month_name)
            y += 32 * SCALE

            # Day Numbers
            self.set_font(self.active_font, size=16 * SCALE)
            num_x = MARGIN_LEFT
            spacing = (PDF_W - MARGIN_LEFT * 2) / 31

            for day in range(1, days_in_month + 1):
                link = self.get_day_link(target_year, month, day)
                self.set_xy(num_x, y)
                self.cell(spacing, 25 * SCALE, str(day), align="C", link=link)
                num_x += spacing

            y += 28 * SCALE
            # Underline
            self.set_draw_color(*COLOR_DOTS)
            self.line(MARGIN_LEFT, y, PDF_W - MARGIN_LEFT, y)
            y += 35 * SCALE


# 1. Setup PDF
pdf = BulletJournal(orientation="P", unit="pt", format=(PDF_W, PDF_H))
pdf.set_auto_page_break(False)

# --- Smart Font Loading ---
pdf.active_font = "Helvetica"
pdf.has_italic = True

# Check if the static folder exists
if not os.path.exists(FONT_DIR):
    print(
        f"Warning: Folder '{FONT_DIR}' not found. Please create it or unzip your fonts there."
    )

# Try to load fonts from the static directory
if os.path.exists(FONT_REGULAR) and os.path.exists(FONT_BOLD):
    try:
        # uni=True is deprecated in newer fpdf2 versions
        pdf.add_font(FONT_NAME, "", FONT_REGULAR)
        pdf.add_font(FONT_NAME, "B", FONT_BOLD)

        # Check for Italic
        if os.path.exists(FONT_ITALIC):
            pdf.add_font(FONT_NAME, "I", FONT_ITALIC)
            pdf.has_italic = True
        else:
            pdf.has_italic = False

        pdf.active_font = FONT_NAME
        print(f"Success: Using custom font {FONT_REGULAR}")
    except Exception as e:
        print(f"Error loading font: {e}. Falling back to Helvetica.")
else:
    print(f"Font file '{FONT_REGULAR}' not found. Using Helvetica.")


# 2. Date Logic
target_year = 2026
jan_one = date(target_year, 1, 1)
start_date = jan_one - timedelta(days=jan_one.weekday())

# 3. Generation Loop
total_weeks = 53

# --- A. Index Pages (Reserved) ---
index_page_idx = pdf.page_no() + 1
for _ in range(2):  # Reserve 2 pages for Index
    pdf.add_page()
    pdf.draw_background()
    pdf.draw_dot_grid()

# --- B. Data Structures for Navigation ---
months_data = {}  # month_key -> {'timeline_idx': int, 'action_idx': int, 'next_link_id': link_id}
weeks_data = {}  # week_num -> {'action_idx': int, 'reflection_idx': int, 'next_link_id': link_id}
# Pre-calculate months to handle 'Next month' links correctly
unique_months = []
for i in range(total_weeks):
    d = start_date + timedelta(weeks=i)
    if d.year < target_year:
        continue
    m_key = (d.year, d.month)
    if m_key not in unique_months:
        unique_months.append(m_key)
TEXT_TIMELINE = (
    "This page is your Timeline. Though it can be used as a traditional calendar "
    "by adding upcoming events, it’s recommended to use the Timeline to log "
    "events after they’ve happened. This will provide a more accurate and useful "
    "record of your life."
)

TEXT_MONTHLY_ACTION = (
    "The next page is your Monthly Action Plan. It’s designed to help you organize "
    "and prioritize your monthly Tasks. It consists of new Tasks, Future Log items "
    "scheduled for this month, and any important unfinished Tasks from the previous month."
)

TEXT_ACTION_PLAN = (
    "Write down only what you can get done this week. Think of this as your weekly commitments. "
    "If something is too big, break into smaller steps. When you're done, number the top three "
    "things that would make this week a success."
)

TEXT_REFLECTION = (
    "Tidy your weekly entries. Update the monthly timeline and action plan. "
    "Acknowledge up to three things that moved you toward, and up to three things that moved "
    "you away, from the life you want/who you want to be, in a few sentences. "
    "Migrate only relevant Actions into the next week's Action Plan. "
    "Enact any insight from your reflection into the action plan."
)

last_month_key = None
prev_month_timeline_link_id = None
prev_month_action_link_id = None

for week_num in range(1, total_weeks + 1):
    current_monday = start_date + timedelta(weeks=week_num - 1)
    month_key = (current_monday.year, current_monday.month)

    # Check if we need to insert a new Monthly Log
    if month_key != last_month_key and month_key in unique_months:
        month_name = calendar.month_name[current_monday.month]
        days_in_month = calendar.monthrange(current_monday.year, current_monday.month)[
            1
        ]

        # If there was a previous month, point its 'Next' links to this month's pages
        if prev_month_timeline_link_id is not None:
            pdf.set_link(prev_month_timeline_link_id, page=pdf.page_no() + 1)
        if prev_month_action_link_id is not None:
            pdf.set_link(prev_month_action_link_id, page=pdf.page_no() + 2)

        prev_month_key = last_month_key
        prev_month_data = months_data.get(prev_month_key)

        # Timeline Page
        timeline_idx = pdf.page_no() + 1
        pdf.set_link(
            pdf.get_month_link(current_monday.year, current_monday.month),
            page=timeline_idx,
        )

        # Only create 'Next month' links if there is a next month
        is_last_month = month_key == unique_months[-1]
        next_month_timeline_link_id = pdf.add_link() if not is_last_month else None
        next_month_action_link_id = pdf.add_link() if not is_last_month else None

        pdf.draw_timeline(
            month_name,
            current_monday.month,
            current_monday.year,
            days_in_month,
            TEXT_TIMELINE,
            [
                ("Index", pdf.link_to_page(index_page_idx)),
                (
                    "Prev month",
                    pdf.link_to_page(
                        prev_month_data["timeline_idx"] if prev_month_data else None
                    ),
                ),
                ("Next month", next_month_timeline_link_id),
            ],
        )

        # Action Plan Page
        action_idx = pdf.page_no() + 1
        pdf.draw_monthly_action_plan(
            month_name,
            TEXT_MONTHLY_ACTION,
            [
                ("Index", pdf.link_to_page(index_page_idx)),
                (
                    "Prev month",
                    pdf.link_to_page(
                        prev_month_data["action_idx"] if prev_month_data else None
                    ),
                ),
                ("Next month", next_month_action_link_id),
            ],
        )

        months_data[month_key] = {
            "timeline_idx": timeline_idx,
            "action_idx": action_idx,
        }

        last_month_key = month_key
        prev_month_timeline_link_id = next_month_timeline_link_id
        prev_month_action_link_id = next_month_action_link_id

    # --- Week Generation ---
    week_end = current_monday + timedelta(days=6)
    date_str = f"{current_monday.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"

    # We'll use placeholders for week navigation since we don't know page numbers yet
    prev_week_idx = weeks_data[week_num - 1]["action_idx"] if week_num > 1 else None

    # For 'Next week', we need to use a link ID because the page doesn't exist yet
    next_week_link_id = pdf.add_link() if week_num < total_weeks else None

    if week_num > 1:
        # Point the previous week's 'Next' link to this week's Action Plan
        pdf.set_link(weeks_data[week_num - 1]["next_link_id"], page=pdf.page_no() + 1)

    # --- A. Action Plan ---
    week_action_idx = pdf.page_no() + 1
    pdf.set_link(pdf.get_week_link(week_num), page=week_action_idx)
    pdf.add_page()
    pdf.draw_background()
    pdf.draw_dot_grid()

    pdf.draw_instruction_block(
        title="Action Plan: Week", date_subtitle=date_str, instructions=TEXT_ACTION_PLAN
    )
    pdf.draw_navigation_links(
        [
            ("Index", pdf.link_to_page(index_page_idx)),
            ("Prev week", pdf.link_to_page(prev_week_idx)),
            ("Next week", next_week_link_id),
        ]
    )

    # --- B. Daily Pages ---
    for day_offset in range(7):
        day_date = current_monday + timedelta(days=day_offset)
        day_month_key = (day_date.year, day_date.month)
        # Use the month data for the specific day, safely
        day_month_data = months_data.get(day_month_key) or months_data.get(month_key)

        pdf.add_page()
        pdf.draw_background()
        pdf.draw_dot_grid()

        # Set the link destination from the Monthly Log
        link_id = pdf.get_day_link(day_date.year, day_date.month, day_date.day)
        pdf.set_link(link_id, page=pdf.page_no())

        # Header
        pdf.set_font(pdf.active_font, size=60 * SCALE)
        pdf.set_xy(MARGIN_LEFT, 80 * SCALE)
        pdf.cell(0, 70 * SCALE, f"{day_date.strftime('%A')}")

        pdf.set_font(pdf.active_font, size=40 * SCALE)
        pdf.set_xy(MARGIN_LEFT, 150 * SCALE)
        pdf.cell(0, 40 * SCALE, f"{day_date.strftime('%B %d')}")

        # Navigation Links
        nav_links = [
            ("Index", pdf.link_to_page(index_page_idx)),
            ("Weekly log", pdf.link_to_page(week_action_idx)),
        ]
        if day_month_data:
            nav_links.insert(
                1, ("Monthly log", pdf.link_to_page(day_month_data["timeline_idx"]))
            )

        pdf.draw_navigation_links(nav_links)

    # --- C. Reflection ---
    week_reflection_idx = pdf.page_no() + 1
    pdf.add_page()
    pdf.draw_background()
    pdf.draw_dot_grid()

    pdf.draw_instruction_block(
        title="Reflection: Week", date_subtitle=None, instructions=TEXT_REFLECTION
    )
    pdf.draw_navigation_links(
        [
            ("Index", pdf.link_to_page(index_page_idx)),
            ("Prev week", pdf.link_to_page(prev_week_idx)),
            ("Next week", next_week_link_id),
        ]
    )

    weeks_data[week_num] = {
        "action_idx": week_action_idx,
        "reflection_idx": week_reflection_idx,
        "next_link_id": next_week_link_id,
    }

# 4. Draw Index Content
pdf.draw_index_content(start_date, total_weeks, index_page_idx)

# 5. Output
pdf.output("bujo_custom_font.pdf")
print("PDF Generated.")
