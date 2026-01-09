# reMarkable Paper Pro Bullet Journal Generator

## 0. The Final Product

The generator produces a professional, high-performance 2026 Bullet Journal PDF with the following features:

* **Full Hyperlinking**: Instant navigation between Index, Months, Weeks, and Days.
* **Optimized for rMPP**: Native 1620x2160 resolution ensures razor-sharp dots and text.
* **Comprehensive Layout**:
  * **Index**: Global navigation for all months, weeks, and daily logs.
  * **Monthly Log**: Timeline for logging events and an Action Plan for tasks.
  * **Weekly Pages**: Action Plan for commitments and Reflection for weekly reviews.
  * **Daily Pages**: Clean, dated pages for rapid logging.
* **Perfect Grid**: A native 45px (5mm) dot grid that aligns perfectly with the hardware pixels of the Paper Pro.

---

## 1. User Guide

### Quick Start

This project uses `uv` for fast, reliable Python package management.

1. **Prerequisites**: Install [uv](https://github.com/astral-sh/uv).
2. **Generate Journal**:

    ```bash
    uv run main.py
    ```

    The PDF will be saved to `output/bujo_2026.pdf`.

### Configuration & Customization (`config.py`)

The `config.py` file is the central source of truth for the journal's appearance.

* **`FONT_SCALE`**: Global multiplier for all text (e.g., `1.6`).
* **`TOOLBAR_BUFFER`**: Space reserved for the rM toolbar (default `120px`).
* **`MONTHLY_TIMELINE_X/Y_OFFSET`**: Fine-tune the alignment of day numbers in the Monthly Log.
* **`COLOR_PAPER` / `COLOR_DOTS`**: Customize the background and grid colors.
* **`DOT_RADIUS`**: Adjust the size of the grid dots (default `1px`).

---

## 2. Project Overview

A Python-based generator to create a fully hyperlinked, PDF-based Bullet Journal specifically optimized for the **reMarkable Paper Pro (rMPP)**.

**Primary Goal:** Solve the "grid misalignment" issue by abandoning scaling factors in favor of a native, integer-based pixel grid system.

---

## 3. Technical Specifications (Native rM PP)

We are designing natively for the device hardware to ensure perfect rendering without interpolation or blurring.

| Metric | Value | Reasoning |
| :--- | :--- | :--- |
| **Canvas Width** | `1620 px` | Native rM PP width |
| **Canvas Height** | `2160 px` | Native rM PP height |
| **Screen DPI** | `229 PPI` | Native pixel density |
| **Target Grid Size** | `45 px` | ~5mm physical size (standard bujo size) |
| **Dot Radius** | `2 px` | Subtle, non-intrusive guide markers |

### The "Integer-First" Grid Logic

To prevent sub-pixel rendering (which causes "smudged" dots), we do not set margins first. We calculate:

1. **Available Space** = Total Width - Toolbar Buffer
2. **Grid Columns** = Available Space // Grid Size (Integer Division)
3. **Margins** = Calculated to perfectly center the integer grid.

---

## 4. Project Structure

The project follows a strict separation of concerns to keep logic, configuration, and rendering distinct.

```text
rmpp_bujo/
├── fonts/                  # Custom font files (Dosis, etc.)
├── output/                 # Generated PDFs
├── src/
│   ├── infrastructure/     # Interfaces for File I/O (if needed)
│   ├── layout/             # Pydantic models for Page Layouts
│   ├── logic/              # Pure calculation logic (Grid, Dates)
│   └── workers/            # Page generators (Index, Weekly, Daily)
├── config.py               # Constants (Dimensions, Colors)
├── main.py                 # Entry point
└── README.md

```

---

## 5. Architecture

### A. Configuration (`config.py`)

A centralized dictionary or data class containing:

* **Colors:** Ivory background, subtle gray dots, high-contrast text.
* **Fonts:** Pathing for custom fonts.
* **Layout:** Toolbar buffer zone (Left vs. Right handedness).

### B. The Grid Engine

A standalone calculator that outputs exact `(x, y)` coordinates for the grid. It ensures that text elements align to the grid lines, not arbitrary points.

### C. The Navigation "Spine"

A two-pass system to handle hyperlinks:

1. **Pass 1 (Map):** Calculate logical dates and assign them unique Link IDs *before* rendering.
2. **Pass 2 (Render):** Draw the pages using the pre-calculated Link IDs.

### Development

If you want to modify the code or add new page types, please refer to the **Service Object Pattern** rules defined in [AGENT_RULES.md](AGENT_RULES.md).
