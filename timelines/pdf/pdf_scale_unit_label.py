"""Contains class for to draw a single unit of a timeline's scale on a Canvas.

Classes:
    PDFScaleLine
"""

from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from .area import Area


class PDFScaleUnitLabel(Area):
    """Class to measure the dimensions of and draw a time unit label on a
    timeline's scale.

    Extends:
        Area

    Attributes:
        canvas: A Canvas to draw the PDFScaleLine on.
        paragraph: A Paragraph instance to draw the unit in.
    """

    def __init__(
        self, text: str, style: ParagraphStyle, canvas: Canvas, max_width: int
    ):
        """Initialise Instance.

        Args:
            text: A string describing the time unit on the scale.
            style: A ParagraphStyle for the Paragraph instance containing time
            unit text.
            canvas: A Canvas to draw the PDFScaleUnitLabel on.
            max_width: A float equal to maximum width the unit label can be.
        """
        self.canvas = canvas
        self.paragraph = Paragraph(text, style)
        wrap_width = stringWidth(text, style.fontName, style.fontSize)
        if wrap_width > max_width:
            wrap_width = max_width

        self.paragraph.wrapOn(self.canvas, wrap_width, 0)
        super().__init__(0, 0, self.paragraph.width, self.paragraph.height)

    def set_landscape_position(self, x: float, y: float):
        """Position the paragraph describing time unit for a landscape
        timeline.

        Centre on x and place under y.

        Args:
            x: A float equal to the x coordinate.
            y: A float equal to the y coordinate.
        """
        self.x = x - (self.width / 2)
        self.y = y

    def set_portrait_position(self, x: float, y: float):
        """Position the paragraph describing time unit for a portrait timeline.

        Left of x and centre on y.

        Args:
            x: A float equal to the x coordinate.
            y: A float equal to the y coordinate.
        """
        self.x = x - self.width
        self.y = y - (self.height / 2)

    def draw(self):
        """Draw this instance on it's canvas."""
        self.paragraph.drawOn(self.canvas, self.x, self.y)
