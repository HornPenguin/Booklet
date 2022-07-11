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

from PIL import Image

from modules.utils import *
from modules.textdata import *
from modules.gui import HP_Booklet

if __name__ == "__main__":
    text_pady = 3

    logo_width = logo_height = 70
    logo = Image.open(resource_path('logo.png','resource')).resize((logo_width, logo_height), Image.Resampling(1))

    hpbooklet = HP_Booklet(
        icon_path,
        homepage = homepage,
        source = git_repository,
        tutorial = tutorial,
        textpady = text_pady,
        logo = logo
    )

    hpbooklet.basic_inputbox( row=1, column=0, padx = 5, pady =10, width = 370, height = 160, relief="solid", padding="4 4 10 10")
    hpbooklet.basic_outputbox( row=1, column=1, padx = 5, pady =10, width = 370, height = 200, relief="solid", padding="4 4 10 10")

    imposition_iconpaths =  { name: resource_path(f"{name}.png", 'resource') for name in imposition_icon_names}
    imposition_icons = { name: Image.open(imposition_iconpaths[name]) for name in imposition_icon_names}

    hpbooklet.advanced_imposition(imposition_icons, row= 1, column=0, padx = 5, pady= 10, width = 450, height = 220, relief = "solid", padding="4 4 10 10")
    
    printing_iconpaths =  { name: resource_path(f"{name}.png", 'resource') for name in printing_icon_names}
    printing_icons = { name: Image.open(printing_iconpaths[name]) for name in printing_icon_names}
    hpbooklet.advanced_printing(printing_icons, row= 1, column=1, padx = 5, pady= 10, width = 450, height = 140, relief = "solid", padding="4 4 10 10")
    
    hpbooklet.genbutton(row=2, column=0, columnspan =2 ,width = 370, height = 50, padding="2 2 2 2")

    hpbooklet.window.mainloop()