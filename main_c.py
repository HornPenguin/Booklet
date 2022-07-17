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
__name__ = "Booklet"

import modules.signature as sig
import modules.textdata as textdata
import argparse
import sys

des = "PDF modulation for printing and press"
epi = "github: https://github.com/HornPenguin/Booklet \nsupport: support@hornpenguin.com"

class format_help(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        print('Format\twidth(mm)\theight(mm)')
        for format in textdata.format_table:
            print(format)
            
parser = argparse.ArgumentParser(
    prog=f'{__company__} {__name__}',
    description=des,
    epilog=epi
    )

parser.add_argument('-i', '-input', nargs='?', type=str, help='The input pdf file path')
parser.add_argument('-o', '-output', nargs='?', type=str, help='The input pdf file path')
parser.add_argument('--version', action='version', version='%(prog)s '+f'{__version__}')

parser.add_argument('-page_range', type=str, nargs='*', help='The page range to moldulate in the input file. Example: 1-3, 10, 14-20')

parser.add_argument('--format-help', action=format_help)

if __name__ == "__main__":
    arguments = sys.argv[1:]

    if len(arguments) == 0:
        print("No argumnets, see help with \'--h\', \'-help\'")
        sys.exit()
    

    sig.generate_signature(
    inputfile = , 
    output = ,
    pagerange = , 
    blank= ,
    sig_n= ,
    riffle= ,
    fold= ,
    format= ,
    imposition= ,
    split= ,
    trim= ,
    registration= ,
    cmyk= ,
    sigproof= ,
    progress=  
    )
    
