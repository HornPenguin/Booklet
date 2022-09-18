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


import io, tempfile
from re import M
from math import log2, log, floor
from typing import Union, Tuple, NoReturn
from datetime import datetime
from typing import Callable

# import numpy as np
import PyPDF2 as pypdf

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import pdf2image

from booklet.utils.misc import *
from booklet.data import PaperFormat
from booklet.utils.permutation import Permutation
import booklet.dependency.img2pdf as img2pdf

from booklet.utils.fonts import *

#   font_database, get_font_file, get_text_width, get_number_widths, cal_width, get_font_file_without_s

fold_arrange = {  # From left-top to right-bottom
    4: [[4, 1], [2, 3]],  # Front page  # Back page
    8: [[8, 1, 5, 4], [2, 7, 3, 6]],
    12: [[12, 1, 9, 4, 8, 5], [2, 11, 3, 10, 6, 7]],
    16: [[16, 1, 4, 13, 9, 8, 5, 12], [10, 7, 6, 11, 15, 2, 3, 14]],
    24: [
        [24, 1, 12, 13, 21, 4, 9, 16, 20, 5, 8, 17],
        [14, 11, 2, 23, 15, 10, 3, 22, 18, 7, 6, 19],
    ],
    32: [
        [20, 13, 12, 21, 29, 4, 5, 28, 32, 1, 8, 25, 17, 16, 9, 24],
        [22, 11, 14, 19, 27, 6, 3, 30, 26, 7, 2, 31, 23, 10, 15, 18],
    ],
    64: [
        [
            44,
            21,
            28,
            37,
            40,
            25,
            24,
            41,
            53,
            12,
            5,
            60,
            57,
            8,
            9,
            56,
            52,
            13,
            4,
            61,
            64,
            1,
            16,
            49,
            45,
            20,
            29,
            36,
            33,
            32,
            17,
            48,
        ],
        [
            46,
            19,
            30,
            35,
            34,
            31,
            18,
            47,
            51,
            14,
            3,
            62,
            63,
            2,
            15,
            50,
            54,
            11,
            6,
            59,
            58,
            7,
            10,
            55,
            43,
            22,
            27,
            38,
            39,
            26,
            23,
            42,
        ],
    ],
}

# Signature modulation-----------------------------------------------------------
def __fold_matrix_update(n: int, matrix: list) -> list:
    """Update :math:`n` signature page layout to :math:`n+1` layout.

    :param n: update number
    :param matrix: :math:`n-1` signature page layout matrix. Must be a :math:'n-1' level matrix for given :param:`n`.

    :type n: int
    :type matrix: list[list]

    This function imitates fold process to increase the number of sheets in signature.

    1. Rotating it elements counter-clockwise.
    2. Adding corresponding :math:`n` page numbers.
    3. Return the next level signature layout matrix.

    Rotating process is same with transpose and filp vertically.

    .. math::

        Rotate(\bold{M}, 90) = Flip(M^T, v)

    The dimension of :math:`n`-level signature layout refers :function:`sig_layout`.
    """
    # n_1 = np.flip(matrix.T, axis=0)
    n_1 = flip(transpose(matrix))
    len_n = len(n_1[0])
    l = int(len_n / 2)
    rows = []
    for row in n_1:
        # r_split = np.split(row,l)
        r_split = split_list(row, l, mode="n")
        row_appended = []
        for tu in r_split:
            # tem = np.array([n-tu[0] +1,n-tu[1] +1])
            # row_appended.append(np.insert(tem, 1, tu))
            tem = [n - tu[0] + 1, n - tu[1] + 1]
            tem.insert(1, tu[1])
            tem.insert(1, tu[0])
            row_appended.append(tem)
        # rows.append(np.concatenate(row_appended, axis=None))
        rows.append(concatenate(row_appended))
    # return np.stack(rows)
    return rows


