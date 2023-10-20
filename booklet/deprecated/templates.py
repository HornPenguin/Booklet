# Copyright (c) 2022, Hyunseong Kim <qwqwhsnote@gm.gist.ac.kr>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

# Python standard
import tempfile
from copy import copy
import io
from math import floor

# Type hint
from typing import Union, Callable, List, Tuple, Dict, Literal
from types import FunctionType
from io import BytesIO, FileIO

# PDF
import pypdf
from reportlab.pdfgen.canvas import Canvas

# Project modules
from booklet.core.manuscript import Modifier, Template, Manuscript
from booklet.converters import SigComposition
import vailidation
from booklet.utils.misc import *


# sample class for example
class Sample(Template):
    __name__ = "Sample"
    __description__ = "Sample Template works"

    @property
    def name(self):
        return Sample.__name__

    @property
    def description(self):
        return Sample.__description__

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def generate_template(self, *args):
        pass

    def do(self, index: int, manuscript: Manuscript, file_mode):
        new_pdf, new_file = self.get_new_pdf(index, manuscript.tem_directory.name, file_mode)

        # generation process

        new_pdf.write(new_file)
        manuscript.pdf_update(new_pdf, new_file)


class Imposition(Template):
    __name__ = "Imposition"
    __description__ = "Imposition work"

    @property
    def name(self):
        return Imposition.__name__

    @property
    def description(self):
        return Imposition.__description__

    def __init__(
        self,
        imposition: bool = True,
        gap: int = 0,  # pts
        proof: bool = False,
        proof_color: Tuple[float, float, float, float] = (0, 0, 0, 0),
        proof_width: Union[None, int] = None,
        imposition_layout: Union[Tuple[int, int], SigComposition] = (4, 1),
    ):

        super().__init__(direction=True)

        self.imposition = bool(imposition)
        self.gap = gap if vailidation.check_integer(gap, positive=True) else 0
        self.proof = proof if type(proof) == bool else False
        self.proof_color = self.___get_cmyk(proof_color)
        self.proof_width = self.gap if proof_width == None else proof_width
        self.layout = (
            imposition_layout.layout
            if isinstance(imposition_layout, SigComposition)
            else imposition_layout
        )
        self.pages_per_template = (
            self.layout[0] * self.layout[1] if self.layout != None else 1
        )

    def rule(
        self, i: int
    ) -> list:  # i = template page, list = manuscript pages unordered
        _i = i * self.pages_per_template
        _f = (i + 1) * self.pages_per_template
        return list(range(_i, _f))

    def position(self, i: int) -> tuple[float, float]:  # manuscript page
        index = i % self.pages_per_template
        column = self.layout[1]
        row = self.layout[0]

        x = (index) % column
        y = row - floor((index) / column) - 1
        x_pos = (self.manuscript_format[0] + self.gap) * x - (
            self.gap if x > column - 1 else 0
        )
        y_pos = (self.manuscript_format[1] + self.gap) * y - (
            self.gap if y > row - 1 else 0
        )

        return (x_pos, y_pos)

    # Internal routines
    def ___get_cmyk(self, color) -> Tuple[float, float, float, float]:
        if type(color) == str:
            return Conversion.hex_to_cmyk(color)
        if len(color) == 3:
            return Conversion.hex_to_cmyk(Conversion.rgb_to_hex(color))
        elif len(color) == 4:
            return color

    def generate_template(self, paper_width, paper_height, template_pages):
        tem_pdf_byte = io.BytesIO()
        template_proof = Canvas(tem_pdf_byte, pagesize=(paper_width, paper_height))

        proof_height = 2 * self.manuscript_format[1] / template_pages
        proof_width = self.proof_width
        # position
        x_center = self.manuscript_format[0] + self.gap / 2
        x_position = x_center - proof_width / 2
        y_position = paper_height - proof_height
        proof_position = [x_position, y_position]
        c, m, y, k = self.proof_color
        template_proof.setLineWidth(0)
        template_proof.setFillColorCMYK(c, m, y, k)

        heights = []

        for i in range(0, template_pages):
            heights.append(proof_position[1])
            if i % 2 == 0:
                template_proof.setLineWidth(0)
                template_proof.setFillColorCMYK(c, m, y, k)
                template_proof.rect(
                    proof_position[0],
                    proof_position[1],
                    proof_width,
                    proof_height,
                    fill=1,
                )
                proof_position[1] -= proof_height
            template_proof.showPage()

        template_proof.save()
        tem_pdf_byte.seek(0)
        proof_templates = pypdf.PdfReader(tem_pdf_byte)

        for i in range(0, template_pages):
            proof_page = proof_templates.pages[i]
            proof_page.mediabox.setLowerLeft((proof_position[0], heights[i]))
            proof_page.mediabox.setUpperRight(
                (proof_position[0] + proof_width, heights[i] + proof_height)
            )

        return proof_templates, tem_pdf_byte

    def do(self, index: int, manuscript: Manuscript, file_mode="safe"):

        if not self.imposition:
            return 0

        new_pdf, new_file = self.get_new_pdf(index, manuscript.tem_directory.name, file_mode)

        self.manuscript_format = manuscript.file_paper_format
        paper_width = (self.manuscript_format[0] + self.gap) * self.layout[1] - (
            self.gap
        )
        paper_height = (self.manuscript_format[1] + self.gap) * self.layout[0] - (
            self.gap
        )
        format = (paper_width, paper_height)

        manuscript_pages = len(manuscript.pages)
        pages_per_template = self.pages_per_template

        template_pages = int(manuscript_pages / pages_per_template) + (
            1 if bool(manuscript_pages % pages_per_template) else 0
        )

        for i in range(0, template_pages):
            new_pdf.add_blank_page(format[0], format[1])

        for i in range(0, template_pages):
            manu_pages = self.index_mapping(manuscript, i, template_pages)

            tem_page = new_pdf.pages[i]
            for j in manu_pages:
                page = manuscript.pages[j]
                x, y = self.position_mapping(manuscript, j, manuscript.file_pages)

                tx = x
                ty = y

                page_translate = pypdf.Transformation().translate(tx=tx, ty=ty)
                page.add_transformation(page_translate)
                page.mediaBox.setLowerLeft((tx, ty))
                upr = (tx + self.manuscript_format[0], ty + self.manuscript_format[1])
                page.mediaBox.setUpperRight(upr)

                tem_page.merge_page(page)

        if self.proof:
            proof_templates, temp_file = self.generate_template(
                paper_width, paper_height, template_pages
            )
            for i in range(0, template_pages):
                page = new_pdf.pages[i]
                page.merge_page(proof_templates.pages[i])

        new_pdf.write(new_file)
        manuscript.meta["/Imposition"] = f"{self.layout[0]}x{self.layout[1]}"
        manuscript.pdf_update(new_pdf, new_file)


