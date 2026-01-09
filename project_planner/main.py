import os
from pypdf import PdfReader, PdfWriter, Transformation
from src.infrastructure.pdf_adapter import FPDFAdapter
import project_planner.config as config
from project_planner.logic.planner_map import SpineLogic
from project_planner.workers.planner_worker import ProjectPlannerWorker, PlannerInput


def main():
    # 1. Setup PDF
    pdf = FPDFAdapter(format=(config.CANVAS_WIDTH, config.CANVAS_HEIGHT))

    # Register Fonts
    # We use paths relative to the project root as configured in common logic usually
    # or absolute paths here
    font_path_reg = (
        "/home/meteof/proj/bullet_journal/fonts/Dosis/static/Dosis-Regular.ttf"
    )
    font_path_bold = (
        "/home/meteof/proj/bullet_journal/fonts/Dosis/static/Dosis-Bold.ttf"
    )

    if os.path.exists(font_path_reg):
        pdf.add_font(config.FONT_NAME, "", font_path_reg)
    if os.path.exists(font_path_bold):
        pdf.add_font(config.FONT_NAME, "B", font_path_bold)

    # 2. Initialize Links (Pre-pass)
    spine = SpineLogic(pdf)
    planner_map = spine.initialize_links(total_pages=10)

    # 3. Setup Worker
    worker = ProjectPlannerWorker(pdf)

    # 4. Define Input
    planner_input = PlannerInput(
        project_name="Project",
    )

    # 5. Generate PDF
    worker.draw_planner(planner_input, planner_map.page_links)

    # 6. Output paths
    output_path = "/home/meteof/proj/bullet_journal/output/project_planner.pdf"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the fpdf2 generated file temporarily
    temp_gen_path = output_path.replace(".pdf", "_temp.pdf")
    pdf.output(temp_gen_path)

    # 7. Merge Background for Page 1 (planner.pdf)
    background_path = config.HUB_BACKGROUND_PDF
    if os.path.exists(background_path):
        print(f"Merging background from {background_path}...")
        writer = PdfWriter()
        generated_reader = PdfReader(temp_gen_path)
        background_reader = PdfReader(background_path)

        # Get first page of generated PDF (this contains the right rail and links)
        content_page = generated_reader.pages[0]
        # Get first page of background PDF
        bg_page = background_reader.pages[0]

        # Scale background to fit canvas (1620x2160)
        scale_factor = config.CANVAS_WIDTH / float(bg_page.mediabox.width)

        # Merge background UNDER the content (links/rail)
        # We merge bg_page INTO content_page with over=False to preserve content_page's annotations (links)
        content_page.merge_transformed_page(
            bg_page, Transformation().scale(scale_factor), over=False
        )

        # Add the merged page (with links and background) to writer
        writer.add_page(content_page)

        # Add remaining pages from generated PDF
        for i in range(1, len(generated_reader.pages)):
            writer.add_page(generated_reader.pages[i])

        with open(output_path, "wb") as f_out:
            writer.write(f_out)

        # Clean up
        if os.path.exists(temp_gen_path):
            os.remove(temp_gen_path)
        print(f"Project Planner with background generated at: {output_path}")
    else:
        # Fallback if no background
        os.rename(temp_gen_path, output_path)
        print(f"Project Planner generated at: {output_path}")


if __name__ == "__main__":
    main()
