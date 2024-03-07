"""Contains class to draw an event with a start time and no end time on a
Canvas.

Classes:
    PDFEvent
"""

from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from .area import Area

"""Ideal ratio between width and height of a PDFEvent, if possible should be
twice as wide a high."""
WIDTH_HEIGHT_RATIO = 2.0

"""Fraction to reduce width of PDFEvent by until it meets constraints of
width / height ratio, minimum width and maximum height """
INCREMENT_SIZE = 0.1


class PDFEvent(Area):
    """Class to draw an Timeline Event with a start time on a Canvas.

    Extends:
        Area

    Attributes:
        time_paragraph: A Paragraph displaying the time when the Event
        occurred.
        title_paragraph: A Paragraph displaying the title of the Event.
        description_paragraph: A Paragraph displaying the description of the
        Event.
        border_size: A float storing the gap between the Paragraphs and their
        bounding box.
        canvas: A Canvas to draw the Event on.
    """

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
        border_size: float,
        max_width: float = 0,
        max_height: float = 0,
    ):
        """Initialise Instance.

        Measures width how long each paragraph will be then creates a
        PDFEvent instance of a suitable size and layout to fit into the
        max_width or max_height depending on the timeline orientation.

        Args:
            time: A String describing when the event occurred.
            title: A String holding the event's title.
            description: A String describing the event in detail.
            orientation: A String holding if the event is to be drawn is from
            a landscape or portrait timeline.
            canvas: A Canvas to draw the PDFEvent on.
            time_style: A ParagraphStyle for the time.
            title_paragraph: A ParagraphStyle for the title.
            description_style: A ParagraphStyle for the description.
            border_size: A float storing the gap between the Paragraphs and
            their bounding box.
            max_width: A float storing the maximum width the PDFEvent can be
            on a portrait timeline.
            max_height: A float storing the maximum width the PDFEvent can be
            on a landscape timeline.

        Raises:
            ValueError: If orientation is not L for landscape or P for
            portrait.
        """
        if (orientation != "L") and (orientation != "P"):
            raise ValueError(
                "orientation must be L for landscape or P for portrait"
            )

        self.time_paragraph: Paragraph = Paragraph(time, time_style)
        self.title_paragraph: Paragraph = Paragraph(title, title_style)
        self.description_paragraph: Paragraph = Paragraph(
            description, description_style
        )
        self.border_size = border_size
        self.canvas = canvas

        self.x = 0
        self.y = 0

        time_width = stringWidth(
            time, time_style.fontName, time_style.fontSize
        )
        title_width = stringWidth(
            title, title_style.fontName, title_style.fontSize
        )
        description_width = stringWidth(
            description, description_style.fontName, description_style.fontSize
        )

        self.min_width = 0.0
        self.sized_to_ratio = False
        self.sized_to_min_width = False
        self.sized_to_max_width = False
        self.sized_to_max_height = False

        if orientation == "L":
            self.width, self.height = self.__landscape_init(
                time_width,
                title_width,
                description_width,
                WIDTH_HEIGHT_RATIO,
                max_height,
            )
        elif orientation == "P":
            self.width, self.height = self.__portrait_init(
                time_width,
                title_width,
                description_width,
                WIDTH_HEIGHT_RATIO,
                max_width,
            )

        max_text_width = self.width - (2 * self.border_size)
        self.time_paragraph.wrapOn(self.canvas, max_text_width, 0)
        self.title_paragraph.wrapOn(self.canvas, max_text_width, 0)
        self.description_paragraph.wrapOn(self.canvas, max_text_width, 0)

    def _get_dimensions(self, width: float):
        """Calculates the total width and height needed to display the time,
        title and description Paragraphs for a given width."""
        time_width, time_height = self.time_paragraph.wrap(width, 0)
        title_width, title_height = self.title_paragraph.wrap(width, 0)
        (
            description_width,
            description_height,
        ) = self.description_paragraph.wrap(width, 0)
        max_width = max(max(time_width, title_width), description_width)
        total_height = time_height + title_height + description_height

        return max_width, total_height

    def __landscape_init(
        self,
        time_width: float,
        title_width: float,
        description_width: float,
        target_ratio: float,
        max_height: float,
    ):
        """Calculates the best width and height for a landscape PDFEvent given
        the constraints of a target ratio for width/height and the maximum
        height available to draw it in."""
        init_width = max(max(time_width, title_width), description_width)
        min_width = time_width

        width, height = self._get_dimensions(init_width)
        best_width, best_height = width, height
        width_reduction_increment = width * INCREMENT_SIZE

        # reduce width until within parameters
        while (
            ((width / height) >= target_ratio)
            and (width >= min_width)
            and (height <= max_height)
        ):
            best_width, best_height = width, height
            new_width = width - width_reduction_increment
            width, height = self._get_dimensions(new_width)

        self.min_width = min_width + (2 * self.border_size)
        self.sized_to_ratio = ((width / height) < target_ratio)
        self.sized_to_min_width = (width < min_width)
        self.sized_to_max_height = (height > max_height)

        return best_width + (2 * self.border_size), best_height

    def __portrait_init(
        self,
        time_width: float,
        title_width: float,
        description_width: float,
        target_ratio: float,
        max_width: float,
    ):
        """Calculates the best width and height for a portrait PDFEvent given
        the constraints of a target ratio for width/height and the maximum
        width available to draw it in."""
        largest_width = max(max(time_width, title_width), description_width)
        internal_max_width = max_width - (2 * self.border_size)
        init_width = min(largest_width, internal_max_width)
        min_width = min(time_width, internal_max_width)

        width, height = self._get_dimensions(init_width)
        best_width, best_height = width, height
        width_reduction_increment = width * INCREMENT_SIZE

        # reduce width until within parameters
        while (
            ((width / height) >= target_ratio)
            and (width >= min_width)
        ):
            best_width, best_height = width, height
            new_width = width - width_reduction_increment
            width, height = self._get_dimensions(new_width)

        self.min_width = min_width + (2 * self.border_size)
        self.sized_to_ratio = ((width / height) < target_ratio)
        self.sized_to_min_width = (width < min_width)
        self.sized_to_max_width = (width == internal_max_width)

        return best_width + (2 * self.border_size), best_height

    def draw(self):
        """Draw PDFEvent on it's canvas."""
        self.time_paragraph.drawOn(
            self.canvas,
            self.x + self.border_size,
            self.y
            + self.height
            - self.time_paragraph.height,
        )
        self.title_paragraph.drawOn(
            self.canvas,
            self.x + self.border_size,
            self.y
            + self.height
            - self.time_paragraph.height
            - self.title_paragraph.height,
        )
        self.description_paragraph.drawOn(
            self.canvas,
            self.x + self.border_size,
            self.y
            + self.height
            - self.time_paragraph.height
            - self.title_paragraph.height
            - self.description_paragraph.height,
        )
        self.canvas.rect(
            self.x,
            self.y,
            self.width,
            self.height,
        )
