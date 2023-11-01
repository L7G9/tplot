from reportlab.graphics.shapes import Drawing, Line, String
from reportlab.lib.colors import black
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth, getFont
from reportlab.pdfgen.canvas import Canvas

from timelines.pdf.timeline_layout import TimelineLayout


def get_font_height(font_name, font_size):
    face = getFont(font_name).face
    return (face.ascent - face.descent) / 1000 * font_size


class ScaleDrawer():
    """Class to draw a Timeline Scale on a Canvas."""
    def __init__(self, layout: TimelineLayout, canvas: Canvas):
        self.layout = layout
        self.canvas = canvas
        self.drawing = Drawing(
            self.layout.scale_area.width * mm,
            self.layout.scale_area.height * mm
        )
        if layout.timeline.page_orientation == "L":
            self.landscape_add_main_line()
            self.landscape_add_time_units()
        else:
            self.portrait_add_main_line()
            self.portrait_add_time_units()

    def landscape_add_main_line(self):
        self.drawing.add(
            Line(
                self.layout.border_size * mm,
                self.layout.scale_size * mm,
                (self.layout.border_size + self.layout.scale_description.scale_length) * mm,
                self.layout.scale_size * mm
            )
        )

    def portrait_add_main_line(self):
        self.drawing.add(
            Line(
                self.layout.scale_size * mm,
                self.layout.border_size * mm,
                self.layout.scale_size * mm,
                (self.layout.border_size + self.layout.scale_description.scale_length) * mm,
            )
        )

    def landscape_add_time_units(self):
        y_from = self.layout.scale_size * mm
        y_to = (self.layout.scale_size - self.layout.scale_unit_line_length) * mm

        for i in range(self.layout.scale_description.scale_units + 1):
            scale_length = self.layout.timeline.scale_length
            x = ((i * scale_length * 10) + self.layout.border_size) * mm
            self.drawing.add(Line(x, y_from, x, y_to))
            label_text = self.layout.scale_description.get_scale_label(i)
            # TODO - get font details from a Paragraph Style
            label_width = stringWidth(label_text, "Times-Roman", 10)
            center_x = x - (label_width / 2)
            self.drawing.add(
                String(
                        center_x,
                        0,
                        label_text,
                        fontName="Times-Roman",
                        fontSize=10,
                        fillColor=black
                    )
               )

    def portrait_add_time_units(self):
        x_from = self.layout.scale_size * mm
        x_to = (self.layout.scale_size - self.layout.scale_unit_line_length) * mm

        for i in range(self.layout.scale_description.scale_units + 1):
            scale_length = self.layout.timeline.scale_length
            y = ((i * scale_length * 10) + self.layout.border_size) * mm
            self.drawing.add(Line(x_from, y, x_to, y))
            label_text = self.layout.scale_description.get_scale_label(i)
            # TODO - get font details from a Paragraph Style
            label_height = get_font_height("Times-Roman", 10)
            print(f"{label_height}")
            center_y = y
            self.drawing.add(
                String(
                        0,
                        center_y,
                        label_text,
                        fontName="Times-Roman",
                        fontSize=10,
                        fillColor=black
                    )
               )

    def draw(self):
        self.drawing.drawOn(
            self.canvas,
            self.layout.scale_area.x * mm,
            self.layout.scale_area.y * mm
        )
