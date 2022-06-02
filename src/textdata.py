

git_repository = r"https://github.com/HornPenguin/Booklet"
homepage = r"https://www.hornpenguin.com/%EC%84%9C%EB%B9%84%EC%8A%A4/booklet"


about_text= r'''
HornPenguin Booklet provides various routines for printing and press.

Copyright (c) 2022 HornPenguin Co.
All right reserved.

Contact: support@hornpenguin.com
'''

license = r'''
BSD 3-Clause License

Copyright (c) 2022, HornPenguin Co.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

----------------------------------------------------------------------------------
    This program uses PyPDF2 module which is distributed under BSD-3 license. 
    Below part is a credit for original authors of PYPDF2

    Copyright (c) 2006-2008, Mathieu Fenniak
    Some contributions copyright (c) 2007, Ashish Kulkarni <kulkarni.ashish@gmail.com>
    Some contributions copyright (c) 2014, Steve Witham <switham_github@mac-guyver.com>

     Full texts of the license is same with above texts 
'''

format_head = ["Format", "width(mm)", "height(mm)"]
format_table = [
    ("A3",297,420),
    ("A4",210,297),
    ("A5",148,210),
    ("B3",353,500),
    ("B4",250,353),
    ("B5",176,250),
    ("B6",125,176),
    ("JIS B3",364,515),
    ("JIS B4",257,364),
    ("JIS B5",182,257),
    ("JIS B6",128,182),
    ("Letter",216,279),
    ("Legal",216,356),
    ("Tabloid",279,432),
    ("Gov Letter",203,267),
    ("Gov Legal",216,279),
    ("ANSI A",216,279),
    ("ANSI B",279,432),
    ("Arch A",229,305),
    ("Arch B",305,457)
]

PaperFormat = { #mm
    "Default": "0x0",
    "A3": "297x420",
    "A4": "210x297",
    "A5": "148x210",
    "B3" : "353x500",
    "B4" : "250x353",
    "B5": "176x250",
    "B6": "125x176",
    "JIS B3" :"364x515 ",
    "JIS B4": "257x364",
    "JIS B5": "182x257",
    "JIS B6": "128x182",
    "Letter" : "216x279",
    "Legal" : "215x275",
    "Tabloid": "279x432",
    "Gov Letter":"203x267",
    "Gov Legal":"216x279",
    "ANSI A":"216x279",
    "ANSI B":"279x432",
    "ARCH A":"229x305",
    "ARCH B":"305x457"
}
