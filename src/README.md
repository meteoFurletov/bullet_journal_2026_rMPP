# Core Components (Shared Library)

This directory contains reusable components for generating reMarkable-optimized PDFs.

## 1. Layout Standards (`src.layout`)

To ensure a consistent user experience on the reMarkable Paper Pro, all projects should respect the **System Toolbar Buffer**.

* **Toolbar Buffer:** 120px (standard).
* **Sidebar Placement:** Typically on the `LEFT` for right-handed users.
* **Safe Zone:** Use `LayoutManager.calculate_safe_zone()` to get the usable Rect where text and interactive elements should be placed.

## 2. Grid System (`src.workers.grid_worker`)

Standard engineering dot grid.

* **Grid Size:** 45px ($\approx$ 5mm at 229 DPI).
* **Dot Radius:** 2px.
* **Worker:** Use `GridWorker` to render a centered grid within a given canvas or safe zone.

## 3. PDF Infrastructure (`src.infrastructure`)

* **`PDFInterface`**: Abstract base class for PDF operations.
* **`FPDFAdapter`**: Implementation using `fpdf2`, handling internal link management and font registration.
