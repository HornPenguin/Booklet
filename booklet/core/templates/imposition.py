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
from booklet.core.converters.section import SecComposition
from booklet.utils import validation
from booklet.utils.misc import *
from booklet.utils.color import hex2cmyk, rgb2cmyk


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
        imposition_layout: Union[Tuple[int, int], SecComposition] = (4, 1),
    ):

        super().__init__(direction=True)

        self.imposition = bool(imposition)
        self.gap = gap if validation.check_integer(gap, positive=True) else 0
        self.proof = proof if type(proof) == bool else False
        self.proof_color = self.___get_cmyk(proof_color)
        self.proof_width = self.gap if proof_width == None else proof_width
        self.layout = (
            imposition_layout.layout
            if isinstance(imposition_layout, SecComposition)
            else imposition_layout
        )
        self.pages_per_template = (
            self.layout.layout[0] * self.layout.layout[1] if self.layout != None else 1
        )

    def rule(
        self, i: int
    ) -> list:  # i = template page, list = manuscript pages unordered
        _i = i * self.pages_per_template
        _f = (i + 1) * self.pages_per_template
        return list(range(_i, _f))

    def position(self, i: int) -> tuple[float, float]:  # manuscript page
        index = i % self.pages_per_template
        column = self.layout.layout[1]
        row = self.layout.layout[0]

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
            return hex2cmyk(color)
        if len(color) == 3:
            return rgb2cmyk(color)
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
            proof_page.mediabox.lower_left((proof_position[0], heights[i]))
            proof_page.mediabox.upper_right(
                (proof_position[0] + proof_width, heights[i] + proof_height)
            )

        return proof_templates, tem_pdf_byte

    def do(self, index: int, manuscript: Manuscript, file_mode="safe"):

        if not self.imposition:
            return 0

        new_pdf, new_file = self.get_new_pdf(index, manuscript.tem_directory.name, file_mode)

        self.manuscript_format = manuscript.file_paper_format
        paper_width = (self.manuscript_format[0] + self.gap) * self.layout.layout[1] - (
            self.gap
        )
        paper_height = (self.manuscript_format[1] + self.gap) * self.layout.layout[0] - (
            self.gap
        )
        format = (paper_width, paper_height)

        manuscript_pages = len(manuscript.pages)
        pages_per_template = self.pages_per_template

        # template_pages - Number of pages in the output pdf
        template_pages = int(manuscript_pages / pages_per_template) + (
            1 if bool(manuscript_pages % pages_per_template) else 0
        )

        for i in range(0, template_pages):
            new_pdf.add_blank_page(format[0], format[1])

        for i in range(0, template_pages):
            # manu_pages - Which input pages appear on this output page.
            manu_pages = self.index_mapping(manuscript, i, template_pages)
            #print(f"page: {i}, manu_pages {manu_pages}")

            tem_page = new_pdf.pages[i]
            for j in manu_pages:
                page = manuscript.pages[j]
                x, y = self.position_mapping(manuscript, j, manuscript.file_pages)

                tem_page.merge_transformed_page(
                    page,
                    pypdf.Transformation().translate(
                        x,y
                    )
                )

        if self.proof:
            proof_templates, temp_file = self.generate_template(
                paper_width, paper_height, template_pages
            )
            for i in range(0, template_pages):
                page = new_pdf.pages[i]
                page.merge_page(proof_templates.pages[i])

        new_pdf.write(new_file)
        manuscript.meta["/Imposition"] = f"{self.layout.layout[0]}x{self.layout.layout[1]}"
        manuscript.pdf_update(new_pdf, new_file)