def sig_layout(n: int) -> tuple:
    """Return a signature page imposition layout for the given argument :param:`n`.

    :param n: Number of sheets in single signature. It must be a positive interger that multiple of 4 or just 1.
    :type n: int

    Additonal description about :param:`n`:
        There are two case of signature sheets. Multiple of only 2 and multiple of 3 (12, 24).
        The former case is more widely used and this function supports perfect layout for all numbers, more than 128.
        However, it only supports 12 ans 24 sheet signature for the latter case. 48 and larger numbers will not work and
        raise value error.
    """
    if type(n) != int:
        raise ValueError("n is not an integer")
    if n == 1:
        return (1, 1)
    elif n < 4 or n % 4 != 0:
        raise ValueError(f"n:{n} must be a positive integer that multiple of 4.")
    if n % 3 == 0:
        if n > 24:
            raise ValueError("Only 12 and 24 sheets signatures are")
        i = log2(n) - log2(3) - 1
        return (3, int(2**i))
    else:
        i = int(log2(n / 4))
        if i % 2:
            k = kp = int((i + 1) / 2)
        else:
            k = int(i / 2)
            kp = k + 1
        return (int(2**k), int(2**kp))


def fold_arrange_n(n, per=False) -> Union[list, Permutation]:
    if n == 2:
        if per:
            return Permutation(2, [1, 2])
        else:
            return [[1], [2]]
    if n % 4 != 0:
        raise ValueError(
            "Fold sheets must be 4*2^k for k= 0, 1, 2, .... \n Current value is {n}"
        )

    if n <= 64:
        fn = fold_arrange[n]
        if per:
            return Permutation(n, fn[0] + fn[1])
        else:
            return fn
    else:
        n_iter = int(log(n / 16, 2))
        n_i = 32
        per_n_1 = [fold_arrange[n_i][0], fold_arrange[n_i][1]]
        # permutation to matrix
        layout_n_1 = sig_layout(n_i)
        # front_matrix = np.array(per_n_1[0]).reshape(layout_n_1)
        # back_matrix = np.array(per_n_1[1]).reshape(layout_n_1)
        front_matrix = reshape(per_n_1[0], layout_n_1)
        back_matrix = reshape(per_n_1[1], layout_n_1)
        for i in range(0, n_iter):
            n_i = 2 * n_i
            front_matrix = __fold_matrix_update(n_i, front_matrix)
            back_matrix = __fold_matrix_update(n_i, back_matrix)
    # per_fn = np.concatenate(front_matrix).tolist()
    # per_bn = np.concatenate(back_matrix).tolist()
    per_fn = concatenate(front_matrix)
    per_bn = concatenate(back_matrix)
    if per:
        return Permutation(n, per_fn + per_bn)
    else:
        return [per_fn, per_bn]


def sig_rearrange(nn: int, ns: int, split: bool = False) -> list:
    if ns == 2:
        return [1, 2]
    n_l = nn * ns
    nlist = [i + 1 for i in range(0, n_l)]
    nlist_splited = split_list(nlist, int(ns / 2)) if ns != 1 else nlist

    rlist = []

    n_splited = 2 * nn

    if split:
        for i in range(0, nn):
            rlist.append(nlist_splited[i] + nlist_splited[n_splited - i - 1])
    else:
        for i in range(0, nn):
            rlist = rlist + nlist_splited[i] + nlist_splited[n_splited - i - 1]
    return rlist


def signature_permutation(
    n: int, nn: int, ns: int, arrange: list[list, list] = [[None], [None]]
) -> Permutation:

    if n == nn and nn == ns:
        permutation_signature = Permutation(1, [1])
    else:
        if arrange[0][0] != None:
            arrange = fold_arrange_n(ns, per=True)
        permutation_signature = Permutation(n, sig_rearrange(nn, ns)).index_mul_partial(
            arrange, oper=False
        )
    return permutation_signature


