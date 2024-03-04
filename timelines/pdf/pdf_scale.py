"""Contains class to draw a timeline's scale on a Canvas.

Classes:
    PDFScale
"""


from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm
from .area import Area
from .pdf_scale_line import PDFScaleLine
from .pdf_scale_units import PDFScaleUnits
from .pdf_event import PDFEvent
from .scale_description import ScaleDescription
from .time_unit import TimeUnit


"""Default length for the lines marking each unit on the scale."""
DEFAULT_UNIT_LINE_LENGTH = 5 * mm


class PDFScale(Area):
    """Class to draw a timeline's scale.

    Extends:
        Area

    Attributes:
        scale_description: A ScaleDescription instance holding of the scale to
        create.
        units: A PDFScaleUnits instance to draw the units on the timeline's
        scale.
        line: A PDFScaleLine instance to draw the lines that represent the
        timeline's scale.
    """
    def __init__(
        self,
        scale_description: ScaleDescription,
        canvas: Canvas,
        unit_label_style: ParagraphStyle,
        unit_line_length: float = DEFAULT_UNIT_LINE_LENGTH,
    ):
        """Initialise Instance.

        Args:
            scale_description: A ScaleDescription instance holding
            the settings for the scale to draw.
            canvas: A Canvas to draw the PDFEvent on.
            unit_label_style: A ParagraphStyle for the text of each unit.
            unit_line_length: A float equal to the length of lines used to
            mark each unit on the line.
        """
        self.scale_description = scale_description
        self.units = PDFScaleUnits(scale_description, unit_label_style, canvas)
        self.line = PDFScaleLine(scale_description, canvas, unit_line_length)

        if scale_description.timeline.page_orientation == "L":
            self.width = self.units.width
            self.height = self.units.height + self.line.height
        else:
            self.width = self.units.width + self.line.width
            self.height = self.units.height

        self.move(0, 0)

    def move(self, x: float, y: float):
        """Move this instance, it's units and line.

        Args:
            x: A float equal to the x coordinate of the new position.
            y: A float equal to the y coordinate of the new position.
        """
        self.x = x
        self.y = y

        self.units.x = x
        self.units.y = y

        if self.scale_description.timeline.page_orientation == "L":
            self.line.x = self.units.x + self.units.start_offset
            self.line.y = self.units.y + self.units.height
        else:
            self.line.x = self.units.x + self.units.width
            self.line.y = self.units.y + self.units.start_offset

    def draw(self):
        """Draw this instance on it's canvas."""
        self.units.draw()
        self.line.draw()

    def plot(self, time_unit: TimeUnit, pdf_event: PDFEvent) -> float:
        """Get distance relative to the start of this instance where
        PDFEvent should be positioned WRT to TimeUnit.

        Arguments:
            time_unit: A TimeUnit instance equal to the time that the event
            occurred at.
            pdf_event: A PDFEvent instance that is to be positioned.

        Returns:
            A float equal to the x or y coordinate (depending on orientation)
            that pdf_event should be positioned.
        """
        event_position = self.scale_description.plot(time_unit) * mm
        if self.scale_description.timeline.page_orientation == "L":
            return event_position + self.units.start_offset
        else:
            return (
                self.height
                - pdf_event.height
                - event_position
                - self.units.start_offset
            )
