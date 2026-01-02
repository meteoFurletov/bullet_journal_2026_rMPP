from src.infrastructure.pdf_adapter import FPDFAdapter
from src.workers.grid_worker import GridWorker, GridInput
import config


def main():
    # Initialize PDF adapter
    pdf = FPDFAdapter(format=(config.CANVAS_WIDTH, config.CANVAS_HEIGHT))
    pdf.add_page()

    # Draw background
    pdf.set_fill_color(*config.COLOR_PAPER)
    pdf.rect(0, 0, config.CANVAS_WIDTH, config.CANVAS_HEIGHT, "F")

    # Initialize Grid Worker
    worker = GridWorker(pdf)

    # Define Grid Input
    grid_input = GridInput(
        canvas_width=config.CANVAS_WIDTH,
        canvas_height=config.CANVAS_HEIGHT,
        grid_size=config.GRID_SIZE,
        toolbar_buffer=config.TOOLBAR_BUFFER,
        dot_radius=config.DOT_RADIUS,
    )

    # Draw Grid
    output = worker.draw_grid(grid_input, config.COLOR_DOTS)

    print(f"Grid generated with {output.num_cols} columns and {output.num_rows} rows.")
    print(f"Margins: Left={output.margin_left}, Top={output.margin_top}")

    # Save PDF
    pdf.output("output/test_grid.pdf")
    print("Test grid saved to output/test_grid.pdf")


if __name__ == "__main__":
    main()