# Printing markers--------------------------------------------------------
def __drawRegistationMark(
    canvas: canvas.Canvas, x: float, y: float, l: float
) -> Union[NoReturn, int]:
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
    canvas.setStrokeColor(registration_black)
    canvas.setFillColor(registration_black)
    # lines
    canvas.lines(lines)

    # outter
    arcs = canvas.beginPath()
    # arcs.circle(x+l/2+line_t, y+l/2+line_t, circle_r1)
    c = l / 2 - line_t / 2
    # x1 = c - circle_r1
    # x2 = c + circle_r1
    # x1, x2 = get_abpath2(x1, x2)
    # arcs.circle(x+ c, y+c , circle_r1)
    x1 = c - circle_r1
    x2 = c + circle_r1
    # 상대 경로는 같아도 절대 경로에서는 x,y값이 같지 않음
    x1, y1 = get_abpath2(x1, x1)
    x2, y2 = get_abpath2(x2, x2)
    arcs.arc(x1, y1, x2, y2, startAng=180, extent=90)
    arcs.arc(x1 + line_t, y1, x2 + line_t, y2, startAng=270, extent=90)
    arcs.arc(x1 + line_t, y1 + line_t, x2 + line_t, y2 + line_t, startAng=0, extent=90)
    arcs.arc(x1, y1 + line_t, x2, y2 + line_t, startAng=90, extent=90)
    canvas.drawPath(arcs, fill=0, stroke=1)

    # inner
    arcs_fill = canvas.beginPath()
    # arcs_fill.circle(x+l/2, y+l/2, circle_r2)
    x1 = c - circle_r2
    x2 = c + circle_r2
    x1, y1 = get_abpath2(x1, x1)
    x2, y2 = get_abpath2(x2, x2)

    xc, yc = get_abpath2(l / 2, l / 2)

    d = line_t / 2

    arcs_fill.moveTo(xc - d, yc - d)
    arcs_fill.arcTo(x1, y1, x2, y2, startAng=180, extent=90)

    arcs_fill.moveTo(xc + d, yc - d)
    arcs_fill.arcTo(x1 + line_t, y1, x2 + line_t, y2, startAng=270, extent=90)

    arcs_fill.moveTo(xc + d, yc + d)
    arcs_fill.arcTo(
        x1 + line_t, y1 + line_t, x2 + line_t, y2 + line_t, startAng=0, extent=90
    )

    arcs_fill.moveTo(xc - d, yc + d)
    arcs_fill.arcTo(x1, y1 + line_t, x2, y2 + line_t, startAng=90, extent=90)

    canvas.drawPath(arcs_fill, fill=1, stroke=0)

    return 0


