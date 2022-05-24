git_repository = r"https://github.com/HornPenguin/Booklet"
homepage = r"https://www.hornpenguin.com/"
about_text= r'''
Copyright (c) 2022 Kim, Hyunseong
All right reserved.

This program is using PyPDF2 library which is ditributed under
BSD-3 license.
See details of license in LICENSE file in repository.
'''
format_table = r'''
Format (mm)x(mm)

A4      210x297
A5      148x210
B5      176x250
B6      125x176
JIS B5  182x257
JIS B6  128x182
Letter  216x279
Legal   215x275
'''

PaperFormat = { #mm
    "Default": "0x0",
    "A4": "210x297",
    "A5": "148x210",
    "B5": "176x250",
    "B6": "125x176",
    "JIS B5": "182x257",
    "JIS B6": "128x182",
    "Letter" : "216x279",
    "Legal" : "215x275"
}
