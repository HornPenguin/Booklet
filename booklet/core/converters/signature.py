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


from typing import Union, Tuple
from numbers import Number
from decimal import Decimal
from math import log2

import PyPDF2 as pypdf

from booklet.core.manuscript import Manuscript, Converter
from booklet.utils.permutation import Permutation
from booklet.utils import matrix as Matrix
from booklet.utils import validation as Validation


class SigComposition:  # Fix all the permutation routines. Currnet is not vaild option
    __page_map = {
        4: [[4, 1], [2, 3]],
        8: [[8, 1, 5, 4], [2, 7, 3, 6]],
        16: [[16, 1, 4, 13, 9, 8, 5, 12], [10, 7, 6, 11, 15, 2, 3, 14]],
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
        12: [[12, 1, 9, 4, 8, 5], [2, 11, 3, 10, 6, 7]],
        24: [
            [24, 1, 12, 13, 21, 4, 9, 16, 20, 5, 8, 17],
            [14, 11, 2, 23, 15, 10, 3, 22, 18, 7, 6, 19],
        ],
    }

    def __init__(
        self,
        sig_leaves: int = 4,
        insert: int = 1,
        custom: Union[
            Tuple[bool], Tuple[bool, Union[list[list, list], list], Tuple[int, int]]
        ] = [False],
    ):
        self.__leaves_check(sig_leaves, insert)
        self._leaves_total: int = sig_leaves
        self._leaves_inserted: int = insert
        self._leaves_gathered: int = int(self._leaves_total / self._leaves_inserted)

        if custom[0]:
            custom_map = custom[1]
            custom_layout: Tuple = custom[2]
            self._page_mapping: Permutation = self.__map_check(custom_map)
            self._page_imposition = self.__layout_check(custom_layout)
        else:
            self._page_mapping: Permutation = self.__std_mapping(
                self._leaves_inserted, self._leaves_gathered
            )
            self._page_imposition = self.__page_impose_layout(self._leaves_gathered)

    @classmethod
    def from_permutation(
        cls, permute: Permutation, insert=1, custom=False, layout=(1, 1)
    ):
        if not isinstance(permute, Permutation):
            raise TypeError(f"Must be a permutation type, {type(permute)}")
        sig_leaves = permute.n
        if sig_leaves % 2:
            raise ValueError("Must be an even length permutation")

        if custom:
            custom_tuple = (custom, permute.plist, layout)
        else:
            custom_tuple = custom
        return cls(sig_leaves, insert, custom_tuple)

    @classmethod
    def from_custom_composition(cls, lists: Union[list, tuple], layout):
        if isinstance(lists, list, tuple):
            length = len(lists)
        if isinstance(lists[0], list, tuple):
            length = len(lists[0]) + len(lists[1])
        return cls(length, custom=(True, lists, layout))

    @property
    def leaves(self):
        return self._leaves_total

    @leaves.setter
    def leaves(self, leave):
        self.__leaves_check(leave, self._leaves_inserted)
        self._leaves_total = leave

    @property
    def composition(self):
        return (self._leaves_inserted, self._leaves_gathered)

    @property
    def map(self):
        return self._page_mapping

    @map.setter
    def map(self, map):
        self._page_mapping = self.__map_check(map)

    def __map_check(self, map):
        if isinstance(map, list):
            if isinstance(map[0], list):
                if len(map[0]) != len(map[1]):
                    raise ValueError(
                        "[a:List,b:List], lengths of the a and the b are not same."
                    )
                map = Permutation.from_lists(map)
            else:
                length = len(map)
                if length % 2 != 0:
                    raise ValueError("The length must be even.")
                map = Permutation(length, map)

        if not isinstance(map, Permutation):
            raise TypeError("Given mapping data must be a Permutation or list type.")
        else:
            length = map.n

        if length != self._leaves_total:
            raise ValueError("Length of list is not same with the total leaves.")

        return map

    @property
    def imposition(self):
        row, column = self.layout
        front, back = Matrix.split_list(self.map.plist, 2, mode="n")
        return (
            Matrix.split_list(front, row, mode="n"),
            Matrix.split_list(back, row, mode="n"),
        )

    @property
    def layout(self):
        return self._page_imposition

    @layout.setter
    def layout(self, layout):
        self._page_impose_layout = self.__layout_check(layout)

    def __layout_check(self, layout):
        if not isinstance(layout, list, tuple):
            raise TypeError("Must be list or tuple")
        if len(layout) != 2:
            raise ValueError("Length must be 2")

        try:
            row = int(layout[0])
            column = int(layout[1])
        except:
            raise ValueError(f"Values must be integer, {type(row)} {type(column)}")

        if row <= 0 or column <= 0:
            raise ValueError("Must be positive integer")

        if row * column != int(self._leaves_total / 2):
            raise ValueError("Total pages must be same with a half of signature leaves")

        return layout

    def __leaves_check(self, leaves, insert):
        if isinstance(leaves, str) or isinstance(insert, str):
            try:
                leaves = int(leaves)
                insert = int(insert)
            except:
                raise ValueError(
                    f"Given values must be at least numerical string: {leaves} {insert}"
                )
        if not isinstance(leaves, int) or not isinstance(insert, int):
            raise TypeError(f"Must be integer types, {type(leaves)} {type(insert)}")

        if leaves % insert:
            raise ValueError("leaves must have insert as a factor")

    def __page_impose_layout(self, n: int):
        if type(n) != int:
            raise ValueError("n is not an integer")
        if n == 1:
            return (1, 1)
        elif n < 4 or n % 4 != 0:
            raise ValueError(
                f"n:{n} must be a positive integer that has for divisor 4."
            )
        if n % 3 == 0:
            if n > 24:
                raise ValueError("Only 12 and 24 sheets signatures are supported")
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

    def __std_mapping(self, insert: int, n: int):

        if insert == n and n == 1:
            return Permutation(1, [1])
        if n == 2:
            return Permutation(2, [1, 2])
        if n % 4 != 0:
            raise ValueError(f"Leaves must have 4 as a factor. {n}")
        if n == 48:
            raise ValueError(f"Not supported, {n}")
        if n <= 64:
            fn = self.__page_map[n]
            permutation_i = Permutation(n, fn[0] + fn[1])
        else:

            def matrix_update(order, matrix):
                matrix_rotated = Matrix.flip(Matrix.transpose(matrix))
                len_n = len(matrix_rotated[0])
                l = int(len_n / 2)

                matrix_updated = []

                for row in matrix_rotated:
                    row_split = Matrix.split_list(row, l, mode="n")
                    row_appended = []
                    for tu in row_split:
                        tem = [order - tu[0] + 1, order - tu[1] + 1]
                        tem.insert(1, tu[1])
                        tem.insert(1, tu[0])
                        row_appended.append(tem)
                    matrix_updated.append(Matrix.concatenate(row_appended))

                return matrix_updated

            n_i = 64
            n_iter = int(log2(n / n_i))

            per_n_i = self.__page_map[64]
            layout_n_i = self.__page_impose_layout(64)
            front_matrix = Matrix.reshape(per_n_i[0], layout_n_i)
            back_matrix = Matrix.reshape(per_n_i[1], layout_n_i)

            for i in range(0, n_iter):
                n_i = 2 * n_i
                front_matrix = matrix_update(n_i, front_matrix)
                back_matrix = matrix_update(n_i, back_matrix)

            vec_front = Matrix.concatenate(front_matrix)
            vec_back = Matrix.concatenate(back_matrix)

            gather_list = vec_front + vec_back

            permutation_i = Permutation(n, gather_list)

        if insert != 1:

            insert_list = []

            if n == 2:
                insert_list = [1, 2]
            else:
                n_total = insert * n
                nlist = [i + 1 for i in range(0, n_total)]
                nlist_splited = (
                    Matrix.split_list(nlist, int(n / 2)) if n != 1 else nlist
                )
                n_splited = 2 * insert

                for i in range(0, insert):
                    insert_list += nlist_splited[i] + nlist_splited[n_splited - i - 1]
            sig_permutation = Permutation(n_total, insert_list).index_mul_partial(
                permutation_i, oper=False
            )
        else:
            sig_permutation = permutation_i

        return sig_permutation