def page_printing_layout(
    pagesize: tuple,
    pagenum: int,
    n: tuple,
    nd: int,
    d: int,
    proof: bool,
    proofcode: str,
    trim: bool,
    registration: bool,
    cmyk: bool,
) -> Tuple[pypdf.PdfReader, io.BytesIO, Tuple[float, float]]:

    # signature composition

    ni, ns = n[0], n[1]
    sig = 2 if ns > 1 else 1
    n_block = int(pagenum / (ni * ns))

    # Paper dimension
    arrange = sig_layout(ns)
    ny = arrange[0]
    nx = arrange[1]

    x = 2 * nd + nx * pagesize[0] + (nx - 1) * d
    y = 2 * nd + ny * pagesize[1] + (ny - 1) * d

    y1 = nd + ny * pagesize[1] + (ny - 1) * d

    # Signature proof
    if proof:
        proof_height = pagesize[1] / n_block
        proof_width = d
        cmyk_proof = hex_to_cmyk(proofcode)
        proof_position = [
            nd + pagesize[0],
            nd + ny * pagesize[1] + (ny - 1) * d - proof_height,
        ]
    # trim
    trim_l = nd * (1 / 2)
    if trim:

        # horizontal line
        x1 = nd / 4
        x2 = nd + nx * pagesize[0] + (nx - 1) * d + x1
        y1 = nd + ny * pagesize[1] + (ny - 1) * d
        y2 = nd
        # vertical line
        x3 = nd
        x4 = x2 - x1
        y3 = nd / 4
        y4 = y1 + y3

        trim_lines = [
            (x1, y1, x1 + trim_l, y1),  # h, u l
            (x1, y2, x1 + trim_l, y2),  # h, d l
            (x2, y1, x2 + trim_l, y1),  # h, u r
            (x2, y2, x2 + trim_l, y2),  # h, d r
            (x3, y4, x3, y4 + trim_l),  # v, u l
            (x3, y3, x3, y3 + trim_l),  # v, d l
            (x4, y4, x4, y4 + trim_l),  # v, u r
            (x4, y3, x4, y3 + trim_l),  # v, d r
        ]
    if registration:
        l = (4 / 5) * nd
        dis = nd / 2

        if not trim:
            # horizontal line
            x1 = nd / 4
            x2 = nd + nx * pagesize[0] + (nx - 1) * d + x1
            y1 = nd + ny * pagesize[1] + (ny - 1) * d
            y2 = nd
            # vertical line
            x3 = nd
            x4 = x2 - x1
            y3 = nd / 4
            y4 = y1 + y3

        regist_coords = [
            (dis - l / 2, y1 - dis - l),
            (dis - l / 2, y2 + dis),
            (x2 + trim_l / 2 - l / 2, y1 - dis - l),
            (x2 + trim_l / 2 - l / 2, y2 + dis),
            (x3 + dis, y4 + trim_l / 2 - l / 2),
            (x3 + dis, dis - l / 2),
            (x4 - dis - l, y4 + trim_l / 2 - l / 2),
            (x4 - dis - l, dis - l / 2),
        ]
    if cmyk:
        rec_l = nd / 2
        rec_d = nd / 8
        cmyk_position = [nd / 4, y1 - 2 * (nd + rec_l)]

    tem_pdf_byte = io.BytesIO()

    layout = canvas.Canvas(tem_pdf_byte, pagesize=(x, y))

    # Test
    layout.setFillColorRGB(0, 1, 1)

    for i in range(0, n_block):
        for j in range(0, ni):

            # fill basic layout components
            if proof and j == 0:  # draw rectangle
                layout.setLineWidth(0)
                layout.setFillColorCMYK(
                    cmyk_proof[0], cmyk_proof[1], cmyk_proof[2], cmyk_proof[3]
                )
                layout.rect(
                    proof_position[0],
                    proof_position[1],
                    proof_width,
                    proof_height,
                    fill=1,
                )

                proof_position[1] = proof_position[1] - proof_height

            for k in range(0, sig):
                if trim:  # draw line
                    layout.setLineWidth(0.5 * mm)
                    layout.lines(trim_lines)
                if registration:  # add image
                    __drawRegistationMark(
                        canvas=layout, x=regist_coords[0][0], y=regist_coords[0][1], l=l
                    )
                    __drawRegistationMark(
                        canvas=layout, x=regist_coords[1][0], y=regist_coords[1][1], l=l
                    )
                    __drawRegistationMark(
                        canvas=layout, x=regist_coords[2][0], y=regist_coords[2][1], l=l
                    )
                    __drawRegistationMark(
                        canvas=layout, x=regist_coords[3][0], y=regist_coords[3][1], l=l
                    )
                    __drawRegistationMark(
                        canvas=layout, x=regist_coords[4][0], y=regist_coords[4][1], l=l
                    )
                    __drawRegistationMark(
                        canvas=layout, x=regist_coords[5][0], y=regist_coords[5][1], l=l
                    )
                    __drawRegistationMark(
                        canvas=layout, x=regist_coords[6][0], y=regist_coords[6][1], l=l
                    )
                    __drawRegistationMark(
                        canvas=layout, x=regist_coords[7][0], y=regist_coords[7][1], l=l
                    )
                if cmyk:
                    layout.setLineWidth(0)
                    layout.setFillColor(color_cyan)
                    layout.rect(
                        cmyk_position[0], cmyk_position[1], rec_l, rec_l, fill=1
                    )
                    cmyk_position[1] -= rec_d + rec_l
                    layout.setFillColor(color_magenta)
                    layout.rect(
                        cmyk_position[0], cmyk_position[1], rec_l, rec_l, fill=1
                    )
                    cmyk_position[1] -= rec_d + rec_l
                    layout.setFillColor(color_yellow)
                    layout.rect(
                        cmyk_position[0], cmyk_position[1], rec_l, rec_l, fill=1
                    )
                    cmyk_position[1] -= rec_d + rec_l
                    layout.setFillColor(color_black)
                    layout.rect(
                        cmyk_position[0], cmyk_position[1], rec_l, rec_l, fill=1
                    )
                    cmyk_position[1] = y1 - 2 * (nd + rec_l)

                layout.showPage()

    # ----------------------------
    layout.save()
    tem_pdf_byte.seek(0)
    tem_pdf = pypdf.PdfReader(tem_pdf_byte)

    return tem_pdf, tem_pdf_byte, (x - nd, y - nd)


