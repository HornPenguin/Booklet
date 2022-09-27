# Copyright (c) 2022, Hyunseong Kim <qwqwhsnote@gm.gist.ac.kr>
#
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


# 1, 2 dimension matrix operation based on default list type

import collections
from math import sin, cos

# Utils

def rotate_2dim(vec, angle):
    co = cos(angle)
    si = sin(angle)
    x_new = co* vec[0] -si * vec[1]
    y_new = si * vec[0] + si *vec[1]
    return [x_new, y_new]

def split_list(list1d: list, n: int, mode="l") -> list:
    if not isinstance(list1d, collections.Iterable):
        raise TypeError("The given object is not an iterable object.")
    if mode != "l" and mode != "n":
        raise ValueError("The 'mode' parameter must be 'l' or 'n', current = {mode}")
    num = n
    length_list = len(list1d)
    if mode == "n":
        if length_list % num != 0:
            raise ValueError(
                "The length of the given list and the sublist length must have a divider relationship."
            )
        num = int(length_list / num)
        mode = "l"
    if mode == "l":
        if num <= 1:
            return list1d
        if len(list1d) % num != 0:
            raise ValueError(
                f"The length of sublist, {num}, must be a divider of original list, {len(list1d)}. "
            )
        rlist = []
        for i in range(0, int(length_list / num)):
            ni = num * i
            rlist.append([list1d[ni : ni + num]][0])
    return rlist

def transpose(list2d: list) -> list:
    row_length = len(list2d)
    column_length = len(list2d[0])
    t = list()
    for i in range(0, column_length):
        t.append([])
    for i in range(0, column_length):
        for j in range(0, row_length):
            t[i].append(list2d[j][i])
    return t

def flip(matrix: list) -> list:
    size = len(matrix)
    f = list()
    for i in range(0, size):
        f.append(matrix[size - i - 1])
    return f

def concatenate(matrix: list[list]) -> list:
    length = len(matrix)
    rlist = list()
    for i in range(0, length):
        for element in matrix[i]:
            rlist.append(element)
    return rlist

def reshape(list1d: list, shape) -> list[list]:
    size1d = len(list1d)
    if size1d != shape[0] * shape[1]:
        raise ValueError("The list length and shape are not matched each other.")
    return split_list(list1d, shape[0], mode="n")


