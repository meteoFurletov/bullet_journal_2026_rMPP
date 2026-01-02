from fpdf import FPDF
from src.infrastructure.interfaces import PDFInterface


class FPDFAdapter(PDFInterface):
    def __init__(self, orientation="P", unit="pt", format=(1620, 2160)):
        self.pdf = FPDF(orientation=orientation, unit=unit, format=format)
        self.pdf.set_auto_page_break(False)

    def add_page(self):
        self.pdf.add_page()

    def set_fill_color(self, r, g, b):
        self.pdf.set_fill_color(r, g, b)

    def rect(self, x, y, w, h, style=""):
        self.pdf.rect(x, y, w, h, style)

    def output(self, name):
        self.pdf.output(name)

    def add_link(self):
        return self.pdf.add_link()

    def set_link(self, link, page=None, x=None, y=None):
        # fpdf2 set_link expects x and y to be numbers if provided,
        # but if we only want to set the page, we should be careful.
        # Actually, fpdf2's set_link signature is set_link(link, page=-1, x=0, y=0)
        # Wait, let's check the version.
        kwargs = {}
        if page is not None:
            kwargs["page"] = page
        if x is not None:
            kwargs["x"] = x
        if y is not None:
            kwargs["y"] = y
        self.pdf.set_link(link, **kwargs)

    def set_font(self, family, style="", size=0):
        self.pdf.set_font(family, style, size)

    def set_text_color(self, r, g, b):
        self.pdf.set_text_color(r, g, b)

    def set_xy(self, x, y):
        self.pdf.set_xy(x, y)

    def cell(self, w, h=0, txt="", border=0, ln=0, align="", fill=False, link=""):
        self.pdf.cell(w, h, txt, border, ln, align, fill, link)

    def multi_cell(
        self, w, h, txt, border=0, align="J", fill=False, dry_run=False, output=""
    ):
        return self.pdf.multi_cell(w, h, txt, border, align, fill, dry_run, output)

    def line(self, x1, y1, x2, y2):
        self.pdf.line(x1, y1, x2, y2)

    def set_draw_color(self, r, g, b):
        self.pdf.set_draw_color(r, g, b)

    def set_line_width(self, width):
        self.pdf.set_line_width(width)

    def polygon(self, points, style=""):
        self.pdf.polygon(points, style)

    def page_no(self):
        return self.pdf.page_no()

    def add_font(self, family, style="", fname="", uni=False):
        self.pdf.add_font(family, style, fname)