# Main Routine (Sequential): For the progress routine in the program ui.
def get_writer_and_manuscript(
    inputfile: str,
) -> Tuple[pypdf.PdfFileReader, pypdf.PdfFileWriter, dict]:

    if type(inputfile) == str:
        manuscript = pypdf.PdfFileReader(inputfile)
    else:
        manuscript = inputfile
    output = pypdf.PdfFileWriter()

    # Copy meta datas and add modificaion 'date' and 'producer'
    # PyPDF2 has an error for directly putting PdfReader meta values to PdfWriter
    # We have to convert them with string variable before apply to PdfWriter.
    meta = {}
    for key in manuscript.metadata.keys():
        val = manuscript.metadata.raw_get(key)
        meta[key] = str(val)  # converting to string

    output.add_metadata(meta)
    output.add_metadata({"/Producer": "HornPenguin Booklet"})
    output.add_metadata({"/ModDate": f"{datetime.now()}"})

    return manuscript, output, meta


def get_exact_page_range(pagerange: list, blank: tuple) -> list:

    page_range = get_page_range(pagerange)

    blankmode = blank[0]
    blanknum = blank[1]

    if blankmode == "front":
        blankfront = blanknum
    elif blankmode == "both":
        blankfront = int(blanknum / 2)
    else:
        blankfront = 0

    blankback = blanknum - blankfront

    blankfront_list = [0 for i in range(0, blankfront)]
    blankback_list = [0 for i in range(0, blankback)]
    page_range = blankfront_list + page_range + blankback_list

    return page_range


def get_arrange_permutations(
    leaves: tuple, riffle: bool, arrange: list[list[None], list[None]]
) -> Tuple[Permutation, Permutation]:

    nl = int(leaves[0])
    nn = int(leaves[1])
    ns = int(leaves[2])
    sig_permutation = signature_permutation(nl, nn, ns, arrange)
    riffle_permutation = Permutation(2, [1, 2]) if riffle else Permutation(2, [2, 1])
    return sig_permutation, riffle_permutation


def get_arrange_determinant(
    page_range: list, leaves: tuple, fold: bool
) -> Tuple[list, tuple, tuple]:

    nl = leaves[0]
    nn = leaves[1]
    ns = leaves[2]

    blocks = split_list(page_range, nl)
    composition = (nn, ns) if fold else (1, 1)
    layout = sig_layout(ns) if composition[1] != 2 else (1, 1)

    return blocks, composition, layout


def get_format_dimension(format: Tuple[bool, float, float, str]) -> Tuple[float, float]:
    if format[0]:
        f_dim = PaperFormat[format[3]].split("x")
        f_width, f_height = pts_mm((int(f_dim[0]), int(f_dim[1])), False)
    else:
        f_width, f_height = pts_mm((format[1], format[2]), False)

    return f_width, f_height


def toimagepdf(pdf_path, mode: bool = False, dpi: int = 600, format=None):
    """Convert crop/media box view of all pages in the given pdf to single image in each page.

    Args:
        pdf_path (str): Path of the given pdf. It is a first filter so the permitted type is only :type:`str`.
        mode (bool, optional): Activate the function. If it is :py:`False` it will return :py:`{"bool":False}`. Defaults to False.
        dpi (int, optional): DPI value of images. Defaults to 600.
        format (tuple, optional): Size of the ouput image. If it is :code:`None` then original page size will be conserved. Defaults to None.

    Returns:
        dict: bool: boolean value of activation
              pdf: PyPDF2.PdfFileReader class of the transposed pdf. All its pages are image and it is saved in temporary file.
              dir: Temporary directory that all pages images are saved.
              file: Temporary file object connected with the pdf.
    """
    if mode:
        tem_dir = tempfile.TemporaryDirectory()
        page_images = pdf2image.convert_from_path(
            pdf_path,
            dpi=dpi,
            fmt="png",
            use_cropbox=True,
            transparent=False,
            output_folder=tem_dir.name,
            size=format,
        )
        tem_file = tempfile.TemporaryFile(suffix=".pdf")
        files = [im.filename for im in page_images]

        tem_file.write(img2pdf.convert(files))
        return {
            "bool": True,
            "pdf": pypdf.PdfFileReader(tem_file),
            "dir": tem_dir,
            "file": tem_file,
        }

    else:
        return {"bool": False}


