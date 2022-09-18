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


from reportlab.lib.colors import CMYKColor
from typing import Union, Tuple, Literal
import collections

# Reportlab color class supports hex(), rgb(), cmyk() attributes.
Basis_Colors = {
    "black": CMYKColor(0, 0, 0, 1),
    "cyan": CMYKColor(1, 0, 0, 0),
    "magenta": CMYKColor(0, 1, 0, 0),
    "yellow": CMYKColor(0, 0, 1, 0),
    "key": CMYKColor(1, 1, 1, 1),
    "blue": CMYKColor(1, 1, 0, 0),
    "green": CMYKColor(1, 0, 1, 0),
    "red": CMYKColor(0, 1, 1, 0),
    "reg": CMYKColor(1, 1, 1, 0),
}

CMYK_VanDiagram_Sequence = [
    Basis_Colors["cyan"],
    Basis_Colors["blue"],
    Basis_Colors["magenta"],
    Basis_Colors["red"],
    Basis_Colors["yellow"],
    Basis_Colors["green"],
    Basis_Colors["cyan"],
]

color_mode = ["rgb", "cmyk", "hex"]


def __color_conversion(
    value: Union[Tuple[int, int, int], Tuple[float, float, float, float], str],
    i: Literal["rgb", "cmyk", "hex"] = "rgb",
    f: Literal["rgb", "cmyk", "hex"] = "hex",
) -> Union[Tuple[int, int, int], Tuple[float, float, float, float], str]:
    """
    Color representation conversion between [RGB, CMYK, HEX] <-> [RGB, CMYK, HEX].
    RGB value is length 3 integer tuple.
    CMYK value is length 4 float tuple.
    HEX is a formatted string.

    :param value: Color value to convert to other form
    :type value: Union[Tuple[int,int,int], Tuple[float, float, float, float], str]
    :param i: Mode of the given vale, defaults to "rgb"
    :type i: Literal[&quot;rgb&quot;, &quot;cmyk&quot;, &quot;hex&quot;], optional
    :param f: Mode of result, defaults to "hex"
    :type f: Literal[&quot;rgb&quot;, &quot;cmyk&quot;, &quot;hex&quot;], optional
    :raises ValueError: :param:`i` or :param:`f` value is not one of "rgb", "cmyk", "hex".
    :raises ValueError: :code:`i = "rgb"`, Invaild rgb value, not an iterable object.
    :raises ValueError: :code:`i = "rgb"`, Invaild rgb value, its length is not 3.
    :raises TypeError: :code:`i = "rgb"`, Not an integer array, at least one of element is not integer type.
    :raises ValueError: :code:`i = "cmyk"`, Invaild cmyk value, not an iterable object.
    :raises ValueError: :code:`i = "cmyk"`, Invaild cmyk value, its length is not 4.
    :raises TypeError: :code:`i = "cmyk"`, Not a float array, at least one of element is not float type.
    :raises TypeError: :code:`i = "hex"`, Invaild type, it is not a stirng object.
    :raises ValueError: :code:`i = "hex"`, Invaild hex string, its length is not 7.
    :raises ValueError: :code:`i = "hex"`, Invaild hex string, its length is not 7.
    :return: Color representation determinded by :param:`f`.
    :rtype: Union[ Tuple[int, int, int], Tuple[float, float, float, float], str ]
    """
    if i not in color_mode or f not in color_mode:
        raise ValueError(f"Invaild conversion space, they must be in {color_mode}")
    if i == "rgb":
        if not isinstance(value, collections.Iterable):
            raise ValueError("Invaild rgb value, not an iterable object")
        if len(value) != 3:
            raise ValueError("Invaild rgb value, its length is not 3")
        if type(value[0]) != int or type(value[1]) != int or type(value[2]) != int:
            raise TypeError(
                "Not an integer array, at least one of element is not integer type."
            )
        r, g, b = int(value[0]), int(value[1]), int(value[2])
    elif i == "cmyk":
        if not isinstance(value, collections.Iterable):
            raise ValueError("Invaild cmyk value, not an iterable object")
        if len(value) != 4:
            raise ValueError("Invaild cmyk value, its length is not 4")
        if (
            type(value[0]) != float
            or type(value[1]) != float
            or type(value[2]) != float
            or type(value[3]) != float
        ):
            raise TypeError(
                "Not a float array, at least one of element is not float type."
            )
        c, m, y, k = value[0], value[1], value[2], value[3]
        r = int(255 * (1 - c) * (1 - k))
        g = int(255 * (1 - m) * (1 - k))
        b = int(255 * (1 - y) * (1 - k))
    elif i == "hex":
        if type(value) != str:
            raise TypeError("Invaild type, it is not a stirng object")
        if len(value) != 7:
            raise ValueError("Invaild hex string, {value} is not of length 7")
        if "#" not in value and len(value) != 6:
            raise ValueError("Invaild hex string, #{value} is not of length 7")
        hex_string = value.replace("#", "") if "#" in value else value
        r, g, b = (
            int(hex_string[0:2], 16),
            int(hex_string[2:4], 16),
            int(hex_string[4:6], 16),
        )
    if f == "rgb":
        return r, g, b
    elif f == "cmyk":
        r_d = r / 255
        g_d = g / 255
        b_d = b / 255
        k = 1 - max(r_d, g_d, b_d)
        c = (1 - r_d - k) / (1 - k)
        m = (1 - g_d - k) / (1 - k)
        y = (1 - b_d - k) / (1 - k)
        return c, m, y, k
    elif f == "hex":
        rcode = str(hex(r)).split("x")[1]
        gcode = str(hex(g)).split("x")[1]
        bcode = str(hex(b)).split("x")[1]
        if len(rcode) == 1:
            rcode = "0" + rcode
        if len(gcode) == 1:
            gcode = "0" + gcode
        if len(bcode) == 1:
            bcode = "0" + bcode
        return "#" + rcode + gcode + bcode