class PrintingMark(Template):
    __name__ = "printing mark"
    __desciprtion__ = "Add printing marks to manuscript"

    @property
    def name(self):
        return PrintingMark.__name__

    @property
    def description(self):
        return PrintingMark.__desciprtion__

    def __init__(
        self,
        on: bool = False,
        margin: int = 43,  # pts
        crop: bool = True,
        reg: bool = True,
        cmyk: bool = True,
    ):

        self.on = on if type(on) == bool else False
        self.margin = margin if margin != None else 43
        self.crop = bool(crop)
        self.reg = bool(reg)
        self.cmyk = bool(cmyk)

        super().__init__(direction=True)

    def ____basic_position(
        self, pagesize: Tuple[float, float]
    ) -> Tuple[
        Tuple[float, float, float, float], Tuple[Tuple[float, float, float, float]]
    ]:
        x1 = self.margin * 0.25
        x2 = self.margin + pagesize[0] + x1
        y1 = self.margin + pagesize[1]
        y2 = self.margin

        x3 = y2
        x4 = x2 - x1
        y3 = x1
        y4 = y1 + y3

        return [[x1, x2, x3, x4], [y1, y2, y3, y4]]

    def __get_paper_dim(self, pagesize: Tuple[float, float]) -> Tuple[float, float]:
        width, height = pagesize
        x = 2 * self.margin + width
        y = 2 * self.margin + height
        return x, y

    def __draw_crop_lines(self, canvas: Canvas, positions: list = []) -> bool:
        if self.crop:
            if len(positions) == 0:
                positions = self.___get_crop_line_positions(self.manu_paper_format)
            canvas.setLineWidth(0.5 * mm)
            canvas.lines(positions)
            return True
        return False

    def __draw_registration(
        self, canvas: Canvas, ratio: float = 0.8, positions: list = []
    ) -> bool:
        self.reg_l = 0
        pagesize = self.manu_paper_format
        if self.reg:
            self.reg_l = l = ratio * self.margin
            center = self.margin / 2
            if len(positions) == 0:
                positions = self.___get_registeration_positions(l, center, pagesize)
            for position in positions:
                self.___draw_registration_mark(
                    canvas=canvas, x=position[0], y=position[1], l=l
                )
            return True
        return False

    def __draw_color_marker(self, canvas: Canvas) -> bool:
        if self.cmyk:
            cyan = [(0.2 * (1 + i), 0, 0, 0) for i in range(0, 5)]
            magenta = [(0, 0.2 * (1 + i), 0, 0) for i in range(0, 5)]
            yellow = [(0, 0, 0.2 * (1 + i), 0) for i in range(0, 5)]
            black = [(0, 0, 0, 0.2 * (1 + i)) for i in range(0, 5)]

            color_sequence = [
                (1, 0, 0, 0),
                (1, 1, 0, 0),
                (0, 1, 0, 0),
                (0, 1, 1, 0),
                (0, 0, 1, 0),
                (1, 0, 1, 0),
                (1, 0, 0, 0),
            ]

            color_row1 = cyan + magenta
            color_row2 = yellow + black
            pagesize = self.manu_paper_format
            (
                vertical,
                case,
                origin,
                origin_s,
                length,
            ) = self.___get_color_marker_position_and_length(
                pagesize, padding_ratio=0.15
            )

            row, column = case.split("x")

            row = int(row)
            column = int(column)
            color_map = (
                [color_row1, color_row2] if row == 2 else [color_row1 + color_row2]
            )

            if not vertical:
                column, row = row, column
                color_map = List12dim.transpose(color_map)

            for i in range(0, row):
                for j in range(0, column):
                    square_coordinate = (origin[0] + length * i, origin[1] + length * j)
                    color = color_map[i][j]
                    c, m, y, k = color
                    canvas.saveState()
                    canvas.setLineWidth(0)
                    canvas.setFillColorCMYK(c, m, y, k)
                    canvas.setStrokeColorCMYK(0, 0, 0, 0)
                    canvas.rect(
                        square_coordinate[0],
                        square_coordinate[1],
                        length,
                        length,
                        stroke=1,
                        fill=1,
                    )
                    canvas.restoreState()
            origin_s
            for k in range(0, len(color_sequence)):
                i, j = (0 if vertical else k, k if vertical else 0)
                square_coordinate = (origin_s[0] + i * length, origin_s[1] + j * length)
                color = color_sequence[k]
                c, m, y, k = color
                canvas.saveState()
                canvas.setLineWidth(0)
                canvas.setFillColorCMYK(c, m, y, k)
                canvas.setStrokeColorCMYK(0, 0, 0, 0)
                canvas.rect(
                    square_coordinate[0],
                    square_coordinate[1],
                    length,
                    length,
                    stroke=1,
                    fill=1,
                )
                canvas.restoreState()

            return True
        return False

    def ___get_crop_line_positions(
        self, pagesize: Tuple[float, float]
    ) -> list[
        Tuple[float, float, float, float],
        Tuple[float, float, float, float],
        Tuple[float, float, float, float],
        Tuple[float, float, float, float],
    ]:
        trim_l = self.margin * 0.5
        x, y = self.____basic_position(pagesize)
        return [
            (x[0], y[0], x[0] + trim_l, y[0]),  # h, u l
            (x[0], y[1], x[0] + trim_l, y[1]),  # h, d l
            (x[1], y[0], x[1] + trim_l, y[0]),  # h, u r
            (x[1], y[1], x[1] + trim_l, y[1]),  # h, d r
            (x[2], y[3], x[2], y[3] + trim_l),  # v, u l
            (x[2], y[2], x[2], y[2] + trim_l),  # v, d l
            (x[3], y[3], x[3], y[3] + trim_l),  # v, u r
            (x[3], y[2], x[3], y[2] + trim_l),  # v, d r
        ]

    def ___get_registeration_positions(
        self, l: float, center: float, pagesize: Tuple[float, float]
    ) -> list[
        Tuple[float, float],
        Tuple[float, float],
        Tuple[float, float],
        Tuple[float, float],
        Tuple[float, float],
        Tuple[float, float],
        Tuple[float, float],
        Tuple[float, float],
    ]:
        x, y = self.____basic_position(pagesize)
        trim_l = self.margin / 2
        return [
            (center - l / 2, y[0] - center - l),
            (center - l / 2, y[1] + center),
            (x[1] + trim_l / 2 - l / 2, y[0] - center - l),
            (x[1] + trim_l / 2 - l / 2, y[1] + center),
            (x[2] + center, y[3] + trim_l / 2 - l / 2),
            (x[2] + center, center - l / 2),
            (x[3] - center - l, y[3] + trim_l / 2 - l / 2),
            (x[3] - center - l, center - l / 2),
        ]

    def ___get_color_marker_position_and_length(
        self, pagesize: Tuple[float, float], padding_ratio: float
    ) -> Tuple[list, Literal["2x10", "1x20"], list, list, float]:

        # Calculate side and head size and choose bigger one.
        pa = padding_ratio * self.margin
        hor = pagesize[0] - 2 * self.reg_l - self.margin
        ver = pagesize[1] - 2 * self.reg_l - self.margin

        if 2 * pa > hor or 2 * pa > ver:
            pa_t = padding_ratio * min(hor, ver)
        else:
            pa_t = pa
        vertical = True

        if ver < hor:
            vertical = False
            space_size = (hor - 2 * pa_t, self.margin - 2 * pa)
            origin = [self.margin * 1.5 + self.reg_l + pa_t, 0]

        else:
            space_size = (self.margin - 2 * pa, ver - 2 * pa_t)
            origin = [0, self.margin * 1.5 + self.reg_l + pa_t]

        # Fit 2x10, 1x20 to the empty space and calculate square size(min(width, height) respectively)
        # and choose bigger size
        # 2x10 case
        if vertical:
            dim2 = space_size[0] * 0.5
            dim10 = space_size[1] * 0.1
        else:
            dim2 = space_size[1] * 0.5
            dim10 = space_size[0] * 0.1
        dim2_10 = min(dim2, dim10)
        # 1x32 case
        if vertical:
            dim1 = space_size[0]
            dim20 = space_size[1] * 0.05
        else:
            dim1 = space_size[1]
            dim20 = space_size[0] * 0.05
        dim1_20 = min(dim1, dim20)

        square_length = max(dim2_10, dim1_20)
        case = "2x10" if dim2_10 > dim1_20 else "1x20"

        padding = self.margin / 2 - (
            square_length if case == "2x10" else square_length / 2
        )
        if ver < hor:
            origin[1] = padding
        else:
            origin[0] = padding

        # origin_mixed = (self.margin+hor+2*self.reg_l+pa, self.margin+pa) if vertical else (self.margin +pa, self.margin+ ver + 2*self.margin+ pa)
        origin_mixed = copy(origin)
        if ver < hor:
            origin_mixed[1] = self.margin * 1.5 + pagesize[1] - square_length * 0.5
        else:
            origin_mixed[0] = self.margin * 1.5 + pagesize[0] - square_length * 0.5

        return vertical, case, origin, origin_mixed, square_length

    def ___draw_registration_mark(
        self, canvas: Canvas, x: float, y: float, l: float
    ) -> NoReturn:
        def get_abpath4(x0, y0, x1, y1):
            return (x + x0, y + y0, x + x1, y + y1)

        def get_abpath2(x0, y0):
            return x + x0, y + y0

        line_t = l / 15  # /25
        line_l = l * (3 / 16)
        circle_r1 = l * (5 / 16) - line_t
        circle_r2 = circle_r1 - line_t * (1.5)

        lines = [
            get_abpath4(0, l / 2, line_l, l / 2),
            get_abpath4(l - line_l, l / 2, l, l / 2),
            get_abpath4(l / 2, 0, l / 2, line_l),
            get_abpath4(l / 2, l - line_l, l / 2, l),
        ]
        canvas.setLineWidth(line_t)
        canvas.setStrokeColor(registration_black)
        canvas.setFillColor(registration_black)
        # Draw cross line
        canvas.lines(lines)
        # Outer circle parts
        arcs_outer = canvas.beginPath()
        c = l / 2 - line_t / 2
        a = c - circle_r1
        b = c + circle_r1
        x1, y1 = get_abpath2(
            a, a
        )  # Same relative coordinate values are not same in abs different basis
        x2, y2 = get_abpath2(b, b)
        arcs_outer.arc(x1, y1, x2, y2, startAng=180, extent=90)
        arcs_outer.arc(x1 + line_t, y1, x2 + line_t, y2, startAng=270, extent=90)
        arcs_outer.arc(
            x1 + line_t, y1 + line_t, x2 + line_t, y2 + line_t, startAng=0, extent=90
        )
        arcs_outer.arc(x1, y1 + line_t, x2, y2 + line_t, startAng=90, extent=90)
        canvas.drawPath(arcs_outer, fill=0, stroke=1)

        # inner circle parts
        arcs_inner = canvas.beginPath()
        a = c - circle_r2
        b = c + circle_r2
        x1, y1 = get_abpath2(a, a)
        x2, y2 = get_abpath2(b, b)
        xc, yc = get_abpath2(l / 2, l / 2)
        d = line_t / 2
        arcs_inner.moveTo(xc - d, yc - d)
        arcs_inner.arcTo(x1, y1, x2, y2, startAng=180, extent=90)
        arcs_inner.moveTo(xc + d, yc - d)
        arcs_inner.arcTo(x1 + line_t, y1, x2 + line_t, y2, startAng=270, extent=90)
        arcs_inner.moveTo(xc + d, yc + d)
        arcs_inner.arcTo(
            x1 + line_t, y1 + line_t, x2 + line_t, y2 + line_t, startAng=0, extent=90
        )
        arcs_inner.moveTo(xc - d, yc + d)
        arcs_inner.arcTo(x1, y1 + line_t, x2, y2 + line_t, startAng=90, extent=90)

        canvas.drawPath(arcs_inner, fill=1, stroke=0)

    def generate_template(
        self, manuscript: Manuscript
    ) -> Tuple[pypdf.PdfFileReader, BytesIO]:
        self.manu_paper_format = manuscript.file_paper_format
        paper_format = self.__get_paper_dim(self.manu_paper_format)

        tem_byte = io.BytesIO()
        printing_template = Canvas(tem_byte, pagesize=paper_format)

        if self.crop:
            self.__draw_crop_lines(printing_template)
        if self.reg:
            self.__draw_registration(printing_template)
        if self.cmyk:
            self.__draw_color_marker(printing_template)
        printing_template.showPage()
        printing_template.save()

        tem_byte.seek(0)
        template_pdf = pypdf.PdfFileReader(tem_byte)

        return template_pdf, tem_byte

    def do(
        self, index: int, manuscript: Manuscript, file_mode: str = "safe"
    ) -> NoReturn:

        if not self.on:
            pass
        else:
            new_pdf, new_file = self.get_new_pdf(index, manuscript.tem_directory.name, file_mode)
            template_pdf, tem_byte = self.generate_template(manuscript)
            template = template_pdf.pages[0]
            for i, page in enumerate(manuscript.pages):
                temp_page = copy(template)
                page.addTransformation(
                    pypdf.Transformation().translate(tx=self.margin, ty=self.margin)
                )
                upper = float(page.mediaBox[2])
                right = float(page.mediaBox[3])
                page.mediaBox.setUpperRight((upper + self.margin, right + self.margin))

                temp_page.merge_page(page)
                new_pdf.add_page(temp_page)

            new_pdf.write(new_file)

            manuscript.pdf_update(new_pdf, new_file)


