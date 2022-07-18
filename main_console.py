#BSD 3-Clause License
#
#Copyright (c) 2022, HornPenguin Co.
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


__author__ = "Hyunseong Kim"
__company__ = "HornPenguin"
__version__ = "0.0.1"
__license__ = "BSD license"
name = "Booklet"

import modules.signature as sig
import modules.textdata as textdata
import argparse
import sys, os, re

import PyPDF2 as pypdf

des = """PDF modulation for printing and press
----------------------------------------------------"""
epi = "github: https://github.com/HornPenguin/Booklet \nsupport: support@hornpenguin.com"

page_range_size = 0

class Format_Help(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        length = 15
        print('Format'.ljust(length)+'width(mm)'.ljust(length)+'height(mm)'.ljust(length))
        for format in textdata.format_table:
            print(f"{format[0]}".ljust(length)+f"{format[1]}".ljust(length)+f"{format[2]}".ljust(length))
        
        setattr(namespace, self.dest, values)

def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)

def dir_path(string):
    if os.path.isdir(string) or os.path.isfile(string):
        return string
    else:
        raise NotADirectoryError(string)

#range validation
range_validation_re = re.compile(textdata.re_get_ranges)
character_vailidation_re = re.compile(textdata.re_check_permited_character)

class NoInput(Exception):
    pass

def range_validation(string): #only max
    text = string.replace(" ","")
    #self.pagerange_var.set(text)
    vaild= True
    if character_vailidation_re.search(text) != None:
        raise ValueError(f"{string} is not a vaild range.")  
    else:
        return string
        
def color_check(string):
    text = string
    if '#' in text:
        text =  text[1:]
    
    if len(text) != 6:
        raise ValueError
    else:
        on = '0x' + text[0:2]
        tw = '0x' + text[2:4]
        th = '0x' + text[4:6]
        try:
            int(on, 16)
            int(tw, 16)
            int(th, 16)
        except:
            raise ValueError
    return string

def sig_compose():
    pass

parser = argparse.ArgumentParser(
    prog=f'{name}',
    description=des,
    epilog=epi
    )

#program version
parser.add_argument('--version', action='version', version='%(prog)s '+f'{__version__}')
#Addtional help
parser.add_argument('--format-help', action=Format_Help, nargs=0, help="print table of paper format lists.")

#file path
inputgroup = parser.add_mutually_exclusive_group()
inputgroup.add_argument('inputfile', type=file_path, nargs='?')
inputgroup.add_argument('-i', '--input', nargs=1, type=file_path, help='The input pdf file path')
outputgroup = parser.add_mutually_exclusive_group()
outputgroup.add_argument('outputpath', type=dir_path, nargs='?')
outputgroup.add_argument('-o', '--output', nargs=1, type=dir_path, help='The ouput file path')

parser.add_argument('-n', '--name', type=str, help='output file name')

#signature options
parser.add_argument('--page-range', type=range_validation, nargs='*', help='The page range to moldulate in the input file. Example: 1-3, 10, 14-20')
parser.add_argument('--blank-mode', choices=[ 'back', 'front', 'both'], default='back', help='where additional blank pages are added, default = \'back\'')
parser.add_argument('--sig-composition', nargs=2 , type=sig_compose, default=(1,4), help='')
parser.add_argument('--riffle-direction', nargs=1, type = str, choices=['right', 'left'], default='right', help='riffling direction of signature, old asian book has \'left\' riffling direction. Default value=\'right\'')
parser.add_argument('--fold', action="store_true")
formatgroup = parser.add_mutually_exclusive_group()
formatgroup.add_argument('--format', nargs=1, type=str, choices=list(textdata.PaperFormat.keys()), default="Default", help="Output paper size format of signature, \'Default\': conserves original file paper size. See options with \'--format-help\'.")
formatgroup.add_argument('--custom-format', nargs=2, type=float, help='custom paper size(mm) set, width and height respectively. \'--custom-format=200.2 150.1\' means 200.5mm width, 150.1mm height size.')
parser.add_argument('--imposition', action="store_true", help='default conversion only rearrange and rotate, this option locates them in each pages.')
parser.add_argument('--split', action="store_true", help="split pdf pages with each signatures.")
parser.add_argument('--trim', action="store_true", help="add trim marker in imposition pdf.")
parser.add_argument('-reg','--registration', action="store_true", help= "add registration markers in imposition pdf.")
parser.add_argument('--cmyk', action="store_true" ,help= "add cmyk markers in imposition pdf.")
parser.add_argument('--sigproof', type=color_check, default="#729fcf", nargs=1,help='add signature proof that help to check order and missing signature. colorcode is a hex code. default = #729fcf')


if __name__ == "__main__":
    args = parser.parse_args()

    # print info--------------------------

    # generate----------------------------

    #sig.generate_signature(
    #inputfile = , 
    #output = ,
    #pagerange = , 
    #blank= ,
    #sig_n= ,
    #riffle= ,
    #fold= ,
    #format= ,
    #imposition= ,
    #split= ,
    #trim= ,
    #registration= ,
    #cmyk= ,
    #sigproof= 
    #)
    