def hex2cmyk(hex: str) -> Tuple[float, float, float, float]:
    """Convert hex string to cmyk.

    :param hex: Hex color formatted string.
    :type hex: str
    :return: Cmyk representation.
    :rtype: Tuple[float, float, float, float]
    """
    return __color_conversion(hex, i="hex", f="cmyk")


def hex2rgb(hex: str) -> Tuple[int, int, int]:
    """
    Convert hex string to rgb.

    :param hex: Hex color formatted string.
    :type hex: str
    :return: Rgb representation.
    :rtype: Tuple[int, int, int]
    """
    return __color_conversion(hex, i="hex", f="rgb")


def cmyk2rgb(cmyk=None, *args, **kwargs) -> Tuple[int, int, int]:
    """
    Convert cmyk to rgb. Support single tuple, list and seperated arguments and keywords.

    Example:

        cmyk2rgb((0.4, 0.3, 0.2, 0.))

        cmyk2rgb([0.4, 0.3, 0.2, 0.])

        cmyk2rgb(0.4, 0.3, 0.2, 0.)

        cmyk2rgb(c = 0.4, m = 0.3, y = 0.2, k = 0.)

    Supported keywords

    * Cyan = 'c', 'C', 'cyan', 'Cyan', 'CYAN'
    * Magenta = 'm', 'M', 'magenta', 'Magenta', 'MAGENTA'
    * Yellow = 'y', 'Y', 'yellow', 'Yellow', 'YELLOW'
    * Key = 'k', 'K', 'key', 'Key', 'KEY'

    :param cmyk: cmyk value, defaults to None
    :type cmyk: _type_, optional
    :return: cmyk vlaue
    :rtype: Tuple[int, int, int]
    """
    if cmyk == None and len(kwargs) == 4:
        cyan_str = ["c", "C", "cyan", "Cyan", "CYAN"]
        magenta_str = ["m", "M", "magenta", "Magenta", "MAGENTA"]
        yellow_str = ["y", "Y", "yellow", "Yellow", "YELLOW"]
        key_str = ["k", "K", "key", "Key", "KEY"]
        for key in kwargs.keys():
            if key in cyan_str:
                c = kwargs[key]
            elif key in magenta_str:
                m = kwargs[key]
            elif key in yellow_str:
                y = kwargs[key]
            elif key in key_str:
                k = kwargs[key]
        cmyk = [c, m, y, k]
    elif len(args) == 3:
        c = cmyk
        m = args[0]
        y = args[1]
        k = args[2]
        cmyk = [c, m, y, k]
    elif len(args) == 0:
        pass
    return __color_conversion(cmyk, i="cmyk", f="rgb")


