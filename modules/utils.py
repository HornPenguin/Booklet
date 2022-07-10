"""
Miscellaneous uitls 
"""

import webbrowser
from reportlab.lib.units import mm
from reportlab.lib.colors import CMYKColor

# point <-> mm convert
def pts_mm(size:tuple, mode=True)->tuple: #mode: True(pts -> mm), False(mm -> pts)
    """
    :param size: tuple(float, float), tuple of two point or mm unit size.
    :param mode: bool, Determines the direction of conversion. `True`: point to mm, `False`: mm to point.

    Unit conversion between point and mm.
    """
    if mode: #pts to mm
        x = round(size[0]/mm,0)
        y = round(size[1]/mm,0)
        return (x,y)
    else: #mm to pts
        x = size[0] * mm
        y = size[1] * mm
        return (x,y)

# Open webbrowser with a given url
def open_url(url:str)->None:
    return webbrowser.open(url)

# Color utils
color_black = CMYKColor(0, 0, 0, 1)
color_cyan = CMYKColor(1, 0, 0, 0)
color_magenta = CMYKColor(0, 1, 0, 0)
color_yellow = CMYKColor(0, 0, 1, 0)

registration_black = CMYKColor(1,1,1,1)

def hex_to_cmyk(hex:str)->tuple:
    """
    :param hex: str, HEX code string

    Convert HEX code to CMYK code.
    """
    if "#" in hex:
        hex= hex.replace("#", "")
    
    R, G, B  = int(hex[0:2],16), int(hex[2:4],16), int(hex[4:6],16)
    
    R = R/255
    G = G/255
    B = B/255

    K = 1- max(R,G,B)
    C = (1-R-K)/(1 - K)
    M = (1-G-K)/(1 - K)
    Y = (1-B-K)/(1 - K)
    return C, M, Y, K
    
def cmyk_to_rgb(C:float, M:float, Y:float, K:float)->tuple:
    """
    :param C: float, Cyan color code
    :param M: float, Magenta color code
    :param Y: float, Yellow color code
    :param K: float, Key(black) color code

    Convert CMYK code to RGB code.
    """
    R = 255*(1- C) * (1-K)
    G = 255*(1- M) * (1-K)
    B = 255*(1- Y) * (1-K)
    return R, G, B


# Miscellaneous
def split_list(li: list, n:int)->list:
    """
    :param li: list, list to be splited.
    :param n: int, The length of sublist. It must be a divider of the length of :param:`li` list.

    """

    if n <=1:
        return li
    if len(li) %n !=0:
        raise ValueError(f"The length of sublist, {n}, must be a divider of original list, {len(li)}. ")
    
    rlist =[]
    for i in range(0, int(len(li)/n)):
        ni = n*i
        rlist.append([li[ni: ni+n]][0])

    return rlist