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


from typing import Union
from reportlab.lib.units import mm

# point <-> mm convert
def __pts_mm(
    value: Union[int, float, tuple[int, int], tuple[float, float]], mode=True
) -> Union[
    int, float, tuple[int, int], tuple[float, float]
]:  # mode: True(pts -> mm), False(mm -> pts)
    """Unit conversion between point and mm.

    :param value: Tuple of two point or mm unit value.
    :type value: tuple(float, float)
    :param mode: Determines the direction of conversion. :code:`True`: point to mm, :code:`False`: mm to point.
    :type mode: bool, defaults to :code:`True`
    :return: (x, y)
    :rtype: float or int tuple
    """
    if mode:  # pts to mm
        if type(value) == int or type(value) == float:
            x = round(value / mm, 0)
            return x
        else:
            x = round(value[0] / mm, 0)
            y = round(value[1] / mm, 0)
            return (x, y)
    else:  # mm to pts
        if type(value) == int or type(value) == float:
            x = value * mm
            return x
        else:
            x = value[0] * mm
            y = value[1] * mm
            return (x, y)


def pts2mm(value: Union[int, tuple[int, int]]) -> Union[float, tuple[float, float]]:
    """Wrapper of :py:func:`__pts_mm` of point to mm conversion.

    :param value: Point value or point value tuple of length 2.
    :type value: Union[int, tuple[int, int]]
    :return: mm value or mm value tuple of length 2.
    :rtype: Union[float, tuple[float, float]]
    """
    return __pts_mm(value, mode=True)


def mm2pts(value: Union[float, tuple[float, float]]) -> Union[int, tuple[int, int]]:
    """
    Wrapper of :py:func:`__pts_mm` of mm to point conversion.

    :param value: mm value or mm value tuple of length 2.
    :type value: Union[float, tuple[float, float]]
    :return: Point value or point value tuple of length 2.
    :rtype: Union[int, tuple[int, int]]
    """
    return __pts_mm(value, mode=False)


def __pts_pix(
    value: Union[int, float, tuple[int, int], tuple[float, float]], mode: bool = True
) -> Union[float, int, tuple[float, float], tuple[int, int]]:  # 1 pix = 3/4 * (x, pts)
    """
    Unit conversion between point and pixel.
    For :param:`mode`, :code:`True` is point to pixel, and :code:`False` is pixel to point.

    :param value: Point or pixel value or its tuple of length 2.
    :type value: Union[int, float, tuple[int, int], tuple[float, float]]
    :param mode: Direction of conversion, defaults to :code:`True`
    :type mode: bool, optional
    :return: Pixel or point value, or its tuple of length 2.
    :rtype: Union[float, int, tuple[float, float], tuple[int, int]]
    """
    if mode:  # pts -> pix
        pts = value
        pix = pts * (4 / 3)
        remainder = pix - int(pix)
        if remainder > 0.49999:
            pix = int(pix) + 1
        else:
            pix = int(pix)
        return pix
    else:  # pix -> pts
        pix = value
        pts = pix * 0.75
        return pts


def pts2pix(value: Union[float, tuple[float, float]]) -> Union[int, tuple[int, int]]:
    """
    Wrapper of :py:func:`__pts_pix` of point to pixel conversion.

    :param value: Point value or its tuple of length 2
    :type value: Union[float, tuple[float, float]]
    :return: Pixel value or its tuple of length 2
    :rtype: Union[int, tuple[int, int]]
    """
    return __pts_pix(value, mode=True)


def pix2pts(value: Union[int, tuple[int, int]]) -> Union[float, tuple[float, float]]:
    """
    Wrapper of :py:func:`__pts_pix` of pixel to point conversion.

    :param value: Pixel value or its tuple of length 2
    :type value: Union[int, tuple[int, int]]
    :return: Point value or its tuple of length 2
    :rtype: Union[float, tuple[float, float]]
    """
    return __pts_pix(value, mode=False)
