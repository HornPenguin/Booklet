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

import os
from typing import Union, Tuple

import PyPDF2 as pypdf
import pdf2image
from booklet.dependency import img2pdf

from booklet.core.manuscript import Manuscript, Converter

from booklet.utils import validation as Validation


class ToImage(Converter):
    """
    Convert PDF to PDF whose pages are all single image each.
    """
    __name__ = "toimage"
    __description__ = "Convert PDF to PDF whose pages are all single image each"

    @property
    def name(self):
        return ToImage.__name__
    @property
    def description(self):
        return ToImage.__description__

    def __init__(self, toimage:bool = False, dpi:int=600, mode="lgpl"):
        self.toimage = bool(toimage)
        self._dpi = int(dpi) if Validation.check_integer(dpi, True) else 600
        self.mode = mode

    @property
    def dpi(self):
        return self._dpi 
    @dpi.setter
    def dpi(self, dpi):
        self._dpi = int(dpi) if Validation.check_integer(dpi, True) else 600
    
    def do(self, index:int, manuscript:Manuscript, file_mode:int):
        if not self.toimage:
            return 0

        page_images = pdf2image.convert_from_path(
            manuscript.file_path,
            dpi=self.dpi,
            fmt="png",
            use_cropbox=True,
            transparent=False,
            output_folder= manuscript.tem_directory.name
        )
        new_pdf, new_file = self.get_new_pdf(index, manuscript)
        files = [im.filename for im in page_images]
        welldid = True
        if self.mode == "lgpl": # Using img2pdf method
            try:
                with open(new_file.name, "wb") as f:
                    f.write(img2pdf.convert(files))
            except:
                welldid = False
        if not welldid: # PIL version
            files[0].save(new_file.name, save_all=True, append_images=files[1:])

        manuscript.pdf_update(None, new_file.name)

