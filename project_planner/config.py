# --- Native rM PP Specifications ---
CANVAS_WIDTH = 1620
CANVAS_HEIGHT = 2160
GRID_SIZE = 45  # ~5mm at 229 DPI
DOT_RADIUS = 1

# --- Backgrounds ---
HUB_BACKGROUND_PDF = "/home/meteof/proj/bullet_journal/project_planner/planner.pdf"

# --- Layout ---
TOOLBAR_BUFFER = 120
RIGHT_RAIL_WIDTH = 140
HUB_HEADER_RATIO = 0.25
MAP_ARCH_RATIO = 0.60

# --- HUB Page ---
HUB_TITLE_X = 40
HUB_TITLE_Y = 100

# --- MAP Page ---
# Divider is 4cm + 3cm = 7cm from the right sidebar.
# 1cm ~ 90px (based on 45px = 5mm grid)
MAP_DIVIDER_OFFSET_X = 512  # 7cm * 90px
MAP_TITLE_Y = 100
MAP_ARCHITECTURE_TITLE = "Architecture"
MAP_TASKLIST_TITLE = "Tasklist"

# --- Colors (R, G, B) ---
COLOR_PAPER = (252, 252, 250)
COLOR_DOTS = (0, 0, 0)
COLOR_TEXT = (40, 40, 40)
COLOR_SIDEBAR = (245, 245, 245)
COLOR_LINE = (180, 180, 180)

# --- Fonts ---
FONT_NAME = "Dosis"
# Adjust FONT_SCALE to resize all text globally (matching bujo)
FONT_SCALE = 1.6

SIZE_H1 = int(60 * FONT_SCALE)
SIZE_H2 = int(40 * FONT_SCALE)
SIZE_H3 = int(30 * FONT_SCALE)
SIZE_BODY_LG = int(24 * FONT_SCALE)
SIZE_BODY = int(20 * FONT_SCALE)

# Mapped sizes
SIZE_NAV_LINKS = SIZE_BODY_LG
SIZE_TITLE = SIZE_H1
SIZE_SECTION_HEADER = SIZE_H2