# In working
class Note(Template):
    __name__ = "note"
    __desciprtion__ = "Expand and add note characters to manuscript"

    @property
    def name(self):
        return Note.__name__

    @property
    def description(self):
        return Note.__desciprtion__

    def __init__(
        self,
        numbering: bool = True,
        targets: Literal["Both", "Odd", "Even", "Odd(only)", "Even(only)"] = "Both",
        location: Literal["H", "F", "HF", "FH"] = "H",
        align: Literal[
            "L", "R", "C", "LR", "CC", "RL", "LL", "LC", "RR", "RC", "CL", "CR"
        ] = "LR",
        margin: float = 8.0,
        font: str = "Helvetica",
        fontsize: int = 12.0,
    ):

        self.numbering = numbering if type(numbering, bool) else True
        self.targets = targets
        self.location = (
            (location[0], location[1]) if len(align) != 1 else (location, location)
        )
        self.align = (align[0], align[1]) if len(align) != 1 else (align, align)

        pass

    def rule(
        self, i: int
    ) -> list:  # i = template page, list = manuscript pages unordered
        _i = i * self.pages_per_template
        _f = (i + 1) * self.pages_per_template
        return list(range(_i, _f))

    def generate_template(
        self, manuscript: Manuscript
    ) -> Tuple[pypdf.PdfFileReader, BytesIO]:
        self.manu_paper_format = manuscript.file_paper_format
        return template_pdf, tem_byte

    def do(
        self, index: int, manuscript: Manuscript, file_mode: str = "safe"
    ) -> NoReturn:
        if not self.on:
            pass
        else:
            new_pdf, new_file = self.get_new_pdf(index, manuscript.tem_directory.name, file_mode)

            # Expand pages

            template_pdf, tem_byte = self.generate_template(manuscript)
            for i, page in enumerate(template_pdf):
                pass

            new_pdf.write(new_file)
            manuscript.pdf_update(new_pdf, new_file)
            pass


if __name__ == "__main__":
    pass
