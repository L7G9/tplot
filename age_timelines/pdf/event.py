from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from .layout import Area
from ..models import AgeEvent


TITLE_START_WIDTH = 50 * mm
TITLE_WIDTH_INCREMENT = 20 * mm
TITLE_START_LINE_COUNT = 3
TITLE_LINE_COUNT_INCREMENT = 0
DESCRIPTION_START_WIDTH = 50 * mm
DESCRIPTION_WIDTH_INCREMENT = 20 * mm
DESCRIPTION_START_LINE_COUNT = 3
DESCRIPTION_LINE_COUNT_INCREMENT = 1


class PDFEvent():
    """Class to draw an Timeline Event on a Canvas."""
    def __init__(
        self,
        event: AgeEvent,
        canvas: Canvas,
        title_style: ParagraphStyle,
        description_style: ParagraphStyle
    ):
        self.canvas = canvas
        self.area = Area(0, 0, 0, 0)

        title_width = stringWidth(
            event.title,
            title_style.fontName,
            title_style.fontSize
        )
        description_width = stringWidth(
            event.description,
            description_style.fontName,
            description_style.fontSize
        )
        self.area.width = self.calculate_width(title_width, description_width)

        self.title_paragraph = self.create_paragraph(event.title, title_style)
        self.description_paragraph = self.create_paragraph(
            event.description,
            description_style
        )
        self.area.height = self.title_paragraph.height + self.description_paragraph.height

    def calculate_paragraph_width(
        self,
        text_width,
        start_width,
        width_increment,
        start_line_count,
        line_count_increment
    ):
        if text_width <= start_width:
            return text_width
        current_width = start_width
        current_line_count = start_line_count
        while (text_width / current_width) > current_line_count:
            current_width += width_increment
            current_line_count += line_count_increment
        return current_width

    def calculate_width(self, title_width, description_width):
        title_width = self.calculate_paragraph_width(
            title_width,
            TITLE_START_WIDTH,
            TITLE_WIDTH_INCREMENT,
            TITLE_START_LINE_COUNT,
            TITLE_LINE_COUNT_INCREMENT
        )
        description_width = self.calculate_paragraph_width(
            description_width,
            DESCRIPTION_START_WIDTH,
            DESCRIPTION_WIDTH_INCREMENT,
            DESCRIPTION_START_LINE_COUNT,
            DESCRIPTION_LINE_COUNT_INCREMENT
        )
        return max(title_width, description_width)

    def create_paragraph(self, text: str, style: ParagraphStyle) -> Paragraph:
        paragraph = Paragraph(text, style)
        paragraph.wrapOn(self.canvas, self.area.width, 0)

        return paragraph

    def draw(self):
        self.title_paragraph.drawOn(
            self.canvas,
            self.area.x,
            self.area.y + self.description_paragraph.height
        )
        self.description_paragraph.drawOn(
            self.canvas,
            self.area.x,
            self.area.y
        )
