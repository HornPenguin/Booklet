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
import platform, os, io

import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageDraw, ImageFont
from fontTools import ttLib

font_formats = [".ttc", ".ttf", ".otf", ".ttz", ".woff", ".woff2"]  # only true types
platform_type = platform.system()
pathjoin = lambda *paths: os.path.join(*paths)

font_paths = {  # Search path
    "Darwin": [
        pathjoin("/Library", "Fonts"),
        pathjoin("/Network", "Library", "Fonts"),
        pathjoin("/System", "Library", "Fonts"),
        pathjoin(os.path.expanduser("~"), "Library", "Fonts"),
    ],
    "Linux": [
        pathjoin("/usr", "share", "fonts", "truetype"),
        pathjoin("/usr", "share", "fonts", "opentype"),
        pathjoin("/usr", "share", "fonts", "dejavu"),
        pathjoin("/usr", "share", "fonts"),
        pathjoin("/usr", "lib", "X11", "fonts", "TrueType"),
    ],
    "Windows": [
        pathjoin("C:\\Windows", "Fonts"),
        pathjoin("C:\\WinNT", "fonts"),  # for Window XP, but who will use it?
    ],
}

def __get_font_info(file, path):
    def get_info(font):
        # See https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6name.html
        # or https://docs.microsoft.com/en-us/typography/opentype/spec/name#name-ids
        name_codes = [
            16,
            1,
        ]
        code = (
            name_codes[0]
            if font["name"].getDebugName(name_codes[0]) != None
            else name_codes[1]
        )
        if font["name"].getDebugName(code) == None:
            return None, None

        family = font["name"].getDebugName(code)
        subfamily = font["name"].getDebugName(code + 1)
        if subfamily == None:
            filename = os.path.splitext(os.path.split(path)[1])[0]
            if "-" in filename:
                subfamily = filename.split("-")[1]
            elif (
                filename.replace(family, "") != filename
                and len(filename.replace(family, "")) > 0
            ):
                subfamily = filename.replace(family, "")
        return family, subfamily

    if "ttc" in file:  # Font collection
        tfonts = ttLib.TTCollection(path)
        font_info_list = []
        for tfont in tfonts:
            name, suffix = get_info(tfont)
            font_info_list.append((name, suffix))
        return font_info_list

    else:
        tfont = ttLib.TTFont(path)
        font_info_list = [get_info(tfont)]

    return font_info_list


def get_system_fonts():
    font_directory = font_paths[platform_type]
    font_database = {}
    tem_font_files = []

    for font_direct in font_directory:
        for i, (root, dirs, files) in enumerate(os.walk(font_direct)):
            tem_font_files.append({"root": root, "files": files})

    for font_files in tem_font_files:
        root = font_files["root"]
        files = font_files["files"]
        for file in files:
            if os.path.splitext(file)[1] in font_formats:
                font_file_path = pathjoin(root, file)
                font_infos = __get_font_info(file, font_file_path)
                for font_info in font_infos:
                    if font_info[0] == None:
                        continue
                    font_name = font_info[0]
                    suffixs = font_info[1]
                    if font_name not in font_database.keys():
                        font_database[font_name] = {suffixs: font_file_path}
                    else:
                        font_database[font_name][suffixs] = font_file_path


    return dict(sorted(font_database.items()))


def get_font_file(name, suffix):
    system_fonts = get_system_fonts()
    if name not in system_fonts.keys():
        raise ValueError(f"Name is not in font_database")
    if suffix not in system_fonts[name].keys():
        raise ValueError(f"Invaild suffix: {system_fonts[name].keys()}")

    fontname = f"{name}-{suffix}"
    filepath = system_fonts[name][suffix]

    return fontname, filepath


def get_font_file_without_s(name):
    name_font, suffix = name.split("-")
    return get_font_file(name_font, suffix)
 
# https://stackoverflow.com/questions/4190667/how-to-get-width-of-a-truetype-font-character-in-1200ths-of-an-inch-with-python
# by dawid
def get_text_dim(string, font_file: str, size):
    im_width = len(string) * size
    im_height = size
    bg_color = (0, 0, 0)

    # Generate string as image
    im = Image.new("RGB", (im_width, im_height), bg_color)
    draw = ImageDraw.Draw(im)
    font_PIL = ImageFont.truetype(font_file, size)
    draw.text((0, 0), string, font=font_PIL, fill=(255, 255, 255))
    bbox = im.getbbox()  # left, upper, right, and lower pixel coordinate

    width = bbox[2] + bbox[0]
    height = bbox[3] + int(bbox[1] / 2)
    return width, height


def get_number_dims(font, size):
    dims = {}
    for i in range(0, 10):
        width, height = get_text_dim(str(i), font, size)
        dims[i] = (width, height)
    d_max = max([x[0] for x in dims.values()])
    return (font, size, dims, d_max)


def cal_num_width(num_string, widths=None, simple=True, d_max=None):
    # same work with get_text_width() but very efficient for number string using precalculated ditionary.
    if widths == None:
        raise ValueError("No table is given. Argument 'widths' is None")
    if type(num_string) == int:
        num_string = str(num_string)
    if simple:
        if d_max == None:
            d_max = max([x[0] for x in widths.values()])
        length = len(num_string) * d_max
    else:
        length = 0
        for i in range(0, 10):
            rep = num_string.count(str(i))
            length += rep * widths[i][0]
    return length


# tktiner foont dialog

class tkFontdialog(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent

        self.system_fonts = font_database
        self.fontfile:str
        self.fonttype:str
        self.size:float
        self.italic:bool
        self.bold:bool
    
        self.system_fonts_Combobox = ttk.Combobox(self, values=)