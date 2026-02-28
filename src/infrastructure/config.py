import os

# --- Fonts ---
FONT_NAME = "LiberationSerif"
FONT_DIR = "/usr/share/fonts/truetype/liberation/"

FONT_REGULAR = os.path.join(FONT_DIR, "LiberationSerif-Regular.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")
FONT_ITALIC = os.path.join(FONT_DIR, "LiberationSerif-Italic.ttf")
FONT_BOLD_ITALIC = os.path.join(FONT_DIR, "LiberationSerif-BoldItalic.ttf")

# --- Typography ---
BASE_FONT_SIZE = 14.0
LINE_HEIGHT = 8.0  # Slightly more line spacing for readability
HEADLINE_SCALE = 1.3

# --- Colors (R, G, B) ---
COLOR_TEXT = (0, 0, 0)
COLOR_HEADER = (0, 0, 0)
COLOR_SEPARATOR = (180, 180, 180)

# --- Layout ---
MARGIN_LEFT = 20
MARGIN_RIGHT = 15
MARGIN_TOP = 20
MARGIN_BOTTOM = 20
SEPARATOR_SPACE = 8  # mm between notes