def note(
    pdf: Union[pypdf.PdfFileReader, str, None] = None,
    mode: bool = False,
    pages: Union[int, None] = None,
    numbering: bool = False,
    target_pages: str = "Both",
    location: str = "Header",
    align: str = "LR",
    padding: float = 8.0,
    font: str = "Helvetica",
    size: float = 12.0,
    format: tuple = (PaperFormat["A4"]),
):
    """Expand the given pdf to the prefixed number of pages.
    and return the numbered pdfs for merging.
    """

    if mode:  # actiave filter
        pass
    else:
        return False
    if pdf == None:  # No pdf is given
        return False
    elif type(pdf) == str:  # if given value is path, change it to PyPDF2 reader class
        pdf = pypdf.PdfFileReader(pdf)
    elif len(pdf.pages) == 0:
        raise ValueError("Invaild pdf")

    if pages == None:  # No total number of note pages
        return False

    if pages < 50:
        tem_pdfs = [io.BytesIO()]
        if numbering:
            tem_pdfs.append(io.BytesIO())
    else:
        tem_pdfs = [tempfile.TemporaryFile(suffix=".pdf")]
        if numbering:
            tem_pdfs.append(tempfile.TemporaryFile(suffix=".pdf"))

    manuscript = pypdf.PdfFileWriter()
    ml = len(pdf.pages)
    for i in range(0, pages):
        num = i % ml
        manuscript.add_page(pdf.pages[num])
    manuscript.write(tem_pdfs[0])

    if numbering:
        # check the font
        numbered_pages = canvas.Canvas(tem_pdfs[1], pagesize=format)
        available_fonts = numbered_pages.getAvailableFonts()
        if font not in available_fonts:
            try:
                fontname, filepath = get_font_file_without_s(font)
            except:
                raise ValueError(f"Invaild font name: {font}")

            pdfmetrics.registerFont(TTFont(fontname, filepath))

        number_widths = get_number_dims(font, size)[2]
        font = fontname

        for i in range(0, pages):
            # add numbering
            page_number, origin = get_num_position(
                i,
                size,
                padding,
                number_widths,
                format,
                location=location,
                align=align,
                target_pages=target_pages,
            )
            if bool(page_number) == False:
                pass
            else:
                page_number = str(page_number)
                text_object = numbered_pages.beginText()
                text_object.setFont(font, size=size, leading=None)
                text_object.setTextOrigin(origin[0], origin[1])
                text_object.textOut(page_number)
                numbered_pages.drawText(text_object)
            numbered_pages.showPage()
        numbered_pages.save()

    if type(tem_pdfs[0]) == io.BytesIO:
        tem_pdfs[0].seek(0)
        if numbering:
            tem_pdfs[1].seek(0)
    pdf_manu = pypdf.PdfFileReader(tem_pdfs[0])
    pdf_numbering = None
    template = None
    if numbering:
        pdf_numbering = pypdf.PdfFileReader(tem_pdfs[1])
        template = Template(pdf_numbering, tem_pdfs[1])
    return pdf_manu, tem_pdfs[0], template


def get_num_position(
    page_number,
    fontsize,
    widths,
    format,
    padding=5,
    location="H",
    align="C",
    target_pages="Both",
):

    num = page_number + 1
    num_odd = bool(num % 2)
    length = pix2pts(cal_num_width(str(num), widths, simple=True))
    loc_ys = {  # Report Lab start its origin from left top(0,0) to right bottom(format_x, format_y)
        "H": padding,
        "F": format[1] - padding - fontsize,
    }
    text_aligns = {
        "L": padding,
        "C": (format[0] - length) / 2,
        "R": format[0] - padding - length,
    }
    if len(location) > 2:
        location = [location[0]]
    else:
        location = [location[0], location[1]]
    if len(align) > 2:
        align = [align[0]]
    else:
        align = [align[0], align[1]]

    # Numbering
    if target_pages in ["Both", "Left", "Right"]:
        if target_pages[0] == "L":
            num = False if num_odd else num
        else:
            num = num if num_odd else False
    else:  # Only, remeber that odd number pages are right page
        if "Left" in target_pages:
            num = False if num_odd else int(num / 2)
        else:
            num = int((num + 1) / 2) if num_odd else False

    # Location Cal 1. Header/Footer, 2. Center, Right, Left
    if len(location) == 2:
        if num_odd:
            loc_y = loc_ys[location[1]]
        else:
            loc_y = loc_ys[location[0]]
    else:
        loc_y = loc_ys[location[0]]

    if len(align) == 2:
        if num_odd:
            loc_x = text_aligns[align[1]]
        else:
            loc_x = text_aligns[align[0]]
    else:
        loc_x = text_aligns[align[0]]

    origin = [loc_x, loc_y]

    return num, origin


