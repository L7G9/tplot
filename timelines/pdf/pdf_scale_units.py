"""Contains class to draw timeline's scale units on a Canvas.

Classes:
    PDFScaleUnits
"""

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from .area import Area
from .pdf_scale_unit_label import PDFScaleUnitLabel
from .scale_description import ScaleDescription


class PDFScaleUnits(Area):
    """Class to measure dimensions of and draw the units on a timeline's
    scale.

    Extends:
        Area

    Attributes:
        scale_description: A ScaleDescription instance holding the settings
        of the scale to draw.
        style: A ParagraphStyle for the text of each unit label.
        canvas: A Canvas to draw the PDFScaleLine on.
        init_labels: A list of PDFScaleUnitLabel instances
        start_offset: A float equal to distance (x or y depending on
        timeline orientation) to center of first until label, used to
        correctly position the a scale line.
    """

    def __init__(
        self,
        scale_description: ScaleDescription,
        style: ParagraphStyle,
        canvas: Canvas,
    ):
        """Initialise Instance.

        Args:
            scale_description: A ScaleDescription instance holding the
            settings of the scale to draw.
            style: A ParagraphStyle for the PDFScaleUnitLabel instances
            created in unit_labels.
            canvas: A Canvas to draw the PDFScaleUnits on.
        """
        self.x = 0
        self.y = 0

        self.scale_description = scale_description
        self.style = style
        self.canvas = canvas
        self.unit_labels = []
        self.start_offset = 0

        scale_line_length = scale_description.get_scale_unit_length() * mm
        distance_between_label_centers = (
            scale_line_length / scale_description.get_scale_units()
        )

        if self.scale_description.timeline.page_orientation == "L":
            self.__landscape_init(
                scale_line_length, distance_between_label_centers
            )
        else:
            self.__portrait_init(
                scale_line_length, distance_between_label_centers
            )

    def __landscape_init(
        self, scale_line_length, distance_between_label_centers
    ):
        """Creates and positions the required labels for a landscape timeline
        then sets the dimensions of the area surrounding them."""
        max_label_width = distance_between_label_centers - (2 * mm)
        max_label_height = 0

        for i in range(self.scale_description.get_scale_units() + 1):
            unit_label = PDFScaleUnitLabel(
                self.scale_description.get_scale_label(i),
                self.style,
                self.canvas,
                max_label_width,
            )
            self.unit_labels.append(unit_label)
            if unit_label.height > max_label_height:
                max_label_height = unit_label.height

        start_offset = self.unit_labels[0].width / 2
        end_offset = self.unit_labels[-1].width / 2
        total_width = start_offset + scale_line_length + end_offset

        self.width = total_width
        self.height = max_label_height
        self.start_offset = start_offset

        for i in range(self.scale_description.get_scale_units() + 1):
            x_pos = start_offset + (i * distance_between_label_centers)
            y_pos = max_label_height - self.unit_labels[i].height
            self.unit_labels[i].set_landscape_position(x_pos, y_pos)

    def __portrait_init(
        self, scale_line_length, distance_between_label_centers
    ):
        """Creates and positions the required labels for a portrait timeline
        then sets the dimensions of the area surrounding them."""
        # TODO - move to const
        max_label_width = 30 * mm
        calculated_max_label_width = 0

        for i in range(self.scale_description.get_scale_units() + 1):
            unit_label = PDFScaleUnitLabel(
                self.scale_description.get_scale_label(i),
                self.style,
                self.canvas,
                int(max_label_width),
            )
            self.unit_labels.append(unit_label)
            if unit_label.width > calculated_max_label_width:
                calculated_max_label_width = unit_label.width

        start_offset = self.unit_labels[0].height / 2
        end_offset = self.unit_labels[-1].height / 2
        total_height = start_offset + scale_line_length + end_offset

        self.width = calculated_max_label_width
        self.height = total_height
        self.start_offset = start_offset

        for i in range(self.scale_description.get_scale_units() + 1):
            x_pos = calculated_max_label_width
            y_pos = (
                start_offset
                + scale_line_length
                - (i * distance_between_label_centers)
            )
            self.unit_labels[i].set_portrait_position(x_pos, y_pos)

    def draw(self):
        """Draw this instance on it's canvas."""
        self.canvas.saveState()
        self.canvas.translate(self.x, self.y)

        for i in range(self.scale_description.get_scale_units() + 1):
            self.unit_labels[i].draw()

        for unit_label in self.unit_labels:
            unit_label.draw()

        self.canvas.restoreState()
