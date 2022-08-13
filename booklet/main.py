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


__author__ = "Hyunseong Kim"
__company__ = "HornPenguin"
__version__ = "0.0.1"
__license__ = "BSD license"

name = "Booklet"

import argparse
import sys, os, re, platform
sys.path.insert(0, os.path.abspath("."))
import PyPDF2 as pypdf
from PIL import Image


import booklet.signature as sig
import booklet.data as data

from booklet.utils import *
from booklet.data import *

from booklet.images import icon_path
from booklet.gui import Booklet

des = """PDF modulation for printing and press----------------------------------------------------"""
epi = (
    "github: https://github.com/HornPenguin/Booklet \nsupport: support@hornpenguin.com"
)

# Parser check functions-----------------------------------------------------------------------
class Format_Help(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        length = 15
        print(
            "Format".ljust(length)
            + "width(mm)".ljust(length)
            + "height(mm)".ljust(length)
        )
        for format in data.format_table:
            print(
                f"{format[0]}".ljust(length)
                + f"{format[1]}".ljust(length)
                + f"{format[2]}".ljust(length)
            )

        setattr(namespace, self.dest, values)


def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


def dir_path(string):
    if os.path.isdir(string) or os.path.isfile(string):
        return string
    elif '\\' not in string and '/' not in string:
        return string
    elif os.path.isdir(os.path.split(string)[0]):
        return string
    else:
        raise NotADirectoryError(string)


# range validation
range_validation_re = re.compile(data.re_get_ranges)
character_vailidation_re = re.compile(data.re_check_permited_character)


def range_validation(string):  # only max
    text = string.replace(" ", "")
    # self.pagerange_var.set(text)
    vaild = True
    if character_vailidation_re.search(text) != None:
        raise ValueError(f"{string} is not a vaild range.")
    else:
        return string


def color_check(string):
    print("color_check")
    if string is None:
        return "#729fcf"
    text = string
    if "#" in text:
        text = text[1:]

    if len(text) != 6:
        raise ValueError
    else:
        on = "0x" + text[0:2]
        tw = "0x" + text[2:4]
        th = "0x" + text[4:6]
        try:
            int(on, 16)
            int(tw, 16)
            int(th, 16)
        except:
            raise ValueError
    return string


# Argument parser---------------------------------------------------------------------------
parser = argparse.ArgumentParser(prog=f"{name}", description=des, epilog=epi)

# program version
parser.add_argument(
    "--version", action="version", version="%(prog)s " + f"{__version__}"
)
# Addtional help
parser.add_argument(
    "--format-help",
    action=Format_Help,
    nargs=0,
    help="print table of paper format lists.",
)

parser.add_argument(
    "-c",
    "--console", action="store_true", help="Execute with console mode."
)

# file path
inputgroup = parser.add_mutually_exclusive_group()
inputgroup.add_argument(
    "inputfile", nargs="?", type=file_path, help="The input pdf file path."
)
inputgroup.add_argument(
    "-i", "--input", nargs=1, type=file_path, help="The input pdf file path."
)
outputgroup = parser.add_mutually_exclusive_group()
outputgroup.add_argument(
    "outputpath",
    nargs="?",
    type=dir_path,
    help="The output file path can contain file name or not.",
)
outputgroup.add_argument(
    "-o", "--output", nargs=1, type=dir_path, help="The ouput file path."
)

parser.add_argument(
    "-n",
    "--name",
    type=str,
    help="output file name, if output path contains file name, path name is prior than this argument.",
)

# signature options
parser.add_argument(
    "--page-range",
    type=range_validation,
    action="append",
    nargs="*",
    help="The page range to moldulate in the input file. Example: 1-3, 10, 14-20.",
)
parser.add_argument(
    "--blank-mode",
    choices=["back", "front", "both"],
    default="back",
    help="where additional blank pages are added, default = 'back'.",
)
parser.add_argument(
    "--sig-composition", 
    nargs=2, type=int, 
    default=(1, 4), 
    help="signature composition (i, f). i is a inserted number of signature and f is a number of sheets in sub-signature. Default: 1 4")
parser.add_argument(
    "--riffle-direction",
    nargs=1,
    type=str,
    choices=["right", "left"],
    default="right",
    help="riffling direction of signature, old asian book has 'left' riffling direction. Default value='right'.",
)
parser.add_argument("--fold", action="store_true")
formatgroup = parser.add_mutually_exclusive_group()
formatgroup.add_argument(
    "--format",
    nargs=1,
    type=str,
    choices=list(data.PaperFormat.keys()),
    default="Default",
    help="Output paper size format of signature, 'Default': conserves original file paper size. See options with '--format-help'.",
)
formatgroup.add_argument(
    "--custom-format",
    nargs=2,
    type=float,
    help="custom paper size(mm) set, width and height respectively. '--custom-format=200.2 150.1' means 200.5mm width, 150.1mm height size.",
)
parser.add_argument(
    "--imposition",
    action="store_true",
    help="default conversion only rearrange and rotate, this option locates them in each pages. enable \'fold\' option True",
)
parser.add_argument(
    "--split", action="store_true", help="split pdf pages with each signatures."
)
parser.add_argument(
    "--trim", action="store_true", help="add trim marker in imposition pdf."
)
parser.add_argument(
    "-reg",
    "--registration",
    action="store_true",
    help="add registration markers in imposition pdf.",
)
parser.add_argument(
    "--cmyk", action="store_true", help="add cmyk markers in imposition pdf."
)
parser.add_argument(
    "--sigproof",
    type=color_check,
    const="#729fcf",
    nargs="?",
    help="add signature proof that help to check order and missing signature. colorcode is a hex code. Defaults to #729fcf.",
)
parser.add_argument("-y", action="store_true")

# Function------------------------------------------------------------------------


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

    if args.console is True:

        start_1 = False
        start_2 = False
        # Path validation
        inputfile = ""
        outputpath = ""
        pagerange = ""
        if args.inputfile is not None:
            inputfile = args.inputfile
            start_1 =True
        elif args.input is not None:
            inputfile = args.input[0]
            start_1 =True
        elif args.format_help is None:
            raise ValueError("No input file")

        if args.outputpath is not None:
            outputpath = args.outputpath
            start_2 =True
        elif args.output is not None:
            outputpath = args.output[0]
            start_2 =True
        else:
            outputpath = os.getcwd()
            start_2 =True

        if start_1 and start_2:
            # name checker
            if check_dir(outputpath):
                if args.name is not None:
                    name = args.name
                else:
                    name_formatted = os.path.split(inputfile)[1]
                    name = name_formatted.split(".pdf")[0] + "_HP_BOOKLET" + ".pdf"
                outputpath = os.path.join(outputpath, name)

            pre_pdf = pypdf.PdfFileReader(inputfile)
            page_max = len(pre_pdf.pages)
            default_size = [
                float(pre_pdf.getPage(0).mediaBox.width),
                float(pre_pdf.getPage(0).mediaBox.height),
            ]

            # page range
            if args.page_range is not None:
                for li in args.page_range:
                    st = "".join(li)
                    pagerange += st
            else:
                pagerange = f"1-{page_max}"

            #riffle
            rifflebool = True
            if args.riffle_direction == "left":
                rifflebool = False


            # format setting
            if args.format is None or args.format == "Default":
                width, height = pts_mm(default_size)
                format = [width, height]
            else:
                format_size = PaperFormat[args.format].split("x")
                format = [float(format_size[0]), float(format_size[1])]

            # sig composition

            nn = args.sig_composition[0]
            ns = args.sig_composition[1]
            if not check_composition(nn, ns):
                raise ValueError(f"sig composition {nn} {ns} are not vaild.")
            nl = nn * ns
            sig_composition = [nl, nn, ns]

            # blank
            blank = [args.blank_mode, cal_blank_page(len(get_page_range(pagerange)), nl)]

            # sigproof
            if args.sigproof is not None:
                sigproof = [True, args.sigproof[0]]
            else:
                sigproof = [False, ""]

            printbool = args.trim or args.registration or args.cmyk or sigproof[0]

            # Print work info
            print(f"Input:{inputfile}")
            print(f"output:{outputpath}")
            print(f"page range:{pagerange}")
            print(f"blank:add {blank[1]} to {blank[0]}")
            print(f"signature composition:{sig_composition[0]} signature, inserting {sig_composition[1]} {sig_composition[2]} sub signatures")
            print(f"riffle direction:{args.riffle_direction}")
            print(f"paper format: {args.format} {format[0]}x{format[1]} (mm)")
            print(f"fold:{args.fold}")
            print(f"imposition:{args.imposition}")
            print(f"split per signature:{args.split}")

            print("Printing-----------------")
            sigproof_str = f"{sigproof[0]}"
            if sigproof[0]:
                sigproof_str += f" color={args.sigproof[0]}"
            print(f"trim:{args.trim}, registration:{args.registration}, cmyk:{args.cmyk}, sigproof: {sigproof_str}")

            if not args.y:
                print("Continue?(Y/N):")
                answer = input()
                if answer != "y" and answer != "Y":
                    sys.exit()

            pages = sig.get_exact_page_range(pagerange=pagerange, blank=blank)
            page_len =len(pages) * (2 if printbool or args.imposition else 1)
            # generate----------------------------
            sig.generate_signature(
                inputfile=inputfile,
                output=outputpath,
                pagerange=pagerange,
                blank=blank,
                sig_com=sig_composition,
                riffle=rifflebool,
                fold=True if args.imposition else args.fold,
                format=format,
                imposition=args.imposition,
                split=args.split,
                trim=args.trim,
                registration=args.registration,
                cmyk=args.cmyk,
                sigproof=sigproof,
                progress=[page_len]
            )

            print("\n")
            print(f"Done {os.path.split(outputpath)[1]}.")
    else:
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
            name: resources_path(f"{name}.png", "resources") for name in printing_icon_names
        }
        printing_icons = {
            name: Image.open(printing_iconpaths[name]) for name in printing_icon_names
        }
        imposition_icons = {
            name: Image.open(imposition_iconpaths[name]) for name in imposition_icon_names
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
            icons= icons
        )
        hpbooklet.window.mainloop()

