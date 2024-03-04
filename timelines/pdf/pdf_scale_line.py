"""Contains class to draw the line of a timeline's scale on a Canvas.

Classes:
    PDFScaleLine
"""

from typing import Union

from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from .area import Area
from .scale_description import ScaleDescription


class PDFScaleLine(Area):
    """Class to measure dimensions of and draw the line of a timeline's scale.

    Extends:
        Area

    Attributes:
        canvas: A Canvas to draw the PDFScaleLine on.
        drawing: A Drawing instance to add lines needed for the PDFScaleLine
        to.
    """

    def __init__(
        self,
        scale_description: ScaleDescription,
        canvas: Canvas,
        unit_line_length: float,
    ):
        """Initialise Instance.

        Args:
            scale_description: A ScaleDescription instance holding
            the settings for the scale to draw.
            canvas: A Canvas to draw the PDFEvent on.
            unit_line_length: A float equal to the length of lines used to
            mark each unit on the line.
        """
        self.x = 0
        self.y = 0
        self.canvas: Canvas = canvas
        self.drawing: Union[Drawing, None] = None

        scale_line_length = scale_description.get_scale_length() * mm
        unit_line_count = scale_description.get_scale_units() + 1
        unit_line_gap = scale_line_length / scale_description.get_scale_units()

        if scale_description.timeline.page_orientation == "L":
            self.__landscape_init(
                scale_line_length,
                unit_line_count,
                unit_line_gap,
                unit_line_length,
            )
        else:
            self.__portrait_init(
                scale_line_length,
                unit_line_count,
                unit_line_gap,
                unit_line_length,
            )

    def __landscape_init(
        self,
        scale_line_length: float,
        unit_line_count: int,
        unit_line_gap: float,
        unit_line_length: float,
    ):
        """Set the dimensions and draw the lines for the scale line of a
        landscape timeline."""
        self.width = scale_line_length
        self.height = unit_line_length
        self.drawing = Drawing(int(scale_line_length), int(unit_line_length))

        self.drawing.add(
            Line(0, unit_line_length, scale_line_length, unit_line_length)
        )

        for i in range(unit_line_count):
            x = i * unit_line_gap
            self.drawing.add(Line(x, 0, x, unit_line_length))

    def __portrait_init(
        self,
        scale_line_length: float,
        unit_line_count: int,
        unit_line_gap: float,
        unit_line_length: float,
    ):
        """Set the dimensions and draw the lines for the scale line of a
        portrait timeline."""
        self.width = unit_line_length
        self.height = scale_line_length
        self.drawing = Drawing(int(unit_line_length), int(scale_line_length))

        self.drawing.add(
            Line(unit_line_length, 0, unit_line_length, scale_line_length)
        )

        for i in range(unit_line_count):
            y = i * unit_line_gap
            self.drawing.add(Line(0, y, unit_line_length, y))

    def draw(self):
        """Draw this instance on it's canvas."""
        if self.drawing is not None:
            self.drawing.drawOn(self.canvas, self.x, self.y)
