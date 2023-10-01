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

from PIL import Image

from booklet.utils.misc import resources_path
from booklet.utils.images import icon_path
from os import path


des = """PDF modulation for printing and press----------------------------------------------------"""
epi = (
    "github: https://github.com/HornPenguin/Booklet \nsupport: support@hornpenguin.com"
)


# Resources
# -Audio file
beep_file_name = "beep_ping.wav"
beep_file = resources_path(beep_file_name, path.normpath("resouce/sound"))

# -Images
task_bar_icon = icon_path
logo_width = logo_height = 70
logo = Image.open(resources_path("logo.png", "resources")).resize(
    (logo_width, logo_height), Image.Resampling(1)
)

imposition_icon_names = ["imposition", "split"]
imposition_iconpaths = {
    name: resources_path(f"{name}.png", "resources") for name in imposition_icon_names
}
imposition_icons = {
    name: Image.open(imposition_iconpaths[name]) for name in imposition_icon_names
}
printing_icon_names = ["proof", "cmyk", "registration", "trim"]
printing_iconpaths = {
    name: resources_path(f"{name}.png", "resources") for name in printing_icon_names
}
printing_icons = {
    name: Image.open(printing_iconpaths[name]) for name in printing_icon_names
}

icons = {**imposition_icons, **printing_icons}

# - Text
re_get_ranges = r"([ ]{0,}\d+[ ]{0,}-{1,1}[ ]{0,}\d+[ ]{0,}|[ ]{0,}\d+[ ]{0,}[^,-])"
re_check_permited_character = r"([^-,\d\s])+?"

about_text_path = resources_path("about", path.normpath("resources/text"))
license_text_path = resources_path("license", path.normpath("resources/text"))
url_text_path = resources_path("urls", path.normpath("resources/text"))

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
