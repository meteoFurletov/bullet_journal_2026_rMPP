import os

# --- Native rM PP Specifications ---
CANVAS_WIDTH = 1620
CANVAS_HEIGHT = 2160
DPI = 229
GRID_SIZE = 45
DOT_RADIUS = 1

# --- Layout ---
TOOLBAR_BUFFER = 120  # Buffer for the reMarkable toolbar (left or right)
MONTHLY_TIMELINE_X_OFFSET = 70  # Manual adjustment for day numbers in Monthly Log
MONTHLY_TIMELINE_Y_OFFSET = 27  # Manual adjustment for day numbers in Monthly Log

# --- Colors (R, G, B) ---
COLOR_PAPER = (252, 252, 250)
COLOR_DOTS = (100, 100, 100)
COLOR_TEXT = (40, 40, 40)
COLOR_INSTRUCT = (120, 120, 120)

# --- Fonts ---
FONT_NAME = "Dosis"
FONT_DIR = "fonts/Dosis/static"
FONT_REGULAR = os.path.join(FONT_DIR, "Dosis-Regular.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "Dosis-Bold.ttf")
FONT_ITALIC = os.path.join(FONT_DIR, "Dosis-Italic.ttf")

# --- Typography System ---
# Adjust FONT_SCALE to resize all text globally
FONT_SCALE = 1.6

SIZE_H1 = int(60 * FONT_SCALE)
SIZE_H2 = int(40 * FONT_SCALE)
SIZE_H3 = int(30 * FONT_SCALE)
SIZE_BODY_LG = int(24 * FONT_SCALE)
SIZE_BODY = int(20 * FONT_SCALE)
SIZE_BODY_SM = int(18 * FONT_SCALE)
SIZE_TINY = int(16 * FONT_SCALE)

# --- Font Sizes (Mapped to System) ---
SIZE_NAV_LINKS = SIZE_BODY_LG
SIZE_INSTRUCT_TITLE = SIZE_H1
SIZE_INSTRUCT_SUBTITLE = SIZE_H2
SIZE_INSTRUCT_TEXT = SIZE_BODY

SIZE_DAILY_TITLE = SIZE_H1
SIZE_DAILY_SUBTITLE = SIZE_H2

SIZE_WEEKLY_TITLE = SIZE_H1
SIZE_WEEKLY_SUBTITLE = SIZE_H2

SIZE_MONTHLY_TITLE = SIZE_H1
SIZE_MONTHLY_SUBTITLE = SIZE_H2
SIZE_MONTHLY_TIMELINE_DAY = int(GRID_SIZE * 0.7 * FONT_SCALE)

SIZE_INDEX_SECTION_TITLE = SIZE_H2
SIZE_INDEX_MONTH_NAME = SIZE_H3
SIZE_INDEX_WEEK_LABEL = SIZE_BODY_LG
SIZE_INDEX_DAILY_LOG_MONTH = SIZE_H3
SIZE_INDEX_DAILY_LOG_DAY = SIZE_BODY_SM

# --- Line Heights (Relative to Font Sizes) ---
LINE_HEIGHT_NAV_LINKS = int(SIZE_NAV_LINKS * 1.3)
LINE_HEIGHT_INSTRUCT_TEXT = int(SIZE_INSTRUCT_TEXT * 1.5)
LINE_HEIGHT_DAILY_TITLE = int(SIZE_DAILY_TITLE * 1.2)
LINE_HEIGHT_DAILY_SUBTITLE = int(SIZE_DAILY_SUBTITLE * 1.1)
LINE_HEIGHT_INDEX_MONTH = int(SIZE_INDEX_MONTH_NAME * 1.5)
LINE_HEIGHT_INDEX_WEEK = int(SIZE_INDEX_WEEK_LABEL * 1.5)
LINE_HEIGHT_INDEX_DAILY_LOG_MONTH = int(SIZE_INDEX_DAILY_LOG_MONTH * 1.3)
LINE_HEIGHT_INDEX_DAILY_LOG_DAY = int(SIZE_INDEX_DAILY_LOG_DAY * 1.3)

# --- Dynamic Layout Positions ---
Y_HEADER_TITLE = 80
Y_HEADER_SUBTITLE = Y_HEADER_TITLE + int(SIZE_H1 * 1.2)
Y_HEADER_INSTRUCTIONS = Y_HEADER_SUBTITLE + int(SIZE_H2 * 1.2)
Y_NAV_LINKS = 60
X_NAV_LINKS_RIGHT = CANVAS_WIDTH - 280

# --- Text Content ---
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
