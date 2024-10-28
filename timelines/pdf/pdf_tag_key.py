from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from reportlab.lib.units import mm
from .area import Area


TAG_KEY_COLUMN_WIDTH = 70 * mm


class PDFParagraph(Area):
    def __init__(
        self,
        text: str,
        canvas: Canvas,
        style: ParagraphStyle,
        max_width: float,
    ):
        self.canvas = canvas
        self.x = 0
        self.y = 0

        self.paragraph: Paragraph = Paragraph(text, style)
        self.width, self.height = self.paragraph.wrapOn(
            self.canvas, max_width, 0
        )

    def draw(self):
        self.paragraph.drawOn(self.canvas, self.x, self.y)


class PDFTagKey(Area):
    def __init__(
        self,
        tags,
        canvas: Canvas,
        heading_style: ParagraphStyle,
        tag_style: ParagraphStyle,
        max_width: float,
        border_size: float,
        column_count: int = 1
    ):
        if max_width < 0:
            raise ValueError(
                "max_width must be greater than 0"
            )

        if border_size < 0:
            raise ValueError(
                "border_size must be greater than 0"
            )

        if column_count < 1:
            raise ValueError(
                "columns must be 1 or greater"
            )

        self.canvas = canvas
        self.x = 0
        self.y = 0

        max_heading_width = (max_width - (2 * border_size))
        self.heading_paragraph = PDFParagraph(
            "Tag Key",
            canvas,
            heading_style,
            max_heading_width
        )
        self.heading_paragraph.x = border_size
        self.heading_paragraph.y = border_size

        self.rows = []

        # create tag paragraphs
        max_tag_paragraph_width = (
            (max_width - ((column_count + 1) * border_size))
            / column_count
        )

        self.rows, row_heights, total_row_height = self.__make_tags(
            tags,
            column_count,
            canvas,
            tag_style,
            max_tag_paragraph_width,
        )

        # calculate total height
        total_height = (
            self.heading_paragraph.height
            + total_row_height
            + ((2 + len(self.rows)) * border_size)
        )

        # position heading paragraph
        self.heading_paragraph.y = (
            total_height - border_size - self.heading_paragraph.height
        )

        self.__position_tags(border_size, row_heights, max_tag_paragraph_width)

        # set dimensions
        self.width = max_width
        self.height = total_height

    def __make_tags(
        self,
        tags,
        column_count,
        canvas,
        tag_style,
        max_tag_paragraph_width
    ):
        rows = []
        tag_count = 0
        row_count = 0
        row_height = 0
        total_row_height = 0
        row_heights = []

        for tag in tags:
            column_index = tag_count % column_count
            tag_count += 1

            new_row = column_index == 0
            if new_row:
                row_count += 1
                row_height = 0
                rows.append([])

            # create tag paragraph
            if tag.description != "":
                tag_string = f"{tag.name} : {tag.description}"
            else:
                tag_string = tag.name

            tag_paragraph = PDFParagraph(
                tag_string,
                canvas,
                tag_style,
                max_tag_paragraph_width
            )
            rows[row_count-1].append(tag_paragraph)

            # get highest paragraph in row
            if tag_paragraph.height > row_height:
                row_height = tag_paragraph.height

            end_of_row = column_index == (column_count - 1)
            last_tag = tag_count == len(tags)
            if end_of_row or last_tag:
                total_row_height += row_height
                row_heights.append(row_height)

        return rows, row_heights, total_row_height

    def __position_tags(
        self,
        border_size,
        row_heights,
        max_tag_paragraph_width
    ):
        row_index = 0
        start_y = self.heading_paragraph.y
        for row in self.rows:
            column_index = 0
            start_y -= (border_size + row_heights[row_index])
            for tag_paragraph in row:
                x = (
                    border_size
                    + (column_index * (border_size + max_tag_paragraph_width))
                )
                y = start_y + row_heights[row_index] - tag_paragraph.height
                tag_paragraph.x = x
                tag_paragraph.y = y
                column_index += 1
            row_index += 1

    def draw(self):
        self.canvas.saveState()
        self.canvas.translate(self.x, self.y)

        self.heading_paragraph.draw()
        for row in self.rows:
            for tag_paragraph in row:
                tag_paragraph.draw()

        self.canvas.restoreState()
