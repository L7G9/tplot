
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from .area import Area


class PDFScaleUnitLabel(Area):
    """Class to measure the dimensions of and draw a time unit label on a
    timeline's scale."""
    def __init__(
        self,
        text: str,
        style: ParagraphStyle,
        canvas: Canvas,
        max_width: int
    ):
        print(f"PDFScaleUnitLabel({text})")
        self.canvas = canvas
        self.paragraph = Paragraph(text, style)
        wrap_width = stringWidth(text, style.fontName, style.fontSize)
        if wrap_width > max_width:
            wrap_width = max_width

        self.paragraph.wrapOn(self.canvas, wrap_width, 0)
        super().__init__(0, 0, self.paragraph.width, self.paragraph.height)

    def set_landscape_position(self, x: int, y: int):
        """Centre on x and place under y."""
        self.x = x - (self.width / 2)
        self.y = y

    def set_portrait_position(self, x: int, y: int):
        """Left of x and centre on y."""
        print(f"set_portrait_position({x}, {y}, {self.width}, {self.height})")
        self.x = x - self.width
        self.y = y - (self.height / 2)

        print(f"result ({self.x}, {self.y})")

    def draw(self):
        self.paragraph.drawOn(
            self.canvas,
            self.x,
            self.y
        )
