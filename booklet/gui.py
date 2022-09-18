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
# DAMAGES (INCLUDING, BUT NOT LIMITE D TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import platform, os, sys
from functools import partial
import re
from math import log2

#tkinter----------------------------------
import tkinter as tk
from tkinter import filedialog
if platform.system() != "Darwin":
    from tkinter import ttk
else:
    import tkmacosx as ttk #Mac OS specific module
from tkinter.colorchooser import askcolor

# 3rd parties----------------------------
from PIL import Image, ImageTk
import simpleaudio
import PyPDF2 as pypdf


# Project modules-----------------------------------------------

from booklet.core.manuscript import Manuscript
from booklet.core.modifiers import *
import booklet.data as data
from booklet.utils.misc import *
from booklet.utils.conversion import mm2pts, pts2mm
from booklet.utils.color import hex2cmyk, cmyk2rgb, rgb2hex


# UI--------------------------------------------------------------------------------------------
class Booklet:
    """Main GUI module
    """
    def __init__(
        self,
        icon_path,
        homepage,
        source,
        tutorial,
        textpady,
        logo,
        icons,
        beep_file,
        re_range_validation=data.re_get_ranges,
        re_character_validation=data.re_check_permited_character,
        fix=False,
        width=390,
        height=780
    ):
        """init

        :param icon_path: Program app icon path.
        :type icon_path: _type_
        :param homepage: Company url.
        :type homepage: _type_
        :param source: _description_
        :type source: _type_
        :param tutorial:tutorial page url.
        :type tutorial: _type_
        :param textpady: Gui setting, padding value. `y` direction.
        :type textpady: _type_
        :param logo: Gui setting, ui logo image path.
        :type logo: _type_
        :param icons: _description_
        :type icons: _type_
        :param beep_file: _description_
        :type beep_file: _type_
        :param re_range_validation: Regular expression to validate the range of pages., defaults to data.re_get_ranges
        :type re_range_validation: _type_, optional
        :param re_character_validation: Regular expression to confirm vaild characters in page ragne input., defaults to data.re_check_permited_character
        :type re_character_validation: _type_, optional
        :param fix: ui setting, tkinter gui window size modulation permission setting., defaults to False
        :type fix: bool, optional
        :param width: Width of main window. It is not absolute setting, defaults to 390
        :type width: int, optional
        :param height: Height of main window. It is not absolute setting, defaults to 780
        :type height: int, optional
        """

        self.url_homepage = homepage
        self.url_source = source
        self.url_tutorial = tutorial

        self.fix = fix
        self.window_width = width
        self.window_height = height

        self.beep_file = beep_file

        self.window = tk.Tk()
        self.window.call("source", resources_path("azure.tcl", "resources"))
        self.window.call("set_theme", "light")
        self.window.title("HornPenguin Booklet")

        self.range_validation_re = re.compile(re_range_validation)
        self.character_validation_re = re.compile(re_character_validation)

        # Tab: basic, Advanced
        self.Tabwindow = ttk.Notebook(self.window)
        self.Tabwindow.grid(row=1, column=0)

        self.tab_basic = ttk.Frame(self.Tabwindow)
        self.tab_advance = ttk.Frame(self.Tabwindow)
        self.tab_utils = ttk.Frame(self.Tabwindow)

        self.Tabwindow.add(self.tab_basic, text="basic")
        self.Tabwindow.add(self.tab_advance, text="advanced")
        self.Tabwindow.add(self.tab_utils, text="utils")

        self.initiate_window()

        platform_name = platform.system()
        self.platform_linux = True if platform_name == "Linux" else False
        self.platform_mac = True if platform_name == "Darwin" else False

        self.logo = ImageTk.PhotoImage(logo, master=self.window)
        if self.platform_linux:
            self.window.tk.call("wm", "iconphoto", self.window._w, self.logo)
        self.icon_path = icon_path
        self.icon_setting(self.window)

        self.icons = icons

        # Menu setting
        # Help: About, Format, Tutorial, License, Contact, Source, homepage, support

        self.menu = tk.Menu(self.window)
        self.menu_help = tk.Menu(self.menu, tearoff=0)
        self.initiate_menu()
        self.window.configure(menu=self.menu)

        # Text pad
        self.text_pady = textpady

        # input_file info

        self.title = tk.StringVar(value="")
        self.author = tk.StringVar(value="")
        self.page_n = tk.IntVar(value=0)
        self.page_range_size = tk.IntVar(value=0)
        self.page_format = tk.StringVar(value="")
        self.filename = tk.StringVar(value="")

        self.addBlankpages = tk.IntVar(value=0)
        self.foldvalue = tk.BooleanVar(value=False)

        # Advanced variables
        # Paper size: h x w
        # Page range: []
        # Fold option: Sheet num = n1 x n2 <- ratio modification
        # Imposition option: On, Off
        # Sig Proof: color option
        # Attachement PDF: Cover and back: front, back, none

        self.pagerange_var = tk.StringVar(value="")
        self.ns = tk.IntVar(value=4)

        self.custom_width = tk.IntVar(value=0)
        self.custom_height = tk.IntVar(value=0)

        self.customformatbool = tk.BooleanVar(value=False)
        self.impositionbool = tk.BooleanVar(value=True)
        self.splitpersigbool = tk.BooleanVar(value=False)
        self.sig_color = tk.StringVar(value="#729fcf")

        self.margin = tk.IntVar(value = 20)

        # Printing--------------------------------------------------------

        self.sigproofbool = tk.BooleanVar(value=False)
        self.trimbool = tk.BooleanVar(value=False)
        self.registrationbool = tk.BooleanVar(value=False)
        self.cmykbool = tk.BooleanVar(value=False)

        # Window setting
        self.basic_inputbox(
            row=1,
            column=0,
            padx=5,
            pady=10,
            width=370,
            height=160,
            relief="solid",
            padding="4 4 10 10",
        )
        self.basic_outputbox(
            row=1,
            column=1,
            padx=5,
            pady=10,
            width=370,
            height=200,
            relief="solid",
            padding="4 4 10 10",
        )

        self.advanced_imposition(
            row=1,
            column=0,
            padx=5,
            pady=10,
            width=450,
            height=220,
            relief="solid",
            padding="4 4 10 10",
        )

        self.advanced_printing(
            row=1,
            column=1,
            padx=5,
            pady=10,
            width=450,
            height=140,
            relief="solid",
            padding="4 4 10 10",
        )

        self.utils_note(
            row =1,
            column =0,
            padx=5,
            pady=10,
            width=450,
            height=220,
            relief="solid",
            padding="4 4 10 10",
        )
        self.utils_misc(
            row =1,
            column =1,
            padx=5,
            pady=10,
            width=450,
            height=220,
            relief="solid",
            padding="4 4 10 10",
        )

        self.genbutton(
            row=2, column=0, columnspan=2, width=370, height=50, padding="2 2 2 2"
        )
    def icon_setting(self, window):
        try: #Linux environment tkinter does not support and makes an error
            window.iconbitmap(self.icon_path)
        except:
            pass

    def initiate_window(self):
        self.window.winfo_height
        x = int((self.window.winfo_screenwidth() - self.window.winfo_width()) / 2)
        y = int((self.window.winfo_screenheight() - self.window.winfo_height()) / 2)

        if self.fix:
            self.window.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.window.resizable(False, True)

        # Stack top of windows arrangement at beginning of program
        self.window.attributes("-topmost", True)
        self.window.update()
        self.window.attributes("-topmost", False)

    def popup_window(
        self,
        text:Union[str, list[str]],
        title:str,
        tpadx=10,
        tpady=20,
        fix=False,
        align="center",
        button_text="Ok",
        scroll=False,
    ):
        """Common features of popup window
        
        """
        sub_window = tk.Toplevel(self.window)
        sub_window.title(title)
        sub_window.resizable(False, True)
        
        self.icon_setting(sub_window)

        if not hasattr(text, "__iter__"):
            text = [text]

        if scroll: # add scroll bar to right of window
            frame = ttk.Frame(sub_window)
            scrollbar = ttk.Scrollbar(frame, orient="vertical")
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y, anchor=tk.E)
            text_value = tk.Text(frame)
            for te in text:
                text_value.insert(tk.END, te)

            text_value.pack(side=tk.TOP, padx=3, pady=tpady, fill=tk.X, anchor=tk.W)

            text_value.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)
            scrollbar.config(command=text_value.yview)

            frame.pack(side=tk.TOP)

        else:
            for te in text:
                ttk.Label(sub_window, text=te, anchor=align).pack(
                    padx=tpadx, pady=tpady
                )

        destorybutton = ttk.Button(
            sub_window, text=button_text, width=15, comman=sub_window.destroy
        )
        destorybutton.pack(side=tk.BOTTOM, padx=int(2 * tpadx), pady=int(10))

        if fix:
            sub_window.transient(self.window)
            sub_window.grab_set()
            self.window.wait_window(sub_window)
        return 0

    # Popup table routines
    def popup_window_table(
        self,
        width,
        height,
        column_names,
        data,
        title,
        tpadx=10,
        tpady=2.5,
        fix=False,
        align="center",
    ):
        sub_window = tk.Toplevel(self.window)
        sub_window.title(title)
        sub_window.geometry(f"{width}x{height}")
        if fix:
            sub_window.resizable(True, True)
        else:
            sub_window.resizable(False, False)

        self.icon_setting(sub_window)
        

        table = ttk.Treeview(sub_window, selectmode="browse", height=36)
        table.pack(fill="both")
        table["column"] = column_names

        table.column("#0", width=0, stretch=tk.NO)
        table.heading("#0", text="", anchor=tk.W)
        # Head and column setting
        for x in column_names:
            table.column(x, width=100, anchor=align)
            table.heading(x, text=x, anchor=align)

        # Data innsert

        for i, d in enumerate(data):
            table.insert(parent="", index="end", iid=i, values=d)

    def initiate_menu(self):
        # Help: About, Format, Tutorial, License, support
        self.menu.add_cascade(label="Help", menu=self.menu_help)

        about_window = partial(
            self.popup_window,
            text=data.about_text,
            title="About",
            tpadx=10,
            tpady=2.5,
            fix=False,
        )
        self.menu_help.add_command(label="About", command=about_window)

        format_window = partial(
            self.popup_window_table,
            320,
            480,
            data.format_head,
            data.format_table,
            "Paper Format",
            30,
            2.5,
            False,
        )
        self.menu_help.add_command(label="Paper Format", command=format_window)
        self.menu_help.add_command(
            label="Tutorial", command=partial(open_url, self.url_tutorial)
        )
        self.menu_help.add_command(
            label="Source", command=partial(open_url, self.url_source)
        )

        license = partial(
            self.popup_window,
            text=data.license,
            title="License",
            tpadx=10,
            tpady=0,
            fix=False,
            scroll=True,
        )

        self.menu_help.add_command(label="License", command=license)

    def genbutton(self, row, column, width, height, padding, columnspan=1):
        self.Frame_button = ttk.Frame(
            master=self.window,
            width=width,
            height=height,
            borderwidth=0,
            padding=padding,
        )

        self.Generate_button = ttk.Button(
            self.Frame_button,
            text="Generate",
            width=25,
            command=partial(self.gen_button_action),
        )
        self.Generate_button.pack(side=tk.RIGHT, pady=18, anchor="e")
        self.Generate_button.config(state=tk.DISABLED)

        self.Frame_button.grid(row=row, column=column, columnspan=columnspan)

    # UI
    # -- Tab Basic
    def basic_inputbox(
        self, row, column, padx, pady, width, height, relief, padding, entry_width=41
    ):

        self.Frame_input = ttk.LabelFrame(
            master=self.tab_basic,
            text="Manuscript",
            width=width,
            height=height,
            relief=relief,
            padding=padding,
        )

        # self.input_text = ttk.Label(self.Frame_input, text="Manuscript", justify=tk.LEFT, anchor='w')
        # self.input_text.grid(row=0, column=0, sticky = tk.W, padx =3)
        self.input_entry = ttk.Entry(self.Frame_input, width=entry_width)
        self.input_button = ttk.Button(
            self.Frame_input, text="...", width=3, command=partial(self.__event_open_file)
        )

        self.title_value = ttk.Label(
            self.Frame_input, textvariable=self.title, wraplengt=200
        )
        self.author_value = ttk.Label(
            self.Frame_input, textvariable=self.author, wraplengt=200
        )
        self.page_n_value = ttk.Label(
            self.Frame_input, textvariable=self.page_n, wraplengt=200
        )
        self.page_for_value = ttk.Label(
            self.Frame_input, textvariable=self.page_format, wraplengt=200
        )

        self.title_label = ttk.Label(self.Frame_input, text=f"Title")
        self.author_label = ttk.Label(self.Frame_input, text=f"Author(s)")
        self.page_n_label = ttk.Label(self.Frame_input, text=f"Pages")
        self.page_for_label = ttk.Label(self.Frame_input, text=f"Format")

        self.logo_icon = ttk.Label(self.Frame_input, image=self.logo, cursor="hand2")
        self.logo_icon.photo = self.logo
        self.logo_icon.bind("<Button-1>", lambda e: open_url(self.url_homepage))

        self.input_entry.grid(row=1, column=0, columnspan=3, padx=3, ipadx=5)
        self.input_button.grid(row=1, column=3)

        self.title_label.grid(row=2, column=0, pady=self.text_pady)
        self.title_value.grid(row=2, column=1, columnspan=5, pady=self.text_pady)

        self.author_label.grid(row=3, column=0, pady=self.text_pady)
        self.author_value.grid(row=3, column=1, columnspan=5, pady=self.text_pady)

        self.page_n_label.grid(row=4, column=0, pady=self.text_pady)
        self.page_n_value.grid(row=4, column=1, columnspan=5, pady=self.text_pady)

        self.page_for_label.grid(row=5, column=0, pady=self.text_pady)
        self.page_for_value.grid(row=5, column=1, columnspan=5, pady=self.text_pady)

        self.logo_icon.grid(row=6, column=0, columnspan=6, pady=self.text_pady)

        self.Frame_input.grid(
            row=row,
            column=column,
            ipadx=padx,
            padx=(3 * padx, 3 * padx),
            pady=(3 * pady, 3 * pady),
            sticky="ns",
        )

        return 0

    def basic_outputbox(
        self, row, column, padx, pady, width, height, relief, padding, entry_width=41
    ):

        self.Frame_output = ttk.LabelFrame(
            master=self.tab_basic,
            text="Output",
            width=width,
            height=height,
            relief=relief,
            padding=padding,
        )

        # self.output_text = ttk.Label(self.Frame_output, text="Output", justify=tk.LEFT, anchor='w')
        # self.output_text.grid(row=0, column=0, sticky = tk.W, padx =3)
        self.output_entry = ttk.Entry(self.Frame_output, width=entry_width)
        self.output_entry.grid(row=1, column=0, columnspan=3, padx=3, ipadx=5)
        ttk.Button(
            self.Frame_output,
            text="...",
            width=3,
            command=partial(self.__event_open_output_directory),
        ).grid(row=1, column=3)

        self.filename_label = ttk.Label(self.Frame_output, text="File name")
        self.filename_entry = ttk.Entry(
            self.Frame_output, textvariable=self.filename, width=int(entry_width / 2)
        )

        self.text_leaves = ttk.Label(
            self.Frame_output, text="Leaves", justify=tk.LEFT, anchor="w"
        )
        self.lvalues = [
            f"{4*(i+1)}" if (i + 1) % 2 and i != 2 else f"{4*(i+1)}f"
            for i in range(0, 8)
        ]
        self.lvalues.remove("28")
        self.lvalues.append("64f")
        self.lvalues.append("2")
        self.leaves = ttk.Combobox(
            self.Frame_output, value=self.lvalues, state="readonly"
        )
        self.leaves.current(0)
        self.addblankpages_label = ttk.Label(
            self.Frame_output, textvariable=self.addBlankpages, width=3
        )

        self.text_format = ttk.Label(
            self.Frame_output, text="Book Format", justify=tk.LEFT, anchor="w"
        )
        self.format_list = [x for x in data.PaperFormat.keys()]
        self.format = ttk.Combobox(
            self.Frame_output, value=self.format_list, state="readonly"
        )
        self.format.current(0)
        self.format.bind("<<ComboboxSelected>>", self.__set_format_values)

        self.text_fold = ttk.Label(
            self.Frame_output, text="Fold", justify=tk.LEFT, anchor="w"
        )
        self.fold = ttk.Checkbutton(
            self.Frame_output, variable=self.foldvalue, state=tk.DISABLED
        )
        self.leaves.bind("<<ComboboxSelected>>", self.__event_fold_enable)

        self.text_riffle = ttk.Label(
            self.Frame_output, text="Riffling direction", justify=tk.LEFT, anchor="w"
        )
        self.riffle = ttk.Combobox(
            self.Frame_output, values=["right", "left"], state="readonly"
        )
        self.riffle.current(0)

        self.filename_label.grid(row=2, column=0, pady=self.text_pady)
        self.filename_entry.grid(row=2, column=1, pady=self.text_pady)

        self.text_leaves.grid(row=3, column=0, pady=self.text_pady)
        self.leaves.grid(row=3, column=1, pady=self.text_pady)
        self.addblankpages_label.grid(row=3, column=2, pady=self.text_pady)

        self.text_format.grid(row=4, column=0, pady=self.text_pady)
        self.format.grid(row=4, column=1, pady=self.text_pady)

        self.text_fold.grid(row=5, column=0, pady=self.text_pady)
        self.fold.grid(row=5, column=1, pady=self.text_pady)

        self.text_riffle.grid(row=6, column=0, pady=self.text_pady)
        self.riffle.grid(row=6, column=1, pady=self.text_pady)

        self.Frame_output.grid(
            row=row,
            column=column,
            ipadx=padx,
            padx=(3 * padx, 3 * padx),
            pady=(3 * pady, 3 * pady),
            sticky="ns",
        )

    # -- Tab Advanced
    def advanced_imposition(
        self,
        row,
        column,
        padx,
        pady,
        width,
        height,
        relief,
        padding,
        entry_width=41,
    ):

        self.Frame_ad_imposition = ttk.LabelFrame(
            master=self.tab_advance,
            text="Sheet Work",
            width=width,
            height=height,
            relief=relief,
            padding=padding,
        )
        imposition_icon = ImageTk.PhotoImage(
            self.icons["imposition"], master=self.Frame_ad_imposition
        )
        split_icon = ImageTk.PhotoImage(self.icons["split"], master=self.Frame_ad_imposition)

        # self.FrameText_impositon = ttk.Label(self.Frame_ad_imposition, text="Sheet work setting",justify=tk.LEFT, anchor='w')

        self.blankpage_label = ttk.Label(
            self.Frame_ad_imposition, text="Blank page(s)", justify=tk.LEFT, anchor="w"
        )
        self.bp_modes = ["back", "front", "both"]
        self.blankpage = ttk.Combobox(
            self.Frame_ad_imposition, value=self.bp_modes, state="readonly"
        )
        self.blankpage.current(0)
        self.blankpage_label2 = ttk.Label(
            self.Frame_ad_imposition,
            text="back > front \nfor odd in 'both' mode",
            justify=tk.LEFT,
            anchor="w",
        )

        self.pagerange_label = ttk.Label(
            self.Frame_ad_imposition, text="Page range", justify=tk.LEFT, anchor="w"
        )
        range_validation = (self.window.register(self.__range_validation), "%P", r"%V")
        self.pagerange = ttk.Entry(
            self.Frame_ad_imposition,
            textvariable=self.pagerange_var,
            width=int(entry_width / 2),
            validate="all",
            validatecommand=range_validation,
        )
        self.pagerange_size = ttk.Label(
            self.Frame_ad_imposition,
            textvariable=self.page_range_size,
            justify=tk.LEFT,
            anchor="w",
        )
        if self.platform_mac:
            self.pagerange_example = ttk.Label(
                self.Frame_ad_imposition,
                text="1, 3-5, 10",
                justify=tk.LEFT,
                anchor="w",
                bg="white",
            )
        else:
            self.pagerange_example = tk.Label(
                self.Frame_ad_imposition,
                text="1, 3-5, 10",
                justify=tk.LEFT,
                anchor="w",
                bg="white",
            )
        

        self.sigcomposition_label = ttk.Label(
            self.Frame_ad_imposition,
            text="Sig composition",
            justify=tk.LEFT,
            anchor="w",
        )
        self.sigcomposition_nl = ttk.Label(
            self.Frame_ad_imposition, text="4=", justify=tk.LEFT, anchor="w"
        )
        self.sigcomposition_nn_combo = ttk.Combobox(
            self.Frame_ad_imposition, value=[1], state="readonly", width=3
        )
        self.sigcomposition_nn_combo.current(0)
        self.sigcomposition_nn_combo.bind("<<ComboboxSelected>>", self.__event_signature_set)
        self.sigcomposition_times = ttk.Label(
            self.Frame_ad_imposition, text="x", justify=tk.LEFT, anchor="w"
        )
        self.sigcomposition_ns_label = ttk.Label(
            self.Frame_ad_imposition, textvariable=self.ns
        )
        self.sigcomposition_example = ttk.Label(
            self.Frame_ad_imposition,
            text="(insert)x(fold)",
            justify=tk.LEFT,
            anchor="w",
        )

        self.customformat_label = ttk.Label(
            self.Frame_ad_imposition, text="Custom format", justify=tk.LEFT, anchor="w"
        )
        self.customformat_width_entry = ttk.Entry(
            self.Frame_ad_imposition,
            textvariable=self.custom_width,
            width=int(entry_width / 8),
        )
        self.customformat_times = ttk.Label(
            self.Frame_ad_imposition, text="x", justify=tk.LEFT, anchor="w"
        )
        self.customformat_height_entry = ttk.Entry(
            self.Frame_ad_imposition,
            textvariable=self.custom_height,
            width=int(entry_width / 8),
        )
        self.customformat_check = ttk.Checkbutton(
            self.Frame_ad_imposition,
            variable=self.customformatbool,
            command=self.__event_custom_format_entry,
        )
        self.customformat_example = ttk.Label(
            self.Frame_ad_imposition, text="(mm)x(mm)", justify=tk.LEFT, anchor="w"
        )
        self.customformat_width_entry.config(state=tk.DISABLED)
        self.customformat_height_entry.config(state=tk.DISABLED)

        self.imposition_label = ttk.Label(
            self.Frame_ad_imposition, text="Imposition", justify=tk.LEFT, anchor="w"
        )
        self.imposition = ttk.Checkbutton(
            self.Frame_ad_imposition, variable=self.impositionbool
        )
        self.imposition_icon = ttk.Label(
            self.Frame_ad_imposition, image=imposition_icon
        )
        self.imposition_icon.photo = imposition_icon

        self.splitpersig_label = ttk.Label(
            self.Frame_ad_imposition, text="Split per sig", justify=tk.LEFT, anchor="w"
        )
        self.splitpersig = ttk.Checkbutton(
            self.Frame_ad_imposition, variable=self.splitpersigbool
        )
        self.splitpersig_icon = ttk.Label(self.Frame_ad_imposition)
        self.splitpersig_icon.config(image=split_icon)
        self.splitpersig_icon.photo = split_icon

        # Grid
        # self.FrameText_impositon.grid(row=0, column=0, pady=2*self.text_pady)

        self.blankpage_label.grid(
            row=1, column=0, pady=self.text_pady, ipadx=self.text_pady
        )
        self.blankpage.grid(
            row=1, column=1, columnspan=4, pady=self.text_pady, ipadx=self.text_pady
        )
        self.blankpage_label2.grid(
            row=1, column=5, columnspan=2, pady=self.text_pady, ipadx=self.text_pady
        )

        self.pagerange_label.grid(
            row=2, column=0, pady=self.text_pady, ipadx=self.text_pady
        )
        self.pagerange.grid(
            row=2, column=1, columnspan=4, pady=self.text_pady, ipadx=self.text_pady
        )
        self.pagerange_size.grid(
            row=2, column=5, pady=self.text_pady, ipadx=self.text_pady
        )
        self.pagerange_example.grid(
            row=2, column=6, pady=self.text_pady, ipadx=self.text_pady
        )

        self.customformat_label.grid(
            row=3, column=0, pady=self.text_pady, ipadx=self.text_pady
        )
        self.customformat_check.grid(
            row=3, column=1, pady=self.text_pady, ipadx=self.text_pady
        )
        self.customformat_width_entry.grid(
            row=3, column=2, pady=self.text_pady, ipadx=self.text_pady
        )
        self.customformat_times.grid(
            row=3, column=3, pady=self.text_pady, ipadx=self.text_pady
        )
        self.customformat_height_entry.grid(
            row=3, column=4, pady=self.text_pady, ipadx=self.text_pady
        )
        self.customformat_example.grid(
            row=3, column=5, columnspan=2, pady=self.text_pady, ipadx=self.text_pady
        )

        self.sigcomposition_label.grid(
            row=4, column=0, pady=self.text_pady, ipadx=self.text_pady
        )
        self.sigcomposition_nl.grid(
            row=4, column=1, pady=self.text_pady, ipadx=self.text_pady
        )
        self.sigcomposition_nn_combo.grid(
            row=4, column=2, pady=self.text_pady, ipadx=self.text_pady
        )
        self.sigcomposition_times.grid(
            row=4, column=3, pady=self.text_pady, ipadx=self.text_pady
        )
        self.sigcomposition_ns_label.grid(
            row=4, column=4, pady=self.text_pady, ipadx=self.text_pady
        )
        self.sigcomposition_example.grid(
            row=4, column=5, columnspan=2, pady=self.text_pady, ipadx=self.text_pady
        )

        self.imposition_label.grid(
            row=5, column=0, pady=self.text_pady, ipadx=self.text_pady
        )
        self.imposition.grid(
            row=5, column=1, columnspan=4, pady=self.text_pady, ipadx=self.text_pady
        )
        self.imposition_icon.grid(
            row=5, column=5, columnspan=2, pady=self.text_pady, ipadx=self.text_pady
        )

        self.splitpersig_label.grid(
            row=6, column=0, pady=self.text_pady, ipadx=self.text_pady
        )
        self.splitpersig.grid(
            row=6, column=1, columnspan=4, pady=self.text_pady, ipadx=self.text_pady
        )
        self.splitpersig_icon.grid(
            row=6, column=5, columnspan=2, pady=self.text_pady, ipadx=self.text_pady
        )

        self.Frame_ad_imposition.grid(
            row=row,
            column=column,
            ipadx=padx,
            padx=(4 * padx, 4 * padx),
            pady=pady,
            sticky="ns",
        )

    def advanced_printing(
        self,
        row,
        column,
        padx,
        pady,
        width,
        height,
        relief,
        padding,
        entry_width=41,
    ):
        self.Frame_ad_printing = ttk.LabelFrame(
            master=self.tab_advance,
            text="Printing",
            width=width,
            height=height,
            relief=relief,
            padding=padding,
        )

        # Imagesetting
        sigproof_icon = ImageTk.PhotoImage(
            self.icons["proof"], master=self.Frame_ad_printing
        )
        trim_icon = ImageTk.PhotoImage(self.icons["trim"], master=self.Frame_ad_printing)
        registration_icon = ImageTk.PhotoImage(
            self.icons["registration"], master=self.Frame_ad_printing
        )
        cmyk_icon = ImageTk.PhotoImage(self.icons["cmyk"], master=self.Frame_ad_printing)

        self.sigproof_label = ttk.Label(
            self.Frame_ad_printing, text="Signature proof", justify=tk.LEFT, anchor="w"
        )
        self.sigproof_checkbox = ttk.Checkbutton(
            self.Frame_ad_printing, variable=self.sigproofbool
        )
        if self.platform_mac:
            self.sigproof_button = ttk.Button(
                self.Frame_ad_printing,
                width=3,
                height=1,
                text="  ",
                bg=self.sig_color.get(),
                command=self.__event_sig_color_set,
            )

        else:
            self.sigproof_button = tk.Button(
                self.Frame_ad_printing,
                width=3,
                height=1,
                text="  ",
                bg=self.sig_color.get(),
                command=self.__event_sig_color_set,
            )
        self.sigproof_icon = ttk.Label(self.Frame_ad_printing, image=sigproof_icon)
        self.sigproof_icon.photo = sigproof_icon

        self.trim_label = ttk.Label(
            self.Frame_ad_printing, text="Trim", justify=tk.LEFT, anchor="w"
        )
        self.trim_checkbox = ttk.Checkbutton(
            self.Frame_ad_printing, variable=self.trimbool
        )
        self.trim_icon = ttk.Label(self.Frame_ad_printing, image=trim_icon)
        self.trim_icon.photo = trim_icon

        self.registration_label = ttk.Label(
            self.Frame_ad_printing, text="Registration", justify=tk.LEFT, anchor="w"
        )
        self.registration_checkbox = ttk.Checkbutton(
            self.Frame_ad_printing, variable=self.registrationbool
        )
        self.registration_icon = ttk.Label(
            self.Frame_ad_printing, image=registration_icon
        )
        self.registration_icon.photo = registration_icon

        self.cmyk_label = ttk.Label(
            self.Frame_ad_printing, text="CMYK(mark)", justify=tk.LEFT, anchor="w"
        )
        self.cmyk_checkbox = ttk.Checkbutton(
            self.Frame_ad_printing, variable=self.cmykbool
        )
        self.cmyk_icon = ttk.Label(self.Frame_ad_printing, image=cmyk_icon)
        self.cmyk_icon.photo = cmyk_icon

        #margin setting 
        self.margin_label = ttk.Label(
            self.Frame_ad_printing, text="Margin(mm)", justify=tk.LEFT, anchor="w"
            )
        self.margin_entry = ttk.Entry(
            self.Frame_ad_printing,
            textvariable=self.margin,
            width=int(entry_width / 2)
        )
        int_vaild = (self.window.register(self.__int_validation),"%P")
        int_invaild = (self.window.register(self.__int_invaild), )
        self.margin_entry.config(validate="all", validatecommand=int_vaild, invalidcommand=int_invaild)


        self.sigproof_label.grid(row=0, column=0, pady=self.text_pady)
        self.sigproof_checkbox.grid(row=0, column=1, columnspan=2, pady=self.text_pady)
        self.sigproof_button.grid(
            row=0,
            column=3,
            padx=self.text_pady * 6,
            pady=self.text_pady * 6,
            sticky="n",
        )
        self.sigproof_icon.grid(row=0, column=4, pady=self.text_pady)

        self.trim_label.grid(row=1, column=0, pady=self.text_pady)
        self.trim_checkbox.grid(row=1, column=1, columnspan=2, pady=self.text_pady)
        self.trim_icon.grid(row=1, column=3, columnspan=4, pady=self.text_pady)

        self.registration_label.grid(row=2, column=0, pady=self.text_pady)
        self.registration_checkbox.grid(
            row=2, column=1, columnspan=2, pady=self.text_pady
        )
        self.registration_icon.grid(row=2, column=3, columnspan=4, pady=self.text_pady)

        self.cmyk_label.grid(row=3, column=0, pady=self.text_pady)
        self.cmyk_checkbox.grid(row=3, column=1, columnspan=2, pady=self.text_pady)
        self.cmyk_icon.grid(row=3, column=3, columnspan=4, pady=self.text_pady)

        self.margin_label.grid(row=4, column=0, pady=self.text_pady)
        self.margin_entry.grid(row=4, column=1, columnspan=6, pady=self.text_pady)

        self.Frame_ad_printing.grid(
            row=row,
            column=column,
            ipadx=padx,
            padx=(2 * padx, 2 * padx),
            pady=pady,
            sticky="ns",
        )

    # -- Tab Utils
    def utils_note(self,
        row,
        column,
        padx,
        pady,
        width,
        height,
        relief,
        padding,
        entry_width = 41):
        
        self.Frame_utils_note = ttk.LabelFrame(
            master=self.tab_utils,
            text="Note",
            width=width,
            height=height,
            relief=relief,
            padding=padding,
        )

        self.notemode_bool = tk.BooleanVar(value=False)
        self.notemode_label = ttk.Label(self.Frame_utils_note, text="Note mode")
        self.notemode_checkbox = ttk.Checkbutton(
            self.Frame_utils_note, 
            variable = self.notemode_bool, 
            command= self. __event_notemode_onoff)

        self.notepage_str = tk.StringVar(value="")
        self.notepages_label = ttk.Label(self.Frame_utils_note, text="Note Pages")
        self.notepages_entry = ttk.Entry(self.Frame_utils_note, textvariable = self.notepage_str, width=int(entry_width / 2))
        int_vaild = (self.window.register(self.__int_validation),"%P")
        int_invaild = (self.window.register(self.__int_invaild), )
        self.notepages_entry.config(validate="all", validatecommand=int_vaild, invalidcommand=int_invaild)

        self.Frame_pagenumbering = ttk.LabelFrame(
            master = self.Frame_utils_note,
            text = "Page numbering",
            width= width*0.7,
            height=height*0.7,
            relief=relief,
            padding=padding,
        )
        self.pagenumbering_bool = tk.BooleanVar(value=False)
        self.pagenumbering_label = ttk.Label(self.Frame_pagenumbering, text="On/Off")
        self.pagenumbering_checkbox = ttk.Checkbutton(self.Frame_pagenumbering, variable=self.pagenumbering_bool, command=self.__event_page_numbering_onoff)
        self.pagenumbering_checkbox_id = self.pagenumbering_checkbox.winfo_id()

        self.notepagenumbering_pages_label = ttk.Label(self.Frame_pagenumbering, text="Numbering")
        self.notepagenumbering_pages_combobox = ttk.Combobox(
            self.Frame_pagenumbering, value=data.pagespec, state="readonly"
        )
        self.notepagenumbering_pages_combobox.current(0)
        self.notepagenumbering_pages_combobox.bind("<<ComboboxSelected>>", self.__event_pagenumber_select)


        self.notepagenumbering_location_label = ttk.Label(self.Frame_pagenumbering, text="Location")
        self.notepagenumbering_location_combobox = ttk.Combobox(
            self.Frame_pagenumbering, value=data.pagehf, state="readonly"
        )
        self.notepagenumbering_location_combobox.current(0)
        
        self.notepagenumbering_align_label = ttk.Label(self.Frame_pagenumbering, text="Align")
        self.notepagenumbering_align_combobox = ttk.Combobox(
            self.Frame_pagenumbering, value = data.pagealign, state="readonly"
        )
        self.notepagenumbering_align_combobox.current(0)

        for child in self.Frame_pagenumbering.winfo_children():
            child.config(state="disable")

        # pagenumbering grid
        self.pagenumbering_label.grid(row=0, column=0, pady=self.text_pady, ipadx=self.text_pady)
        self.pagenumbering_checkbox.grid(row=0, column=1, pady=self.text_pady, ipadx=self.text_pady)
        self.notepagenumbering_pages_label.grid(row=1, column=0, pady=self.text_pady, ipadx=self.text_pady)
        self.notepagenumbering_pages_combobox.grid(row=1, column=1, pady=self.text_pady, ipadx=self.text_pady)
        self.notepagenumbering_location_label.grid(row=2, column=0, pady=self.text_pady, ipadx=self.text_pady)
        self.notepagenumbering_location_combobox.grid(row=2, column=1, pady=self.text_pady, ipadx=self.text_pady)
        self.notepagenumbering_align_label.grid(row=3, column=0, pady=self.text_pady, ipadx=self.text_pady)
        self.notepagenumbering_align_combobox.grid(row=3, column=1, pady=self.text_pady, ipadx=self.text_pady)
        # main grid
        self.notemode_label.grid(row= 0, column=0)
        self.notemode_checkbox.grid(row= 0, column=1)
        self.notepages_label.grid(row=1, column=0,pady=self.text_pady, ipadx=self.text_pady)
        self.notepages_entry.grid(row=1, column=1,pady=self.text_pady, ipadx=self.text_pady)
        self.Frame_pagenumbering.grid(row=2, column=0, columnspan=4)

        self.Frame_utils_note.grid(
            row= row,
            column = column,
            ipadx = 2*padx,
            padx = (2*padx, 2*padx),
            pady= pady,
            sticky = "nsew"
        )
    
    def utils_misc(self,
        row,
        column,
        padx,
        pady,
        width,
        height,
        relief,
        padding,
        entry_width = 41):

        int_validation = (self.window.register(self.__int_validation), "%P")
        int_invalid = (self.window.register(self.__int_invaild), )
        
        self.Frame_utils_misc = ttk.LabelFrame(
            master=self.tab_utils,
            text="Miscellaneous",
            width=width,
            height=height,
            relief=relief,
            padding=padding,
        )

        self.imageconvert_bool = tk.BooleanVar(value=False)
        self.imageconvert_dpi_int = tk.IntVar(value=600)

        self.imageconvert_label = ttk.Label(
            self.Frame_utils_misc, 
            text="Convert to image"
            )
        self.imageconvert_checkbox = ttk.Checkbutton(
            self.Frame_utils_misc, 
            variable=self.imageconvert_bool
            )
        self.imageconvert_dpi_label = ttk.Label(
            self.Frame_utils_misc, 
            text="dpi"
            )
        self.imageconvert_dpi_entry = ttk.Entry(
            self.Frame_utils_misc, 
            textvariable= self.imageconvert_dpi_int, 
            validate="all", 
            validatecommand= int_validation,
            width = int(entry_width/8)
            ) 
        self.imageconvertexplain_label = ttk.Label(
            self.Frame_utils_misc, 
            text="Prevent the broken \nin transformation."
            )
        

        self.Frame_custom_imposition = ttk.LabelFrame(
            master = self.Frame_utils_misc,
            text = "Custom imposition",
            width= width*0.7,
            height=height*0.7,
            relief=relief,
            padding=padding,
        )

        self.custom_imposition_bool = tk.BooleanVar(value=False)
        self.custom_imposition_label= ttk.Label(self.Frame_custom_imposition, text="On/Off")
        self.custom_imposition_checkbox = ttk.Checkbutton(
            self.Frame_custom_imposition, 
            variable=self.custom_imposition_bool,
            command= self.__event_custom_imposition)
        self.custom_imposition_label_id = self.custom_imposition_label.winfo_id()
        self.custom_imposition_checkbox_id = self.custom_imposition_checkbox.winfo_id()
        
        self.custom_imposition_sig_int = tk.IntVar(value=1)
        self.custom_imposition_sig_label = ttk.Label(self.Frame_custom_imposition, text="Leaves per sig")
        self.custom_imposition_sig_entry = ttk.Entry(self.Frame_custom_imposition,
            textvariable= self.custom_imposition_sig_int,
            validate="all",
            validatecommand=int_validation,
            width =int(entry_width/7))
        
        self.custom_impostion_leaves_int = tk.IntVar(value = 1)
        self.custom_imposition_leaves_label = ttk.Label(self.Frame_custom_imposition, text="Leaves")
        self.custom_imposition_leaves_entry = ttk.Entry(self.Frame_custom_imposition, 
            textvariable=self.custom_impostion_leaves_int,
            validate="all",
            validatecommand=int_validation)

        self.custom_sig_layout_row = tk.IntVar(value=1)
        self.custom_sig_layout_column = tk.IntVar(value=1)

        self.custom_sig_layout_label = ttk.Label(self.Frame_custom_imposition, text= "Sig Layout")
        self.custom_sig_layout_row_entry = ttk.Entry(self.Frame_custom_imposition, textvariable=self.custom_sig_layout_row, width =int(entry_width/5))
        self.custom_sig_layout_column_label = ttk.Label(self.Frame_custom_imposition, textvariable=self.custom_sig_layout_column, width = int(entry_width/5))
        self.custom_sig_layout_x_label = ttk.Label(self.Frame_custom_imposition, text="x")
        
        layout_validation = (self.window.register(self.__layout_validation), r"%P", r"%s",r"%V")
        self.custom_sig_layout_row_entry.config(validate = "all", validatecommand=layout_validation)

        self.custom_sig_impostion_front_str= tk.StringVar(value="")
        self.custom_sig_impostion_back_str= tk.StringVar(value="")

        self.custom_sig_imposition_front_label = ttk.Label(self.Frame_custom_imposition, text="Front")
        self.custom_sig_imposition_back_label = ttk.Label(self.Frame_custom_imposition, text="Back")
        self.custom_sig_imposition_front_entry = ttk.Entry(self.Frame_custom_imposition, textvariable= self.custom_sig_impostion_front_str, width= int(entry_width))
        self.custom_sig_imposition_back_entry = ttk.Entry(self.Frame_custom_imposition, textvariable=  self.custom_sig_impostion_back_str, width= int(entry_width))
        
        
        for child in self.Frame_custom_imposition.winfo_children():
            if child.winfo_id() != self.custom_imposition_checkbox_id and child.winfo_id() != self.custom_imposition_label_id:
                child.config(state="disable")
        # grid-----------------------------
        self.imageconvert_label.grid(row=0, column=0, pady=self.text_pady, ipadx=self.text_pady)
        self.imageconvert_checkbox.grid(row=0, column=1, pady=self.text_pady, ipadx=self.text_pady)
        self.imageconvert_dpi_label.grid(row=0, column=2, pady=self.text_pady, ipadx=self.text_pady)
        self.imageconvert_dpi_entry.grid(row=0, column=3, pady=self.text_pady, ipadx=self.text_pady)
        self.imageconvertexplain_label.grid(row=0, column=4, pady=self.text_pady, ipadx=self.text_pady)

        self.custom_imposition_label.grid(row=0, column = 0, pady=self.text_pady, ipadx=self.text_pady)
        self.custom_imposition_checkbox.grid(row=0, column = 1, columnspan=3, pady=self.text_pady, ipadx=self.text_pady)
        
        self.custom_imposition_sig_label.grid(row=1, column=0, pady=self.text_pady, ipadx=self.text_pady)
        self.custom_imposition_sig_entry.grid(row=1, column=2, pady=self.text_pady, ipadx=self.text_pady)
        
        self.custom_sig_layout_label.grid(row= 2, column=0, pady=self.text_pady, ipadx=self.text_pady)
        self.custom_sig_layout_row_entry.grid(row= 2, column=1, pady=self.text_pady, ipadx=self.text_pady)
        self.custom_sig_layout_x_label.grid(row= 2, column=2, pady=self.text_pady, ipadx=self.text_pady)
        self.custom_sig_layout_column_label.grid(row= 2, column=3, pady=self.text_pady, ipadx=self.text_pady)

        self.custom_sig_imposition_front_label.grid(row=3, column=0, pady=self.text_pady, ipadx=self.text_pady)
        self.custom_sig_imposition_back_label.grid(row=4, column=0, pady=self.text_pady, ipadx=self.text_pady)
        self.custom_sig_imposition_front_entry.grid(row=3, column=1, columnspan=3, pady=self.text_pady, ipadx=self.text_pady)
        self.custom_sig_imposition_back_entry.grid(row=4, column=1, columnspan=3, pady=self.text_pady, ipadx=self.text_pady)

        self.Frame_custom_imposition.grid(row=1, column=0, columnspan=5, pady=self.text_pady, ipadx=self.text_pady)

        self.Frame_utils_misc.grid(
            row= row,
            column = column,
            ipadx = 2*padx,
            padx = (2*padx, 2*padx),
            pady= pady,
            sticky = "nsew"
        )
    # Internal routines---------------------------
    def __beep(self) -> NoReturn:
        """Generate bepp sound

        Returns:
            NoReturn: It takes 0.5 sec for beeping (ping sound).
        """
        wave_obj = simpleaudio.WaveObject.from_wave_file(self.beep_file)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    def __get_file_info(self, path_str:str
        ) -> Tuple[
            Union[bool, str],
            Union[bool, str],
            Union[bool, int],
            Union[bool, list[float, float]]
        ]:

        if type(path_str) != str:
            raise TypeError(
                f"Given path must be a string variable. Current:{type(path_str)}"
            )

        path = Path(path_str)

        if not path.is_file():
            raise ValueError("File {path} does not exist.")

        pdf = pypdf.PdfFileReader(path)

        page_num = pdf.getNumPages()

        if page_num != 0:  # check whether pdf is empty or not.
            pdfinfo = pdf.metadata

            title = pdfinfo["/Title"] if "/Title" in pdfinfo.keys() else "None"
            authors = pdfinfo["/Author"] if "/Author" in pdfinfo.keys() else "Unkown"

            page_size = [
                float(pdf.getPage(0).mediaBox.width),
                float(pdf.getPage(0).mediaBox.height),
            ]

            return title, authors, page_num, page_size

        return False, False, False, False

    def __event_open_file(self):
        """Search the pdf file and, if it is vaild file, extract basic meta informations from the file.

        Returns:
            int: Return zero.
        """
        filename = filedialog.askopenfilename(
            initialdir="~", title="Select Manuscript", filetypes=(("PDF", "*.pdf"),)
        )
        if filename != "":
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)

            title, author, page_num, pagesize = self.__get_file_info(filename)
            if title != False:
                self.title.set(title)
                self.author.set(author)
                self.page_n.set(int(page_num))
                self.page_range_size.set(int(page_num))

                self.pagerange_var.set(f"1-{self.page_n.get()}")

                width, height = pts2mm(pagesize)

                self.page_format.set(f"{width}x{height}")

                self.custom_width.set(width)
                self.custom_height.set(height)

                file_name_with_format = os.path.split(str(filename))[1]
                file_name = file_name_with_format.split(".pdf")
                self.filename.set(file_name[0] + "_HP_BOOKLET" + ".pdf")
                self.output_entry.insert(0, os.path.split(str(filename))[0])

                print(f"title:{self.title.get()}\nfile:{filename}")
                self.Generate_button.config(state=tk.ACTIVE)

            else:
                print(f"Not a vaild PDF file: file ({filename})")
                self.Generate_button.config(state=tk.DISABLED)
        self.__event_fold_enable(False)
        return 0

    def __event_open_output_directory(self):
        """Open an output directory path of the result file.

        Returns:
            _type_: _description_
        """
        directory = filedialog.askdirectory(
            initialdir="~",
            title="Select Directory",
        )
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, directory)

        return 0

    def __event_fold_enable(self, event):
        """Event function when use choose one item of the leaves list.
           * Disable or enable fold checkbox below the leaves listbox.
           * Calculate the additional blank pages of the each choosed leaves number.  

        """

        leaves = self.leaves.get()
        fcheck = False
        if "f" in leaves:
            self.fold.config(state=tk.NORMAL)
            n_l = int(leaves.split("f")[0])
            fcheck = True
        else:
            self.foldvalue.set(False)
            self.fold.config(state=tk.DISABLED)
            n_l = int(leaves)

        pagenumber = self.page_range_size.get()

        # calculate blank page
        if pagenumber < n_l:
            addb = n_l - pagenumber
        else:
            k = pagenumber % n_l
            addb = (n_l - k) if n_l > 1 and k != 0 else 0
        print(f"Addtional Blank Page: {addb}")
        self.addBlankpages.set(addb)

        # Signature composition
        self.sigcomposition_nl.configure(text=f"{n_l} =")

        if n_l == 2:
            self.sigcomposition_nn_combo.config(value=[1])
            self.ns.set(2)
        elif fcheck:
            if n_l == 12:
                self.sigcomposition_nn_combo.config(value=[1, 3])
            elif n_l == 24:
                self.sigcomposition_nn_combo.config(value=[1, 2, 3, 6])
            else:
                self.sigcomposition_nn_combo.config(
                    value=[int(2**i) for i in range(0, int(log2(n_l) - 1))]
                )
            self.ns.set(n_l)
        else:
            self.sigcomposition_nn_combo.config(value=[int(n_l / 4)])
            self.ns.set(4)

        self.sigcomposition_nn_combo.current(0)

    def __event_signature_set(self, event):
        nl = int(self.sigcomposition_nl.cget("text").split("=")[0])
        nn = int(self.sigcomposition_nn_combo.get())

        ns = int(nl / nn)

        if ns == 4:
            self.foldvalue.set(False)
        else:
            self.foldvalue.set(True)

        self.ns.set(int(nl / nn))

    #__custom_format_entry_enable_f
    def __event_custom_format_entry(self):
        if self.customformatbool.get():
            self.customformat_width_entry.config(state=tk.ACTIVE)
            self.customformat_height_entry.config(state=tk.ACTIVE)
        else:
            self.customformat_width_entry.config(state=tk.DISABLED)
            self.customformat_height_entry.config(state=tk.DISABLED)

    def __range_validation(self, value, event):
        print(event)
        text = value.replace(" ", "")
        # self.pagerange_var.set(text)
        vaild = True

        if text == "" or text == None:
            return True

        initial_value = text[0]
        if initial_value not in "123456789":
            return False
        if self.character_validation_re.search(text) != None:
            print(self.character_validation_re.findall(text))
            vaild = False

        rangelist = self.range_validation_re.findall(text)

        range = 0
        if vaild == True:
            pre = 1
            max = int(self.page_n.get())
            for st in rangelist:
                if "-" in st:
                    i_s, l_s = st.split("-")
                    i = int(i_s)
                    l = int(l_s)
                    if (i <= pre and pre > 1) or l > max:
                        vaild = False
                        print(f"{i}-{l}, pre:{pre}, max:{max}")
                    if i >= l:
                        if event !="focusout" and len(i_s) >= len(l_s):
                            return True
                        else:
                            self.pagerange_var.set(f"1-{max}")
                            vaild = False
                            print(f"{i}>{l}")
                    pre = l
                    range += l - i + 1
                else:
                    n = int(st)
                    if (n <= pre and pre > 1) or n > max:
                        print(f"{n}")
                        vaild = False
                    range += 1

        if vaild:
            self.page_range_size.set(range)
            self.__event_fold_enable(True)
        #    self.pagerange_example.config(bg="#ffffff")
        #    if self.platform_mac:
        #        self.pagerange_example.config(highlightbackground = "#ffffff")
            self.Generate_button.config(state=tk.ACTIVE)

        else:
        #    self.pagerange_example.config(bg="#d0342c")
        #    if self.platform_mac:
        #        self.pagerange_example.config(highlightbackground = "#d0342c")
            self.Generate_button.config(state=tk.DISABLED)
            return False

        return True

    # sig_color_set
    def __event_sig_color_set(self):
        color = askcolor()
        if color is not None:
            colorhex = color[1]
            if colorhex is None:
                return 1
            c, m, y, k = hex2cmyk(colorhex)
            r, g, b = cmyk2rgb(c, m, y, k)
            cmyk_hex = rgb2hex(r, g, b)
            self.sig_color.set(cmyk_hex)
            self.sigproof_button.configure(bg=cmyk_hex)
            return 0
        return 1

    def __set_format_values(self, event=None):
        formatname = self.format.get()
        if formatname == "Default":
            return 1
        else:
            width, height = data.PaperFormat[formatname].split("x")

            self.custom_width.set(width)
            self.custom_height.set(height)

            return 0

    # set_pagenumber_select
    def __event_pagenumber_select(self, event=None):
        pagetype = self.notepagenumbering_pages_combobox.get()
        if "Both" != pagetype:
            self.notepagenumbering_location_combobox.config(value = data.pagehf_e)
            self.notepagenumbering_align_combobox.config(value= data.pagealign_e) 
        else:
            self.notepagenumbering_location_combobox.config(value = data.pagehf)
            self.notepagenumbering_align_combobox.config(value= data.pagealign) 
        
        self.notepagenumbering_location_combobox.current(0)
        self.notepagenumbering_align_combobox.current(0)
    def __event_notemode_onoff(self, event=None):
        onoff = self.notemode_bool.get()
        if onoff:
            state = "enable"
            self.pagenumbering_bool.set(True)
        else:
            state = "disable"
            self.pagenumbering_bool.set(False)
        
        self.notepages_entry.config(state=state)
        for child in self.Frame_pagenumbering.winfo_children():
            if "!combobox" in child.winfo_name() and state == "enable":
                child.config(state="readonly")
            else:
                child.config(state=state)
    def __event_page_numbering_onoff(self, event=None):
        onoff = self.pagenumbering_bool.get()
        if onoff:
            state = "enable"
        else:
            state = "disable"
        for child in self.Frame_pagenumbering.winfo_children():
            if child.winfo_id() == self.pagenumbering_checkbox_id:
                pass
            else:
                if "!combobox" in child.winfo_name() and state == "enable":
                    child.config(state="readonly")
                else:
                    child.config(state=state)
    def __event_custom_imposition(self, event=None):
        onoff = self.custom_imposition_bool.get()
        if onoff:
            state = "enable"
        else:
            state = "disable"
        for child in self.Frame_custom_imposition.winfo_children():
            if child.winfo_id() == self.custom_imposition_checkbox_id and child.winfo_id() != self.custom_imposition_label_id:
                pass
            else:
                child.config(state=state)
    
    def __int_validation(self, value):
        if value == "" or value == None:
            return True
        if "-" in value:
            return False
        try:
            value=int(value) 
        except:
            return False 
        return True
    def __int_invaild(self):
        print('Please enter an integer value')
    
    def __layout_validation(self, value, stored_value, event): #focusing in
        if value =="" or value ==None:
            return True
        if "-" in value:
            return False

        try:
            value = int(value)
        except:
            return False
        
        sig_leaves = self.custom_imposition_sig_int.get()

        if event=="focusout":
            layout_row = int(stored_value)
            if sig_leaves%layout_row:
                self.custom_sig_layout_row.set(1)
                self.custom_sig_layout_column.set(sig_leaves)
                return False
            else:
                return True
        else:
            
            layout_row = value

            if sig_leaves%layout_row:
                if len(str(sig_leaves)) <= len(str(layout_row)):
                    return False
                else:
                    return True
            else:
                self.custom_sig_layout_column.set(int(sig_leaves/layout_row))
                return True

    # Pass to parameters to PDF routine
    def pdf_progress_popup(self, page_range, nl, impositionbool):

        tpadx = tpady = 10
        sub_window = tk.Toplevel(self.window)
        sub_window.title(f"{self.filename.get()}")

        self.icon_setting(sub_window)

        progress_length = 2 * len(page_range) if impositionbool else len(page_range)
        print("Pro_length:", progress_length)
        sub_progress = ttk.Progressbar(
            sub_window, orient="horizontal", mode="determinate", maximum=progress_length
        )
        sub_progress.grid(column=0, row=0, padx=10, pady=20)
        progress_text = tk.StringVar(value="Start conversion")
        sub_progress_text_label = ttk.Label(sub_window, textvariable=progress_text)
        sub_progress_text_label.grid(column=0, row=1, padx=10, pady=20)

        destorybutton = ttk.Button(
            sub_window,
            text="OK",
            width=15,
            comman=sub_window.destroy,
            state=tk.DISABLED,
        )
        destorybutton.grid(column=0, row=2, padx=int(2 * tpadx), pady=int(2 * tpady))

        return sub_window, sub_progress, progress_text, progress_length, destorybutton

    def gen_button_action(self):

        # inputfile----------------------------------------------------
        input_file = self.input_entry.get()
        # outputfile----------------------------------------------------
        filename = self.filename.get()
        if ".pdf" not in filename:
            filename = filename + ".pdf"

        output_path = self.output_entry.get()

        # pagerange--------------------------------------------------------
        pagerange: str = self.pagerange.get()
        # Leaves and sub signature---------------------------------------------------------------
        leaves = (self.leaves.get()).split("f")
        nl = int(leaves[0])
        nn = int(self.sigcomposition_nn_combo.get())
        ns = int(self.ns.get())
        # Fold----------------------------------------------------------------------------------
        foldbool: bool = self.foldvalue.get()
        # Riffle direction----------------------------------------------------------------------
        rifflebool: bool = True if self.riffle.get() == "right" else False

        # Format----------------------------------------------------------------------------------
        formatbool = False
        format_width = 0.0
        format_height = 0.0
        formatname = ""
        formatbool = self.customformatbool.get()
        if formatbool:
            format_width = self.custom_width.get()
            format_height = self.custom_height.get()
        else:
            formatname = self.format.get()
            if formatname == "Default":
                wh = self.page_format.get().split("x")
                wh[0] = float(wh[0])
                wh[1] = float(wh[1])
            else:
                formatbool = True
                wh = data.PaperFormat[formatname].split("x")

            format_width = wh[0]  # mm
            format_height = wh[1]

        # Imposition----------------------------------------------------------------------------
        impositionbool: bool = self.impositionbool.get()
        if impositionbool:
            foldbool = True
        # blank
        blankmode: str = self.blankpage.get()
        blanknumber: int = self.addBlankpages.get()
        # Split---------------------------------------------------------------------------------
        splitbool: bool = self.splitpersigbool.get()
        # Signature Proof-----------------------------------------------------------------------
        sigproofbool: bool = self.sigproofbool.get()
        sig_color: str = self.sig_color.get()
        # Trim Mark-----------------------------------------------------------------------------
        trimbool: bool = self.trimbool.get()
        # Registration Mark---------------------------------------------------------------------
        registrationbool: bool = self.registrationbool.get()
        # CYMK Mark-----------------------------------------------------------------------------
        cmykbool: bool = self.cmykbool.get()

        margin = mm2pts(self.margin.get(), False)

        print(
            f"Document:{filename}\n signature leaves: {nl} \n direction: {self.riffle.get()}"
        )

        print("Variable:\t value")
        print(f"input file:\t{input_file} ")
        print(f"Output path:\t{output_path} ")
        print(f"page range:\t\t{pagerange} ")
        print(f"leaves:\t{[nl, nn, ns]} ")
        print(f"fold:\t{foldbool}")
        print(f"riffle:\t{rifflebool}")
        print(f"format:\t [{formatbool},{format_width} ,{format_height} ]")
        print(f"imposition:\t{impositionbool}")
        print(f"blank:\t [{blankmode},{blanknumber}]")
        print(f"split:\t{splitbool}")
        print(f"sigproof:\t[{sigproofbool},{sig_color}]")

        # ----------------------------------------------------------------

        # Modulate file
        # manuscript, writer, meta = get_writer_and_manuscript(input_file)

        # per_sig, per_riffle = get_arrange_permutations([nl,nn,ns], rifflebool)
        # blocks, composition, layout = get_arrange_determinant(page_range, [nl, nn, ns], foldbool)
        # format_width, format_height = pts_mm((format_width , format_height), False) #mm to pts
        #
        # print(blocks)
        # Generate popup window(progress bar)

        ndbool = trimbool or registrationbool or cmykbool
        printbool = sigproofbool or ndbool

        #page_range = get_exact_page_range(pagerange, [blankmode, blanknumber])

        

        default_gap = 5
        manuscript = Manuscript(
                          input = input_file,
                          output = output_path,
                          filename = filename,
                          page_range = pagerange
                      )
        _sig_composition = SigComposition(nl, nn)
        toimage = ToImage(
                       toimage = False,
                       dpi= 600
                      )
        
        signature = Signature(
                          sig_composition = _sig_composition,
                          blank_mode = blankmode,
                          riffle = rifflebool,
                          fold = foldbool,
                          paper_format = [
                            mm2pts(float(format_width), mode = False), 
                            mm2pts(float(format_height), mode = False)]
                      )
        imposition = Imposition(
                          imposition = impositionbool,
                          gap = default_gap,
                          proof = sigproofbool ,
                          proof_color = sig_color,
                          proof_width = default_gap,
                          imposition_layout = _sig_composition
                      )
        printing_mark = PrintingMark(
                          on = True if trimbool or registrationbool or cmykbool else False,
                          margin = margin,
                          crop = trimbool,
                          reg = registrationbool,
                          cmyk = cmykbool,
                      )
        modifiers = [toimage, signature, imposition, printing_mark]
        #(
        #    sub_popup,
        #    sub_progress,
        #    progress_text,
        #    progress_length,
        #    destroybutton,
        #) = self.pdf_progress_popup(pagerange, modifiers)
        #self.window.wait_window(sub_popup)
        for modifier in modifiers:
              manuscript.modifier_register(modifier)
        mode = "safe"
        manuscript.update(file_mode = mode)
        manuscript.save_to_file(split=splitbool)
        del(manuscript)

        # old code
        # generate_signature(
        #     inputfile=input_file,
        #     output=output_path,
        #     pagerange=pagerange,
        #     blank=[blankmode, blanknumber],
        #     sig_com=[nl, nn, ns],
        #     riffle=rifflebool,
        #     fold=foldbool,
        #     format=[format_width, format_height],
        #     imposition=impositionbool,
        #     split=splitbool,
        #     trim=trimbool,
        #     registration=registrationbool,
        #     cmyk=cmykbool,
        #     sigproof=[sigproofbool, sig_color],
        #     progress=[progress_length, sub_progress, progress_text, sub_popup],
        # )

        #sub_progress["value"] = progress_length
        #progress_text.set(f"Done")
        #sub_popup.update()
        #destroybutton.config(state=tk.ACTIVE)

        print("Done")

        self.__beep()

        #sub_popup.transient(self.window)
        #sub_popup.grab_set()
        #self.window.wait_window(sub_popup)

        return 0


if __name__ == "__main__":
    from data import *
    
    text_pady = 3

    hpbooklet = Booklet(
            task_bar_icon,
            homepage=homepage,
            source=git_repository,
            tutorial=tutorial,
            textpady=text_pady,
            beep_file=beep_file,
            logo=logo,
            icons= icons
        )
    hpbooklet.window.mainloop()

    