def cmyk2hex(cmyk=None, *args, **kwargs) -> str:
    """
    Convert cmyk to rgb. Support single tuple, list and seperated arguments and keywords.

    Example:

        cmyk2hex((0.4, 0.3, 0.2, 0.))

        cmyk2hex([0.4, 0.3, 0.2, 0.])

        cmyk2hex(0.4, 0.3, 0.2, 0.)

        cmyk2hex(c = 0.4, m = 0.3, y = 0.2, k = 0.)

    Supported keywords

    * Cyan = 'c', 'C', 'cyan', 'Cyan', 'CYAN'
    * Magenta = 'm', 'M', 'magenta', 'Magenta', 'MAGENTA'
    * Yellow = 'y', 'Y', 'yellow', 'Yellow', 'YELLOW'
    * Key = 'k', 'K', 'key', 'Key', 'KEY'

    :param cmyk: cmyk value, defaults to None
    :type cmyk: tuple, list, argument, keyword argument ...
    :return: hex string
    :rtype: str
    """
    if cmyk == None and len(kwargs) == 4:
        cyan_str = ["c", "C", "cyan", "Cyan", "CYAN"]
        magenta_str = ["m", "M", "magenta", "Magenta", "MAGENTA"]
        yellow_str = ["y", "Y", "yellow", "Yellow", "YELLOW"]
        key_str = ["k", "K", "key", "Key", "KEY"]
        for key in kwargs.keys():
            if key in cyan_str:
                c = kwargs[key]
            elif key in magenta_str:
                m = kwargs[key]
            elif key in yellow_str:
                y = kwargs[key]
            elif key in key_str:
                k = kwargs[key]
        cmyk = [c, m, y, k]
    elif len(args) == 3:
        c = cmyk
        m = args[0]
        y = args[1]
        k = args[2]
        cmyk = [c, m, y, k]
    elif len(args) == 0:
        pass
    return __color_conversion(cmyk, i="cmyk", f="hex")


def rgb2cmyk(rgb=None, *args, **kwargs) -> Tuple[float, float, float, float]:
    """
    Convert rgb to cmyk. Support single tuple, list and seperated arguments and keywords.

    Example:

        rgb2cmyk((100, 230, 12))

        rgb2cmyk([100, 230, 12])

        rgb2cmyk(100, 230, 12)

        rgb2cmyk(r= 100, g= 230, b = 12)


    :param rgb: rgb value, defaults to None
    :type rgb: tuple, list, argument, keyword argument ...
    :return: cmyk value
    :rtype: Tuple[float, float, float, float]
    """
    if rgb == None and len(kwargs) == 3:
        red_str = ["r", "R", "red", "Red", "RED"]
        green_str = ["g", "G", "green", "Green", "GREEN"]
        blue_str = ["b", "B", "blue", "Blue", "BLUE"]
        for key in kwargs.keys():
            if key in red_str:
                r = kwargs[key]
            if key in green_str:
                g = kwargs[key]
            if key in blue_str:
                b = kwargs[key]
        rgb = [r, g, b]
    elif len(args) == 2:
        r = rgb
        g = args[0]
        b = args[1]
        rgb = [r, g, b]
    elif len(args) == 0:
        pass
    return __color_conversion(rgb, i="rgb", f="cmyk")


def rgb2hex(rgb=None, *args, **kwargs) -> str:
    """
    Convert rgb to hex. Support single tuple, list and seperated arguments and keywords.

    Example:

        rgb2hex((100, 230, 12))

        rgb2hex([100, 230, 12])

        rgb2hex(100, 230, 12)

        rgb2hex(r= 100, g= 230, b = 12)


    :param rgb: rgb value, defaults to None
    :type rgb: tuple, list, argument, keyword argument ...
    :return: hex string
    :rtype: str
    """
    if rgb == None and len(kwargs) == 3:
        red_str = ["r", "R", "red", "Red", "RED"]
        green_str = ["g", "G", "green", "Green", "GREEN"]
        blue_str = ["b", "B", "blue", "Blue", "BLUE"]
        for key in kwargs.keys():
            if key in red_str:
                r = kwargs[key]
            if key in green_str:
                g = kwargs[key]
            if key in blue_str:
                b = kwargs[key]
        rgb = [r, g, b]
    elif len(args) == 2:
        r = rgb
        g = args[0]
        b = args[1]
        rgb = [r, g, b]
    elif len(args) == 0:
        pass
    return __color_conversion(rgb, i="rgb", f="hex")
