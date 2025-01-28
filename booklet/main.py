#!/usr/bin/env python3

# BSD 3-Clause License
#
# Copyright (c) 2022, HornPenguin Co.
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
import sys, os
sys.path.insert(0, os.path.abspath("."))

from booklet.meta import __version__ as __version__
from booklet.meta import name

from booklet import pypdf as pypdf
from PIL import Image

from booklet.core.manuscript import Manuscript
from booklet.core.modifiers import *
from booklet.core.converters.section import SecComposition, Section

from booklet.utils.misc import *
from booklet.data import *
from booklet.utils.images import icon_path
from booklet.gui import Booklet
from booklet.parser import parser
from booklet.utils.conversion import pts2mm, mm2pts


# Misc utils
def check_dir(path):
    if os.path.isfile(path):
        return False
    elif os.path.isdir(path):
        return True
    else:
        path_split = os.path.split(path)
        if os.path.isdir(path_split[0]):
            return False
        else:
            raise ValueError(f"Is it path? {path}")


def check_composition(nn, ns):
    nl = nn * ns
    if nl % 4 != 0:
        return False
    if nl == 2 and not nn == 1:
        return False
    elif nl == 12 and nn not in [1, 3]:
        return False
    elif nl == 24 and nn not in [1, 2, 3, 6]:
        return False

    return True


def cal_blank_page(pages, nl):
    if pages < nl:
        return nl - pages
    else:
        k = pages % nl
        return (nl - k) if nl > 1 and k != 0 else 0


