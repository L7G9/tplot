"""Contains class to draw the lines joining the events and scale on a PDF
representation  of a timeline.

Classes:
    PDFJoiningLines
"""
from reportlab.graphics.shapes import Drawing, Line
from reportlab.pdfgen.canvas import Canvas

from ..models import EventArea, Timeline
from .area import Area
from .pdf_event import PDFEvent
from .pdf_event_area import PDFEventArea
from .pdf_scale import PDFScale


class PDFJoiningLines(Area):
    """Class to draw the lines joining the events and scale on a PDF
    representation  of a timeline.

    Extends:
        Area

    Attributes:
        canvas: A Canvas instance to draw the timeline on.
        drawing: A Drawing instance to add the lines to before drawing on the
        canvas.
    """
    def __init__(self, canvas: Canvas, drawable_area: Area):
        """Initialise Instance.

        Creates a Drawing instance equal to size of this area.

        Args:
            canvas: A Canvas instance to draw the joining lines on.
            drawable_area: An Area instance from a timeline layout representing
            the area inside the page borders that can be drawn on to produce
            the timeline.
        """
        super().__init__(
            drawable_area.x,
            drawable_area.y,
            drawable_area.width,
            drawable_area.height
        )
        self.canvas = canvas
        self.drawing = Drawing(int(self.width), int(self.height))

    def is_before(self, event_area: EventArea, timeline: Timeline) -> bool:
        """Test if event area is before timeline scale.

        Args:
            event_area: An EventArea instance to test the position of.
            timeline: A Timeline instance to test event_area against.

        Returns:
            A bool set to true if the event area is positioned before (below
            or to left of depending on timeline orientation) the timeline
            scale.
        """
        return event_area.page_position < timeline.page_scale_position

    def get_line(
            self,
            pdf_event_area: PDFEventArea,
            pdf_event: PDFEvent,
            pdf_scale: PDFScale,
            orientation: str,
            event_is_before_scale: bool
    ) -> Line:
        """Get a line joining the given PDFEvent and PDFScale instances.

        Coordinates of returned line are relative to start of the area this
        instance covers.

        Args:
            pdf_event_area: The PDFEventArea instance containing pdf_event.
            pdf_event: A PDFEvent instance to create a joining line from.
            pdf_scale: A PDFScale instance to create a joining line to.
            orientation: A str describing the timelines orientation
            event_is_before_scale: A bool describing if pdf_event_area is
            positioned before pdf_scale on the PDF timeline.

        Returns:
            A Line instance.
        """
        if orientation == "L":
            x_from = pdf_event_area.x + pdf_event.x
            x_to = pdf_scale.x + pdf_event.position_on_scale
            if event_is_before_scale:
                y_from = pdf_event_area.y + pdf_event.top()
                y_to = pdf_scale.y
            else:
                y_from = pdf_event_area.y + pdf_event.y
                y_to = pdf_scale.top()
        else:
            y_from = pdf_event_area.y + pdf_event.top()
            y_to = (
                pdf_scale.y
                + pdf_event.position_on_scale
                + pdf_event.height
            )
            if event_is_before_scale:
                x_from = pdf_event_area.x + pdf_event.right()
                x_to = pdf_scale.x
            else:
                x_from = pdf_event_area.x + pdf_event.x
                x_to = pdf_scale.right()

        x_from -= self.x
        y_from -= self.y
        x_to -= self.x
        y_to -= self.y

        return Line(x_from, y_from, x_to, y_to)

    def add_line(self, line: Line):
        """Add line to drawing.

        Args:
            line: A Line instance to add.
        """
        self.drawing.add(line)

    def draw(self):
        """Draw PDFJoiningLines on it's canvas."""
        self.drawing.drawOn(self.canvas, self.x, self.y)
