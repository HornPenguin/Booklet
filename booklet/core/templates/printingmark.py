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
from booklet.core.manuscript import Template, Manuscript
import booklet.utils.validation as vailidation
from booklet.utils.conversion import mm
from booklet.utils.color import Basis_Colors
from booklet.utils.misc import *


class PrintingMark(Template):
    """
    Add printing markers to each page.
    """

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
        fold: bool = True,
        direction: bool = True
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
        canvas.setStrokeColor(Basis_Colors["reg"])
        canvas.setFillColor(Basis_Colors["reg"])
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
            new_pdf, new_file = self.get_new_pdf(index, manuscript, file_mode)
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
