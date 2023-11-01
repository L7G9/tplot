from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from .area import Area


class PDFScaleLine(Area):
    """Class to measure dimensions of and draw the line of a timeline's scale."""
    def __init__(self, scale_description, canvas: Canvas, unit_line_length):
        self.x = 0
        self.y = 0
        self.canvas = canvas
        self.drawing = None

        scale_line_length = scale_description.scale_length * mm
        unit_line_count = scale_description.scale_units + 1
        unit_line_gap = scale_line_length / scale_description.scale_units

        if scale_description.timeline.page_orientation == "L":
            self.__landscape_init(scale_line_length, unit_line_count, unit_line_gap, unit_line_length)
        else:
            self.__portrait_init(scale_line_length, unit_line_count, unit_line_gap, unit_line_length)

    def __landscape_init(self, scale_line_length, unit_line_count, unit_line_gap, unit_line_length):
        self.width = scale_line_length
        self.height = unit_line_length
        self.drawing = Drawing(scale_line_length, unit_line_length)


        self.drawing.add(Line(0, unit_line_length, scale_line_length, unit_line_length))

        for i in range(unit_line_count):
            x = i * unit_line_gap
            self.drawing.add(Line(x, 0, x, unit_line_length))

    def __portrait_init(self, scale_line_length, unit_line_count, unit_line_gap, unit_line_length):
        self.width = unit_line_length
        self.height = scale_line_length
        self.drawing = Drawing(unit_line_length, scale_line_length)

        self.drawing.add(Line(unit_line_length, 0, unit_line_length, scale_line_length))

        for i in range(unit_line_count):
            y = i * unit_line_gap
            self.drawing.add(Line(0, y, unit_line_length, y))

    def draw(self):
        self.drawing.drawOn(
            self.canvas,
            self.x,
            self.y
        )
