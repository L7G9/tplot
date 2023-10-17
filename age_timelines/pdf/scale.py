from reportlab.graphics.shapes import Drawing, Line, String
from reportlab.lib.colors import black
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

from .layout import AgeTimelineLayout, BORDER_SIZE, SCALE_SIZE, SCALE_UNIT_LINE_LENGTH


class PDFScale():
    """Class to draw a Timeline Scale on a Canvas."""
    def __init__(self, layout: AgeTimelineLayout, canvas: Canvas):
        self.layout = layout
        self.canvas = canvas
        self.drawing = Drawing(
            self.layout.scale_area.width * mm,
            self.layout.scale_area.height * mm
        )
        self.add_main_line()
        self.add_time_units()

    def add_main_line(self):
        self.drawing.add(
            Line(
                BORDER_SIZE * mm,
                SCALE_SIZE * mm,
                (BORDER_SIZE + self.layout.scale_description.scale_length) * mm,
                SCALE_SIZE * mm
            )
        )

    def add_time_units(self):
        y_from = SCALE_SIZE * mm
        y_to = (SCALE_SIZE - SCALE_UNIT_LINE_LENGTH) * mm

        for i in range(self.layout.scale_description.scale_units + 1):
            scale_length = self.layout.age_timeline.scale_length
            x = ((i * scale_length * 10) + BORDER_SIZE) * mm
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

    def draw(self):
        self.drawing.drawOn(
            self.canvas,
            self.layout.scale_area.x * mm,
            self.layout.scale_area.y * mm
        )
