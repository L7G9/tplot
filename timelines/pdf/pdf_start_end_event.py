"""Contains class to draw an event with a start and end time on a Canvas.

Classes:
    PDFStartEndEvent
"""
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from .pdf_event import PDFEvent


class PDFStartEndEvent(PDFEvent):
    """Class to draw an Timeline Event with a start and end time on a Canvas.

    Extends:
        PDFEvent

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

    # TODO: remove duplication with PDFEvent
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
        fixed_size: float,
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
            fixed_size: A float storing the width or height (depending on
            orientation) that this event should be on the timeline.
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

        if orientation == "L":
            _, self.height = self.__landscape_init(
                fixed_size - (2 * self.border_size)
            )
            self.width = fixed_size
        elif orientation == "P":
            max_width -= 2 * self.border_size
            largest_width = max(
                max(time_width, title_width), description_width
            )
            init_width = min(largest_width, max_width)
            min_width = min(time_width, max_width)

            self.width, _ = self.__portrait_init(
                fixed_size, min_width, init_width
            )
            self.height = fixed_size

    def __landscape_init(self, width):
        """Calculates height for a landscape PDFStartEndEvent given that it
        needs to be a set width."""
        return PDFEvent._get_dimensions(self, width)

    def __portrait_init(self, height, desired_width, max_width):
        """Calculates width for a portrait PDFStartEndEvent given that it
        needs to be a set height."""
        current_width, current_height = self.__get_dimensions(desired_width)

        width_increment = (max_width - desired_width) / 5

        while current_height > height:
            expanded_width = current_width + width_increment
            current_width, current_height = self.__get_dimensions(
                expanded_width
            )

        return current_width + (2 * self.border_size), current_height