class Signature(Converter):
    __name__ = "booklet"
    __description__ = "basic routine for signature generation"

    @property
    def name(self):
        return Signature.__name__

    @property
    def description(self):
        return Signature.__description__

    def __init__(
        self,
        sig_composition: Union[Tuple[int, int], SigComposition] = (1, 1),
        blank_mode: str = "back",
        riffle: bool = True,
        fold: bool = False,
        paper_format: Union[None, Tuple[float, float]] = None,
    ):
        self.sig_composition: SigComposition = self.__get_sig_composition(
            sig_composition
        )
        self.blank_mode = (
            blank_mode if blank_mode in ["front", "back", "both"] else "back"
        )
        self.fold = fold if type(fold) == bool else False
        self.riffle = riffle if type(riffle) == bool else True
        self.riffle_map = (
            Permutation(2, [1, 2]) if self.riffle else Permutation(2, [2, 1])
        )
        self.paper_format = self.__get_paper_format(
            paper_format
        )  # if format==None, the file format is set.

        print(f"Signature Paper format: {paper_format}, {self.paper_format}")

    # Internal routines
    def __get_sig_composition(self, composition) -> SigComposition:
        if type(composition) == SigComposition:
            return composition
        else:
            sig_leaves = composition[0]
            insert = composition[1]
            return SigComposition(sig_leaves, insert)

    def __get_paper_format(self, format: Tuple[float, float]) -> Tuple[Number, Number]:
        if format == None:
            return None
        if type(format) != tuple and type(format) != list:
            raise TypeError(f"Must be list or tuple{format}, {type(format)}")
        if len(format) > 2 or len(format) == 0:
            raise ValueError("Must be 2 or 1 element tuple or list.")
        if len(format) == 1:
            format_t = [format[0], format[0]]
        else:
            format_t = [format[0], format[1]]
        if Validation.check_number(format[0], True) and Validation.check_number(
            format[1], True
        ):
            if type(format_t[0]) == str and "." in format_t[0]:
                format_t[0] = Decimal(format_t[0])
            else:
                format_t[0] = int(format_t[0])
            if type(format_t[1]) == str and "." in format_t[1]:
                format_t[1] = Decimal(format_t[1])
            else:
                format_t[1] = int(format_t[1])
            return (format_t[0], format_t[1])

    def do(self, do_index: int, manuscript: Manuscript, file_mode: int, format=None):
        blank_num = len(manuscript.pages) % self.sig_composition.leaves
        page_range: list(int) = manuscript.page_range
        if self.blank_mode == "front":
            page_range = ([0] * blank_num) + page_range
        elif self.blank_mode == "back":
            page_range = page_range + ([0] * blank_num)
        else:
            blank_num_front = int(blank_num / 2)
            blank_num_back = blank_num - blank_num_front
            page_range = ([0] * blank_num_front) + page_range + ([0] * blank_num_back)

        if format != None:
            paper_format = self.__get_paper_format(format)
        elif self.paper_format != None:
            paper_format = self.paper_format
        else:
            paper_format = manuscript.file_paper_format

        # split page range per each signature
        sig_blocks = Matrix.split_list(page_range, self.sig_composition.leaves)
        fold = 1 if self.fold and self.sig_composition.layout[0] > 1 else 0
        column = self.sig_composition.layout[1]
        # int(index%2 -(1-fold)/2)
        page_transformation = [
            pypdf.Transformation(),
            pypdf.Transformation()
            .rotate(180)
            .translate(tx=paper_format[0], ty=paper_format[1]),
        ]

        permuted_blocks = []
        for sig_block in sig_blocks:
            permuted_block = self.sig_composition.map.permute_to_list_index(sig_block)
            permuted_block = Permutation.subpermutation_to_list_index(
                self.riffle_map, permuted_block
            )
            permuted_blocks.append(permuted_block)

        new_pdf, new_file = self.get_new_pdf(do_index, manuscript, filemode=file_mode)
        for pages in permuted_blocks:
            for index, i in enumerate(pages):
                if i == 0:
                    new_pdf.add_blank_page(
                        width=paper_format[0], height=paper_format[1]
                    )
                else:
                    rotation = int(int(index / column) % 2 - (1 - fold) / 2)
                    transformation = page_transformation[rotation]
                    page_num = i - 1

                    # print(self.sig_composition.layout)
                    # print(f"index:{index}, page number:{i} rotate:{bool(rotation)}")

                    page = manuscript.pages[page_num]

                    page.scale_to(paper_format[0], paper_format[1])
                    page.mediabox.setLowerLeft([0, 0])
                    page.mediabox.setUpperRight(paper_format)

                    left = manuscript.pdf_origin[0]
                    bottom = manuscript.pdf_origin[1]
                    page.add_transformation(
                        transformation.translate(tx=-left, ty=-bottom)
                    )

                    new_pdf.add_page(page)

        with open(new_file.name, "wb") as f:
            new_pdf.write(f)
        manuscript.meta["/signature"] = str(self.sig_composition.leaves)

        manuscript.pdf_update(new_pdf, new_file.name)
        return True
