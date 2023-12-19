from reportlab.lib.units import mm
from .area import Area
from .pdf_scale_line import PDFScaleLine
from .pdf_scale_units import PDFScaleUnits
from .pdf_event import PDFEvent


DEFAULT_UNIT_LINE_LENGTH = 5 * mm


class PDFScale(Area):
    """Class to measure dimensions of and draw a timeline's scale."""

    def __init__(
        self,
        scale_description,
        canvas,
        unit_label_style,
        unit_line_length=DEFAULT_UNIT_LINE_LENGTH,
    ):
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

    def move(self, x, y):
        """Update"""
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
        self.units.draw()
        self.line.draw()

    def plot(self, time_unit, pdf_event: PDFEvent) -> float:
        print(f"plot {time_unit} {pdf_event}")
        event_position = self.scale_description.plot(time_unit) * mm
        print(f"event_position = {event_position/mm}")
        if self.scale_description.timeline.page_orientation == "L":
            return event_position + self.units.start_offset
        else:
            print(f"self.height = {self.height}")
            print(f"pdf_event.height = {pdf_event.height}")
            print(f"event_position = {event_position}")
            print(f"self.units.start_offset = {self.units.start_offset}")
            return (
                self.height
                - pdf_event.height
                - event_position
                - self.units.start_offset
            )