if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])

    if args.console:  # console mode

        start_1 = False
        start_2 = False
        # Path validation
        inputfile = ""
        outputpath = ""
        pagerange = ""
        if args.inputfile is not None:
            inputfile = args.inputfile
            start_1 = True
        elif args.input is not None:
            inputfile = args.input[0]
            start_1 = True
        elif args.format_help is None:
            raise ValueError("No input file")

        if args.outputpath is not None:
            outputpath = args.outputpath
            start_2 = True
        elif args.output is not None:
            outputpath = args.output[0]
            start_2 = True
        else:
            outputpath = os.getcwd()
            start_2 = True

        if start_1 and start_2:
            # name checker
            if check_dir(outputpath):
                if args.name is not None:
                    name = args.name
                else:
                    name_formatted = os.path.split(inputfile)[1]
                    name = name_formatted.split(".pdf")[0] + "_HP_BOOKLET" + ".pdf"
                outputpath = os.path.join(outputpath, name)

            pre_pdf = pypdf.PdfReader(inputfile)
            page_max = len(pre_pdf.pages)
            
            page0 = pre_pdf.pages[0]
            try:
                    hasattr(page0, "mediabox")
            except TypeError:
                    page0.__setitem__(
                        NameObject(PG.MEDIABOX), RectangleObject(page0["/mediabox"])  # type: ignore
                    )
            width, height = page0.mediabox.width, page0.mediabox.height

            default_size = [
                float(width),
                float(height)
            ]

            # page range
            if args.page_range is not None:
                for li in args.page_range:
                    st = "".join(li)
                    pagerange += st
            else:
                pagerange = f"1-{page_max}"

            # toimage
            toimagebool = args.toimage

            # riffle
            rifflebool = True
            if args.riffle_direction == "left":
                rifflebool = False

            # format setting
            if args.format is None or args.format == "Default":
                width, height = pts2mm(default_size)
                format_mm = [width, height]
                format = default_size
            else:
                format_size = PaperFormat[args.format].split("x")
                format_mm = [float(format_size[0]), float(format_size[1])]
                format = [mm2pts(format_mm)]

            # sig composition
            nl = args.sig_composition[0]
            nn = args.sig_composition[1]
            ns = int(nl / nn)
            if not check_composition(nn, ns):
                raise ValueError(f"sig composition {nl} {nn} are not vaild.")
            nl = nn * ns
            _sig_composition = SecComposition(nl, nn)

            # blank
            blankmode = args.blank_mode
            blank = [blankmode, cal_blank_page(len(get_page_range(pagerange)), nl)]

            # sigproof
            if args.sigproof is not None:
                sigproof = [True, args.sigproof[0]]
            else:
                sigproof = [False, ""]

            printbool = args.crop or args.registration or args.cmyk or sigproof[0]

            # Print work info
            print(f"Input:{inputfile}")
            print(f"output:{outputpath}")
            print(f"page range:{pagerange}")
            print(f"blank:add {blank[1]} to {blank[0]}")
            print(
                f"signature composition:{nl} signature, inserting {nn} {ns} sub signatures"
            )
            print(f"riffle direction:{args.riffle_direction}")
            print(f"paper format: {args.format} {format[0]}x{format[1]} (mm)")
            print(f"fold:{args.fold}")
            print(f"imposition:{args.imposition}")
            print(f"split per signature:{args.split}")

            print("Printing-----------------")
            sigproof_str = f"{sigproof[0]}"
            if sigproof[0]:
                sigproof_str += f" color={args.sigproof[0]}"
            print(
                f"trim:{args.trim}, registration:{args.registration}, cmyk:{args.cmyk}, sigproof: {sigproof_str}"
            )

            if not args.y:
                print("Continue?(Y/N):")
                answer = input()
                if answer != "y" and answer != "Y":
                    sys.exit()

            # old code
            # pages = sig.get_exact_page_range(pagerange=pagerange, blank=blank)
            # page_len =len(pages) * (2 if printbool or args.imposition else 1)

            # generate----------------------------

            default_gap = 5
            default_margin = 43

            manuscript = Manuscript(
                input=inputfile, output=outputpath, page_range=pagerange
            )

            toimage = ToImage(toimage=toimagebool, dpi=300)
            signature = Section(
                sig_composition=_sig_composition,
                blank_mode=blankmode,
                riffle=rifflebool,
                fold=args.fold,
                paper_format=format,
            )
            imposition = Imposition(
                imposition=args.imposition,
                gap=default_gap,
                proof=sigproof[0],
                proof_color=sigproof[1],
                proof_width=default_gap * 2,
                imposition_layout=_sig_composition,
            )
            printing_mark = PrintingMark(
                margin=default_margin,
                crop=args.crop,
                reg=args.registration,
                cmyk=args.cmyk,
            )
            modifiers = [toimage, signature, imposition, printing_mark]
            for modifier in modifiers:
                manuscript.modifier_register(modifier)
            manuscript.update(do="all", file_mode="unsafe")
            if args.split:
                manuscript.save_to_file(split=_sig_composition)
            else:
                manuscript.save_to_file()

            # sig.generate_signature(
            #    inputfile=inputfile,
            #    output=outputpath,
            #    pagerange=pagerange,
            #    blank=blank,
            #    sig_com=sig_composition,
            #    riffle=rifflebool,
            #    fold=True if args.imposition else args.fold,
            #    format=format,
            #    imposition=args.imposition,
            #    split=args.split,
            #    trim=args.trim,
            #    registration=args.registration,
            #    cmyk=args.cmyk,
            #    sigproof=sigproof,
            #    progress=[page_len]
            # )

            print("\n")
            print(f"Done {os.path.split(outputpath)[1]}.")
    else:  # guid mode
        text_pady = 3
        beep_file_name = "beep_ping.wav"
        beep_file = resources_path(beep_file_name, "resources\\sound")

        logo_width = logo_height = 70
        logo = Image.open(resources_path("logo.png", "resources")).resize(
            (logo_width, logo_height), Image.Resampling(1)
        )

        imposition_iconpaths = {
            name: resources_path(f"{name}.png", "resources")
            for name in imposition_icon_names
        }
        printing_iconpaths = {
            name: resources_path(f"{name}.png", "resources")
            for name in printing_icon_names
        }
        printing_icons = {
            name: Image.open(printing_iconpaths[name]) for name in printing_icon_names
        }
        imposition_icons = {
            name: Image.open(imposition_iconpaths[name])
            for name in imposition_icon_names
        }
        icons = {**imposition_icons, **printing_icons}

        hpbooklet = Booklet(
            icon_path,
            homepage=homepage,
            source=git_repository,
            tutorial=tutorial,
            textpady=text_pady,
            beep_file=beep_file,
            logo=logo,
            icons=icons,
        )
        hpbooklet.window.mainloop()
