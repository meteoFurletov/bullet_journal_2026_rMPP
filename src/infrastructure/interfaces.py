from abc import ABC, abstractmethod


class PDFInterface(ABC):
    @abstractmethod
    def add_page(self):
        pass

    @abstractmethod
    def set_fill_color(self, r, g, b):
        pass

    @abstractmethod
    def set_draw_color(self, r, g, b):
        pass

    @abstractmethod
    def set_text_color(self, r, g, b):
        pass

    @abstractmethod
    def set_line_width(self, width):
        pass

    @abstractmethod
    def rect(self, x, y, w, h, style=""):
        pass

    @abstractmethod
    def line(self, x1, y1, x2, y2):
        pass

    @abstractmethod
    def circle(self, x, y, r, style=""):
        pass

    @abstractmethod
    def polygon(self, points, style=""):
        pass

    @abstractmethod
    def output(self, name):
        pass

    @abstractmethod
    def add_link(self):
        pass

    @abstractmethod
    def set_link(self, link, page=None, x=None, y=None):
        pass

    @abstractmethod
    def link(self, x, y, w, h, link):
        pass

    @abstractmethod
    def set_font(self, family, style="", size=0):
        pass

    @abstractmethod
    def set_xy(self, x, y):
        pass

    @abstractmethod
    def cell(self, w, h=0, txt="", border=0, ln=0, align="", fill=False, link=""):
        pass

    @abstractmethod
    def multi_cell(
        self, w, h, txt, border=0, align="J", fill=False, dry_run=False, output=""
    ):
        pass

    @abstractmethod
    def add_font(self, family, style, fname):
        pass

    @abstractmethod
    def set_auto_page_break(self, auto, margin=0):
        pass

    @abstractmethod
    def set_margin(self, margin):
        pass
