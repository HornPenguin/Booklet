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

from booklet.core.manuscript import Manuscript, Converter
from booklet.utils.matrix import rotate_2dim

from PyPDF2 import Transformation

class Duplex(Converter):
    __name__ = "duplex"
    __description__ = "supporting for duplex printers"

    @property
    def name(self):
        return Duplex.__name__

    @property
    def description(self): 
        return Duplex.__description__
    
    def __init__(
        self,
        mode : bool = False,
        tx : int = 0,
        ty : int = 0,
        rotate: float = 0.,
        rotate_mode = "c"
        ):
        self.mode = mode if type(mode) == bool else bool(mode)
        self.tx = tx
        self.ty = ty
        self.rotate = rotate
        self.page_transformation = Transformation().translate(self.tx, self.ty).rotate(self.rotate)
        self.rotate_mode = rotate_mode
    
    def do(self, index:int, manuscript:Manuscript, file_mode):
        new_pdf, new_file = self.get_new_pdf(index, manuscript.tem_directory.name, file_mode)

        for i, page in enumerate(manuscript.pages):
            if i%2 == 1:
                l, b, r, t = page.mediaBox
                width = r-l
                height = t-b

                new_r = r
                new_t = t

                if self.rotate_mode == "c":
                    vec = [width/2, height/2]
                    vec_rotated = rotate_2dim(vec, self.rotate)
                    dx = vec[0] - vec_rotated[0]
                    dy = vec[1] - vec_rotated[1]

                elif self.rotate_mode == "b":
                    left_top = [0, height]
                    right_top = [width, height]
                    right_bottom = [width, 0]
                    left_top_rotated = rotate_2dim(left_top, self.rotate)
                    right_top_rotated = rotate_2dim(right_top, self.rotate)
                    right_bottom_rotated = rotate_2dim(right_bottom, self.rotate)

                    new_r = right_bottom_rotated[0] - left_top_rotated[0]
                    new_t = right_top_rotated[1]

                    dx = - left_top_rotated[0]
                    dy = 0

                self.page_transformation = self.page_transformation.translate(tx = dx, ty=dy)
                page.add_transformation(self.page_transformation)
                page.mediaBox.setUpperRight((new_r, new_t))

            new_pdf.add_page(page)

        manuscript.pdf_update(None, new_file.name)

                


