from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from .area import Area


class PDFStartEndEvent(Area):
    """Class to draw an Timeline Event with a start and end time on a Canvas."""
    def __init__(
        self,
        time: str,
        title: str,
        description: str,
        orientation: str,
        canvas: Canvas,
        time_style: ParagraphStyle,
        title_style: ParagraphStyle,
        description_style: ParagraphStyle,
        fixed_size: float,
        max_width: float = 0,
        max_height: float = 0
    ):

        if (orientation != "L") and (orientation != "P"):
            raise ValueError("orientation must be L for landscape or P for portrait")

        self.time_paragraph: Paragraph = Paragraph(time, time_style)
        self.title_paragraph: Paragraph = Paragraph(title, title_style)
        self.description_paragraph: Paragraph = Paragraph(description, description_style)
        self.canvas = canvas

        self.x = 0
        self.y = 0

        time_width = stringWidth(
            time,
            time_style.fontName,
            time_style.fontSize
        )
        title_width = stringWidth(
            title,
            title_style.fontName,
            title_style.fontSize
        )
        description_width = stringWidth(
            description,
            description_style.fontName,
            description_style.fontSize
        )

        if orientation == "L":
            _, self.height = self.__landscape_init(fixed_size)
            self.width = fixed_size
        elif orientation == "P":

            largest_width = max(max(time_width, title_width), description_width)
            init_width = min(largest_width, max_width)
            min_width = min(time_width, max_width)

            self.width, _ = self.__portrait_init(fixed_size, min_width, init_width)
            self.height = fixed_size

    def __landscape_init(self, width):
        return self.__get_dimensions(width)

    def __portrait_init(self, height, desired_width, max_width):
        current_width, current_height = self.__get_dimensions(desired_width)

        width_increment = (max_width - desired_width) / 5

        while current_height > height:
            expanded_width = current_width + width_increment
            current_width, current_height = self.__get_dimensions(expanded_width)

        return current_width, current_height

    def __get_dimensions(self, width):
        time_width, time_height = self.time_paragraph.wrap(width, 0)
        title_width, title_height = self.title_paragraph.wrap(width, 0)
        description_width, description_height = self.description_paragraph.wrap(width, 0)
        max_width = max(max(time_width, title_width), description_width)
        total_height = time_height + title_height + description_height

        return max_width, total_height

    def draw(self):
        self.canvas.rect(self.x, self.y, self.width, self.height)
        time_y = self.y + self.height - self.time_paragraph.height
        self.time_paragraph.drawOn(
            self.canvas,
            self.x,
            time_y,
        )
        title_y = time_y - self.title_paragraph.height
        self.title_paragraph.drawOn(
            self.canvas,
            self.x,
            title_y
        )
        description_y = title_y - self.description_paragraph.height
        self.description_paragraph.drawOn(
            self.canvas,
            self.x,
            description_y
        )
