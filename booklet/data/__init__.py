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

import os
from pathlib import Path

from PIL import Image

from booklet.utils.misc import get_base_path, resources_path
from booklet.utils.images import icon_path


des = """PDF modulation for printing and press----------------------------------------------------"""
epi = (
    "github: https://github.com/HornPenguin/Booklet \nsupport: support@hornpenguin.com"
)

# File path
BASE_PATH  = get_base_path()
PATH_RESOURCE = BASE_PATH/"resources"
PATH_TEXT = PATH_RESOURCE/"text"
PATH_SOUND = PATH_RESOURCE/"sound"
PATH_LANGUAGE = PATH_RESOURCE/"language"
PATH_IMAGE = PATH_RESOURCE/"image"
PATH_ADD_THEME = PATH_RESOURCE/"add_theme"
PATH_ADD_THEME_BUTTONS = PATH_ADD_THEME/"buttons"


# Resources
TK_THEME = "azure.tcl" 
button_files = [
    "up",
    "down",
    "delete",
    "delete_all",
    "sort_up",
    "sort_down"
]
button_size = (35, 35)
__temp_1 = { name: Image.open(PATH_ADD_THEME_BUTTONS/f"{name}.png").resize(button_size,Image.Resampling(1)) for name in button_files}
__temp_2 = { f"{name}_hover" : Image.open(PATH_ADD_THEME_BUTTONS/f"{name}_hover.png").resize((30, 30),Image.Resampling(1)) for name in button_files }

button_icons = {**__temp_1, **__temp_2}
# -Audio file
beep_file = PATH_SOUND/"beep_ping.wav"

# -Images
task_bar_icon = icon_path
logo_width = logo_height = 70
logo = Image.open(PATH_IMAGE/"logo.png").resize(
    (logo_width, logo_height), Image.Resampling(1)
)
icon_images = {
    "imposition": ["imposition", "split"],
    "printing" : ["proof", "cmyk", "registration", "crop"]
}
#imposition_icons = {
#    name: Image.open(PATH_IMAGE/f"{name}.png") for name in icon_images["imposition"]
#}
#printing_icons = {
#    name: Image.open(PATH_IMAGE/f"{name}.png") for name in icon_images["printing"]
#}
#icons = {**imposition_icons, **printing_icons}
icons = {}
# Regular expression
re_get_ranges = r"([ ]{0,}\d+[ ]{0,}-{1,1}[ ]{0,}\d+[ ]{0,}|[ ]{0,}\d+[ ]{0,}[^,-])"
re_check_permited_character = r"([^-,\d\s])+?"

# Text
about_text_path = PATH_TEXT/"about"
license_text_path = PATH_TEXT/"license"
url_text_path = PATH_TEXT/"urls"

with open(url_text_path, mode="r") as f:
    git_repository = f.readline()
    homepage = f.readline()
    tutorial = f.readline()

about_text = []
with open(about_text_path, "r") as f:
    about_list = f.readlines()
    rlist = list(filter(lambda x: x != "" and x != "\n", about_list))
    about_text += rlist

license = []
with open(license_text_path, "r") as f:
    license_list = f.readlines()
    rlist = list(filter(lambda x: x != "" and x != "\n", license_list))
    license += rlist

#----------------------------------------------------
# Option datas
# Paper-format
format_head = ["Format", "width(mm)", "height(mm)"]
format_table = [
    ("A3", 297, 420),
    ("A4", 210, 297),
    ("A5", 148, 210),
    ("B3", 353, 500),
    ("B4", 250, 353),
    ("B5", 176, 250),
    ("B6", 125, 176),
    ("JIS B3", 364, 515),
    ("JIS B4", 257, 364),
    ("JIS B5", 182, 257),
    ("JIS B6", 128, 182),
    ("Letter", 216, 279),
    ("Legal", 216, 356),
    ("Tabloid", 279, 432),
    ("GOV Letter", 203, 267),
    ("GOV Legal", 216, 279),
    ("ANSI A", 216, 279),
    ("ANSI B", 279, 432),
    ("ARCH A", 229, 305),
    ("ARCH B", 305, 457),
]

PaperFormat = {"Default": "0x0"}
for format in format_table:
    PaperFormat[format[0]] = f"{format[1]}x{format[2]}"


# Note-------------------------------------
pagespec = ["Both", "Odd", "Even", "Odd(only)", "Even(only)"]
pagehf = ["Header", "Footer", "HF", "FH"]
pagehf_e = ["Header", "Footer"]
pagealign = ["LR", "CC", "RL", "LL", "LC", "RR", "RC", "CL", "CR"]
pagealign_e = ["L", "R", "C"]