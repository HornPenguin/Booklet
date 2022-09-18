import argparse
import os, re

from booklet.meta import __version__
from booklet.meta import name as project_name
import booklet.data as data


# Argument Parsing Action
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

# Argument typing function
def type_file_path(string:str):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)
def type_dir_path(string:str):
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
def type_page_range(string:str):  # only max
    text = string.replace(" ", "")
    # self.pagerange_var.set(text)
    vaild = True
    if character_vailidation_re.search(text) != None:
        raise ValueError(f"{string} is not a vaild range.")
    else:
        return string
def type_color(string:str):
    if string == None:
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
# ---------------------------------------

parser = argparse.ArgumentParser(prog=f"{project_name}", description=data.des, epilog=data.epi)

# Console activation
parser.add_argument(
    "-c",
    "--console", action="store_true", help="Execute with console mode."
    )
# Program version
parser.add_argument(
    "--version", action="version", version="%(prog)s " + f"{__version__}"
    )
# Additional help informations
parser.add_argument(
    "--format-help",
    action=Format_Help,
    nargs=0,
    help="Print table of paper format lists.",
    )
# File IO
inputgroup = parser.add_mutually_exclusive_group()
inputgroup.add_argument(
    "inputfile", nargs="?", type=type_file_path, help="The input pdf file path."
    )
inputgroup.add_argument(
    "-i", "--input", nargs=1, type=type_file_path, help="The input pdf file path."
    )
outputgroup = parser.add_mutually_exclusive_group()
outputgroup.add_argument(
    "outputpath",
    nargs="?",
    type=type_dir_path,
    help="The output file path can contain file name or not.",
    )
outputgroup.add_argument(
    "-o", "--output", nargs=1, type=type_dir_path, help="The ouput file path."
    )
parser.add_argument(
    "-n",
    "--name",
    type=str,
    help="The output file name, if output path contains file name, path name is prior than this argument.",
    )

# Manuscript Feature
parser.add_argument(
    "--page-range",
    type=type_page_range,
    action="append",
    nargs="*",
    help="The page range to moldulate in the input file. Example: 1-3, 10, 14-20.",
    )
parser.add_argument(
    "--split", 
    action="store_true", 
    help="split pdf pages with each signatures."
)
# ToImage Feature
parser.add_argument(
    "--toimage",
    action="store_true",
    help="Convert all pages to image page to prevent content breaking during transformation."
    )
parser.add_argument(
    "-dpi",
    type = int,
    default = 600,
    help = "Dpi value of image of pages."
    )
# Note Feature

# Signature Feature
parser.add_argument(
    "--blank-mode",
    type = str,
    choices=["back", "front", "both"],
    default="back",
    help="Where additional blank pages are added, defaults to 'back'.",
    )
parser.add_argument(
    "--sig-composition", 
    nargs=2, 
    type=int, 
    default=(1, 4), 
    help="Signature composition (i, f). i is a inserted number of signature and f is a number of sheets in sub-signature, defaults to 1 4"
    )
parser.add_argument(
    "--riffle",
    nargs=1,
    type=str,
    choices=["right", "left"],
    default="right",
    help="Riffling direction of signature, old asian book has 'left' riffling direction, defaults to 'right'.",
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
# Imposition Feature
parser.add_argument(
    "--imposition",
    action="store_true",
    help="default conversion only rearrange and rotate, this option locates them in each pages. enable \'fold\' option True",
)
parser.add_argument(
    "--sigproof",
    type=type_color,
    const="#729fcf",
    nargs="?",
    help="add signature proof that help to check order and missing signature. colorcode is a hex code. Defaults to #729fcf.",
)
# Printing Mark Feature
parser.add_argument(
    "--crop", action="store_true", help="add crop marker in imposition pdf."
)
parser.add_argument(
    "--reg",
    "--registration",
    action="store_true",
    help="add registration markers in imposition pdf.",
)
parser.add_argument(
    "--cmyk", action="store_true", help="add cmyk markers in imposition pdf."
)

# Miscellaneous
parser.add_argument("-y", action="store_true")




