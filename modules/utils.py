"""
Miscellaneous uitls 
"""
import os, sys
from pathlib import Path
from typing import Union, Tuple, NoReturn

import webbrowser
from reportlab.lib.units import mm
from reportlab.lib.colors import CMYKColor
import PyPDF2 as pypdf


re_get_ranges = r"([ ]{0,}\d+[ ]{0,}-{1,1}[ ]{0,}\d+[ ]{0,}|[ ]{0,}\d+[ ]{0,}[^,-])"
re_check_permited_character=  r"([^-,\d\s])+?"


# system related routine

def resources_path(relative_path:str, directory:str)->str:
        #Get absolute path to resources, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, directory, relative_path)


# point <-> mm convert
def pts_mm(size:tuple, mode=True)->tuple: #mode: True(pts -> mm), False(mm -> pts)
    """Unit conversion between point and mm.

    :param size: Tuple of two point or mm unit size.
    :type size: tuple(float, float)
    :param mode: Determines the direction of conversion. :code:`True`: point to mm, :code:`False`: mm to point.
    :type mode: bool, default= :code:`True`
    
    :return: (x, y)
    :rtype: float tuple
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
def open_url(url:str)->NoReturn:
    return webbrowser.open(url)

# Color utils
color_black = CMYKColor(0, 0, 0, 1)
color_cyan = CMYKColor(1, 0, 0, 0)
color_magenta = CMYKColor(0, 1, 0, 0)
color_yellow = CMYKColor(0, 0, 1, 0)

registration_black = CMYKColor(1,1,1,1)

def hex_to_cmyk(hex:str)->Tuple[float,float,float,float]:
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
    
def cmyk_to_rgb(C:float, M:float, Y:float, K:float)->Tuple[int, int, int]:
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
    return int(R), int(G), int(B)

def rgb_to_hex(r:int, g:int, b:int)->str:
    rcode = str(hex(r)).split('x')[1]
    gcode = str(hex(g)).split('x')[1]
    bcode = str(hex(b)).split('x')[1]

    if len(rcode) == 1:
        rcode = '0'+rcode
    if len(gcode) == 1:
        gcode = '0'+gcode
    if len(bcode) == 1:
        bcode = '0'+bcode
    return '#'+  rcode + gcode + bcode

# List routines 
def split_list(li: list, n:int, mode='l')->list:
    """
    :param li: list, list to be splited.
    :param n: int, The length of sublist. It must be a divider of the length of :param:`li` list.
    :param mode: str, The mode of split, `l`: length of sublist, `n`: number of sublist
    """
    if mode != 'l' and mode != 'n':
        raise ValueError('The \'mode\' parameter must be \'l\' or \'n\', current = {mode}')

    num = n
    l_li = len(li)
    if mode =='n':
        if l_li%num !=0:
            raise ValueError('The length of the given list and the sublist length must have a divider relationship.')
        num = int(l_li/num)
        mode ='l'

    if mode == 'l':
        if num <=1:
            return li
        if len(li) %num !=0:
            raise ValueError(f"The length of sublist, {num}, must be a divider of original list, {len(li)}. ")

        rlist =[]
        for i in range(0, int(l_li/num)):
            ni = num*i
            rlist.append([li[ni: ni+num]][0])

    return rlist 
def transpose(matrix:list)->list:
    size = len(matrix)

    t = list()
    for i in range(0, size):
        t.append([])
    
    for i in range(0, size):
        for j in range(0,size):
            t[i].append(matrix[j][i])
    
    return t
def flip(matrix): #axis=0
    size = len(matrix)

    f = list()
    for i in range(0, size):
        f.append(matrix[size-i-1])
    
    return f

def concatenate(lists):
    length = len(lists)

    rlist = list()
    for i in range(0, length):
        for element in lists[i]:
            rlist.append(element)
    
    return rlist

def reshape(list_1d, shape):
    size_1d = len(list_1d)
    if size_1d != shape[0] * shape[1]:
        raise ValueError("The list length and shape are not matched each other.")
    return split_list(list_1d, shape[0], mode='n')
# Miscellaneous
def get_page_range(page_range_string:str)->list:
    page_range = page_range_string.replace(" ", "")

    rlist = []

    for st in page_range.split(","):
        if '-' in st:
            i, l = st.split("-")
            i = int(i)
            l = int(l)
            r = l-i+1

            rlist = rlist +[i + d for d in range(0,r)]
        else:
            rlist.append(int(st))
    
    return rlist

def get_file_info(path_string:str)->Tuple[Union[bool, str],Union[bool, str],Union[bool, int],Union[bool, list[float,float]]]:

    if type(path_string) != str:
        raise TypeError(f"Given path must be a string variable. Current:{type(path_string)}")
    
    path = Path(path_string)

    if not path.is_file():
        raise ValueError("File {path} does not exist.")

    pdf = pypdf.PdfFileReader(path)

    page_num = pdf.getNumPages()

    if page_num != 0: #check whether pdf is empty or not.
        pdfinfo = pdf.metadata

        title = pdfinfo['/Title'] if '/Title' in pdfinfo.keys() else 'None'
        authors = pdfinfo['/Author'] if '/Author' in pdfinfo.keys() else 'Unkown'

        page_size=  [float(pdf.getPage(0).mediaBox.width), float(pdf.getPage(0).mediaBox.height)]

        return title, authors, page_num, page_size
    
    return False, False, False, False