def generate_signature(
    inputfile: str,
    output: str,
    pagerange: str,
    blank: list[str, int],
    sig_com: list[int, int, int],
    riffle: bool,
    fold: bool,
    format: list[float, float],
    imposition: bool,
    split: bool,
    trim: bool,
    registration: bool,
    cmyk: bool,
    sigproof: list[bool, str],
    progress: list = [
        None
    ],  # length, tkinter_progress_barm, tkinter_progress_text, tkinter_windows
    note: tuple = (None),
    image: dict = None,
    custom_imposition: Union[Tuple[None], Tuple[bool, int, int, str, str]] = (None),
):
    update_type = 0
    current = 1

    def update(update_type, current):
        if update_type == 0:
            pass
        elif update_type == 1:
            progress_bar["value"] = current
            progress_text.set(f"{progress_bar['value']/progress_length *100:.2f}%")
            progress_window.update()
        elif update_type == 2:
            percent = 100 * (current / progress_length)
            bar = "█" * int(percent) + "-" * (100 - int(percent))
            endstr = "\r" if (percent - 100) < 0.01 else "\n"
            print(f"\r|{bar}| {percent:.2f}%", end="\r")

        return current + 1

    if progress[0] == None:
        pass
    elif len(progress) == 4:
        update_type = 1
        progress_length = progress[0]
        progress_bar = progress[1]
        progress_text = progress[2]
        progress_window = progress[3]
    elif len(progress) == 1:
        update_type = 2
        progress_length = progress[0]
    else:
        raise ValueError(f"{progress}")

    format_width, format_height = pts_mm(format, False)  # mm to pts

    arrange = [[None], [None]]
    if custom_imposition[0]:
        nl = custom_imposition[1]
        nn = custom_imposition[2]
        ns = nl / nn
        sig_com = (nl, nn, ns)
        arrange = [custom_imposition[3], custom_imposition[4]]

    if image["bool"]:  # Convert pdf pages to image page
        imageconversion = toimagepdf(inputfile, mode=True, dpi=image["dpi"])
        img_tem_dir = imageconversion["dir"]
        img_tem_file = imageconversion["file"]
        inputfile = imageconversion["pdf"]

    # Template processing
    additional_templates = []
    template_total_pages = 0
    # Templates
    if note["bool"]:
        inputfile, tem_file_note, note_template = note(
            pdf=inputfile,
            mode=True,
            pages=note["pages"],
            numbering=note["numbering"],
            target_pages=note["target_pages"],
            location=note["location"],
            align=note["align"],
            padding=note["padding"],
            font=note["font"],
            size=note["fontsize"],
            format=(format_width, format_height),
        )
        if note_template != None:
            additional_templates.append(note_template)
            template_total_pages = (
                note["pages"]
                if note["pages"] > template_total_pages
                else template_total_pages
            )

    template_on = False
    if len(additional_templates) > 0:
        template_on = True
        template_file = tempfile.TemporaryFile(suffix=".pdf")
        template_pdf = pypdf.PdfFileWriter(template_file)
        for i in range(0, template_total_pages):
            template_pdf.add_blank_page(width=format_width, height=format_height)

        for template in additional_templates:
            for i in range(0, template_total_pages):
                page = template_pdf.pages[i]
                if i < len(template.pages) and template.index_rule(i):
                    page.merge_page(template.pages[i])

    manuscript, writer, meta = get_writer_and_manuscript(inputfile)
    page_range = get_exact_page_range(pagerange, blank)
    per_sig, per_riffle = get_arrange_permutations(sig_com, riffle, arrange)
    blocks, composition, layout = get_arrange_determinant(page_range, sig_com, fold)

    # ---------------------------------------------
    transformation = [
        pypdf.Transformation(),
        pypdf.Transformation().rotate(180).translate(tx=format_width, ty=format_height),
    ]
    trans_index = 0

    per_blocks = []  # generate permutated blocks
    for block in blocks:
        per_block = per_sig.permute_to_list_index(block)
        if sig_com[0] != 1:
            per_block = Permutation.subpermutation_to_list_index(per_riffle, per_block)
        per_blocks.append(per_block)

    fold_on = True if fold and layout[0] > 1 else False
    unit_len = int(sig_com[2] / 2) if fold_on else 1

    for pages in per_blocks:
        for index, i in enumerate(pages):
            # number filter
            trans_index = 1 if fold_on and int(index % unit_len) % 2 else 0

            # body---------------------------------------
            if i == 0:
                writer.add_blank_page(width=format_width, height=format_height)
            else:
                pagenum = i - 1
                page = manuscript.pages[pagenum]
                left = page.mediabox[0]
                bottom = page.mediabox[1]
                page.add_transformation(
                    transformation[trans_index].translate(tx=-left, ty=-bottom)
                )
                page.cropbox.setUpperRight([format_width, format_height])
                page.scale_to(format_width, format_height)

                # additonal filter
                if template_on:
                    page.merge_page(template_pdf.pages[pagenum])

                writer.add_page(page)

            current = update(update_type, current)

    # ------------------

    ndbool = trim or registration or cmyk
    printbool = sigproof[0] or ndbool

    nd = 43 if ndbool else 0  # approx to 5mm
    d = 5 if ndbool else 0

    if imposition or printbool:

        tem_pdf, temfile, cropsize = page_printing_layout(
            (format_width, format_height),
            len(page_range),
            n=composition,
            nd=nd,
            d=d,
            proof=sigproof[0],
            proofcode=sigproof[1],
            trim=trim,
            registration=registration,
            cmyk=cmyk,
        )

        def position(i, layout):
            if i == 0:
                i = 1
            nx = layout[1]
            ny = layout[0]
            x = (i - 1) % (nx)
            y = ny - floor((i - 1) / nx) - 1
            return (x, y)

        nre = int(sig_com[2] / 2) if sig_com[2] > 2 and imposition else 1
        # print(f"Debuge: nre={nre}, tem_page:{len(tem_pdf.pages)}")
        for i in range(0, len(tem_pdf.pages)):
            page = tem_pdf.pages[i]

            for k in range(0, nre):
                l = i * nre + k
                # print(l, f"{i}x{int(sig_com[2]/2)}+{k}", len(writer.pages))

                page_wm = writer.pages[l]
                x, y = position(k + 1, layout)
                tx = nd + (format_width + d) * x
                ty = nd + (format_height + d) * y
                t_page = pypdf.Transformation().translate(tx=tx, ty=ty)
                page_wm.add_transformation(t_page)
                page_wm.cropbox.setUpperRight(cropsize)
                page.merge_page(page_wm)

                current = update(update_type, current)
        if split:
            path_and_name = output.split(".pdf")[0]
            for i in range(0, len(tem_pdf.pages))[0::2]:
                sp_pdf = pypdf.PdfFileWriter()
                sp_pdf.add_metadata(meta)
                sp_pdf.add_metadata({"/Producer": "HornPenguin Booklet"})
                sp_pdf.add_metadata({"/ModDate": f"{datetime.now()}"})

                sp_pdf.add_page(tem_pdf.pages[i])
                sp_pdf.add_page(tem_pdf.pages[i + 1])
                with open(path_and_name + f"_{int(i/2)+1}" + ".pdf", "wb") as sp_f:
                    sp_pdf.write(sp_f)
        else:
            tem_pdf_writer = pypdf.PdfWriter()
            tem_pdf_writer.add_metadata(meta)
            tem_pdf_writer.add_metadata({"/Producer": "HornPenguin Booklet"})
            tem_pdf_writer.add_metadata({"/ModDate": f"{datetime.now()}"})
            tem_pdf_writer.append_pages_from_reader(tem_pdf)
            with open(output, "wb") as f:
                tem_pdf_writer.write(f)

        temfile.close()
    else:
        if split:
            path_and_name = output.split(".pdf")[0]
            sig_list = split_list(list(range(0, len(writer.pages))), sig_com[1])

            for i, sig in enumerate(sig_list):
                sp_pdf = pypdf.PdfFileWriter()
                for index in sig:
                    sp_pdf.add_page(writer.pages[index])
                with open(path_and_name + f"_{int(i)+1}" + ".pdf", "wb") as sp_f:
                    sp_pdf.write(sp_f)
        else:
            with open(output, "wb") as f:
                writer.write(f)

    return 0
